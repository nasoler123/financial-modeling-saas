from __future__ import annotations

import math
from datetime import date
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union

Scalar = Union[None, float, int, bool, str, date]
SeriesGetter = Callable[[str, str, date], Optional[float]]  # (driver_id, series_mode, period_start)->value


def month_start(d: date) -> date:
    return date(d.year, d.month, 1)


def add_months(d: date, months: int) -> date:
    # Always return first-of-month (we operate on month buckets)
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return date(y, m, 1)


def parse_period_start(value: Any) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date):
        return month_start(value)
    s = str(value).strip()
    if not s:
        return None
    try:
        return month_start(date.fromisoformat(s[:10]))
    except Exception:
        return None


def _to_float(x: Scalar) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, bool):
        return 1.0 if x else 0.0
    if isinstance(x, (int, float)):
        f = float(x)
        return f if math.isfinite(f) else None
    if isinstance(x, str):
        s = x.strip()
        if not s:
            return None
        try:
            f = float(s)
            return f if math.isfinite(f) else None
        except Exception:
            return None
    return None


def _truthy(x: Scalar) -> bool:
    if x is None:
        return False
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        try:
            return float(x) != 0.0
        except Exception:
            return False
    if isinstance(x, str):
        return bool(x.strip())
    if isinstance(x, date):
        return True
    return False


def _effective_series(mode: str, dep_driver_id: str, owner_driver_id: str, requested: str) -> str:
    m = (mode or "").strip().lower()
    req = (requested or "").strip().lower() or ("actual" if m == "actual" else "value")
    if m in {"forecast", "value"} and dep_driver_id != owner_driver_id and req == "actual":
        return "value"
    if req not in {"actual", "forecast", "value"}:
        return "value" if m in {"forecast", "value"} else "actual"
    return req


def compute_expression_series_monthly(
    ast: Mapping[str, Any],
    *,
    periods: List[date],
    owner_driver_id: str,
    mode: str,
    close_month_start: date,
    get_value: SeriesGetter,
    period_overrides: Optional[Mapping[Any, Any]] = None,
    period_adjust: Optional[Mapping[Any, Any]] = None,
) -> Dict[date, Optional[float]]:
    """Project a driver's monthly series by evaluating its AST per month.

    What-if hooks (both chronological, so they roll forward through self-references read from ``out``):
      * ``period_overrides`` {period -> value} FIXES a month to a given value INSTEAD of evaluating the
        formula (a fixed level that the next month's self-ref then rolls forward).
      * ``period_adjust`` {period -> (kind, value)} evaluates the formula NORMALLY and then transforms the
        result: ``pct``/``percent`` → ×(1+value/100), ``delta`` → +value, ``set``/``fixed`` → =value. The
        transformed value is stored in ``out``, so a % applied over a RANGE COMPOUNDS month over month
        (each month's self-ref reads the previous month's already-adjusted value), instead of every month
        landing on a flat ``base×factor``. ``period_overrides`` wins over ``period_adjust`` for a month.
    """
    m = (mode or "").strip().lower()
    if m not in {"actual", "forecast", "value"}:
        raise ValueError("mode must be actual/forecast/value")

    overrides_norm: Dict[date, float] = {}
    for raw_key, raw_val in (period_overrides or {}).items():
        d = month_start(raw_key) if isinstance(raw_key, date) else parse_period_start(raw_key)
        fv = _to_float(raw_val)
        if d is not None and fv is not None:
            overrides_norm[d] = fv

    adjust_norm: Dict[date, Tuple[str, float]] = {}
    for raw_key, raw_spec in (period_adjust or {}).items():
        d = month_start(raw_key) if isinstance(raw_key, date) else parse_period_start(raw_key)
        if d is None or not isinstance(raw_spec, (tuple, list)) or len(raw_spec) < 2:
            continue
        kind = str(raw_spec[0] or "").strip().lower()
        fv = _to_float(raw_spec[1])
        if kind and fv is not None:
            adjust_norm[d] = (kind, fv)

    ordered = sorted([month_start(p) for p in periods])
    out: Dict[date, Optional[float]] = {}
    forecast_out: Dict[date, Optional[float]] = {}

    def eval_node(node: Mapping[str, Any], *, cur: date) -> Scalar:
        t = str(node.get("type") or "").strip().lower()

        if t == "const":
            return _to_float(node.get("value"))
        if t == "literal":
            v = node.get("value")
            if isinstance(v, (str, int, float, bool)) or v is None or isinstance(v, date):
                return v
            return str(v)
        if t == "ref":
            did_raw = str(node.get("driver_id") or "").strip()
            if not did_raw:
                return None
            try:
                off_i = int(node.get("offset_months", 0) or 0)
            except Exception:
                off_i = 0
            anchor_raw = node.get("anchor_period")
            anchor_period = anchor_raw.strip() if isinstance(anchor_raw, str) and anchor_raw.strip() else None
            anchor_date = parse_period_start(anchor_period) if anchor_period else None
            series_req = str(node.get("series") or "").strip().lower() or ("actual" if m == "actual" else "value")
            is_literal_self = did_raw.lower() == "self"
            is_owner_id = did_raw == owner_driver_id
            is_self_ref = is_literal_self or (is_owner_id and anchor_date is None)
            eff_series = _effective_series(m, owner_driver_id if is_self_ref else did_raw, owner_driver_id, series_req)
            target = anchor_date if anchor_date is not None else add_months(cur, off_i)
            if is_self_ref:
                # -----------------------------
                # Self reference semantics:
                # - In ACTUAL mode: use already computed `out` when available.
                # - In FORECAST/VALUE mode:
                #   * self.actual for months <= close MUST come from materialized ACTUALs (get_value),
                #     not from `out` (which contains forecast outputs + placeholders for pre-close months).
                #   * self.actual for months > close is treated as the forecasted value for that month.
                # -----------------------------

                if eff_series == "actual":
                    if m == "actual":
                        if target in out:
                            return out.get(target)
                        return get_value(owner_driver_id, "actual", target)

                    # m in {"forecast","value"}
                    if target <= close_month_start:
                        # Critical fix: do NOT read out[target] here (it is None pre-close in forecast mode).
                        return get_value(owner_driver_id, "actual", target)

                    # target > close => "actual" in the future means forecasted output
                    if target in forecast_out:
                        return forecast_out.get(target)
                    if target in out:
                        return out.get(target)
                    try:
                        return get_value(owner_driver_id, "forecast", target)
                    except Exception:
                        return None

                # eff_series != "actual" (value / forecast)
                if m == "actual":
                    # In FORECAST/VALUE mode, self.actual for months <= close MUST come from materialized ACTUALs,
                    # not from `out` (which may contain forecast outputs + placeholders for pre-close months).
                    if target <= close_month_start:
                        return get_value(owner_driver_id, "actual", target)

                    # For months > close, "actual" in the future means "use the forecasted output for that month".
                    if target in forecast_out:
                        return forecast_out.get(target)
                    if target in out:
                        return out.get(target)
                    try:
                        return get_value(owner_driver_id, "forecast", target)
                    except Exception:
                        return None

                # m in {"forecast","value"}
                if eff_series == "value":
                    # value pre-close == actual
                    if target <= close_month_start:
                        return get_value(owner_driver_id, "actual", target)
                    # value post-close == forecast output
                    if target in forecast_out:
                        return forecast_out.get(target)
                    if target in out:
                        return out.get(target)
                    try:
                        return get_value(owner_driver_id, "forecast", target)
                    except Exception:
                        return None

                # eff_series == "forecast" (or anything else): only forecast outputs exist post-close
                if target in forecast_out:
                    return forecast_out.get(target)
                if target in out:
                    return out.get(target)
                try:
                    return get_value(owner_driver_id, "forecast", target)
                except Exception:
                    return None
            return get_value(did_raw, eff_series, target)

        if t == "unary":
            op = str(node.get("op") or "").strip().lower()
            fv = _to_float(eval_node(node.get("expr") or {}, cur=cur))
            if fv is None:
                return None
            if op == "neg":
                return -fv
            raise ValueError(f"Unsupported unary op: {op}")

        if t == "binary":
            op = str(node.get("op") or "").strip().lower()
            pol = str(node.get("null_policy") or "coalesce_zero").strip().lower()
            lf = _to_float(eval_node(node.get("left") or {}, cur=cur))
            rf = _to_float(eval_node(node.get("right") or {}, cur=cur))
            if lf is None and rf is None:
                return None
            if pol == "propagate_null":
                if lf is None or rf is None:
                    return None
                if op == "div":
                    return None if rf == 0 else lf / rf
                if op == "add":
                    return lf + rf
                if op == "sub":
                    return lf - rf
                if op == "mul":
                    return lf * rf
                raise ValueError(f"Unsupported binary op: {op}")
            lz = lf if lf is not None else 0.0
            rz = rf if rf is not None else 0.0
            if op == "add":
                return lz + rz
            if op == "sub":
                return lz - rz
            if op == "mul":
                return lz * rz
            if op == "div":
                return None if rz == 0 else lz / rz
            raise ValueError(f"Unsupported binary op: {op}")

        if t == "func":
            name = str(node.get("name") or "").strip()
            args_eval = [eval_node(a or {}, cur=cur) for a in (node.get("args") or [])]
            if name == "abs":
                if len(args_eval) != 1:
                    raise ValueError("abs requires exactly 1 arg")
                v = _to_float(args_eval[0])
                return None if v is None else abs(v)
            if name == "round":
                if len(args_eval) not in (1, 2):
                    raise ValueError("round requires 1 or 2 args")
                v = _to_float(args_eval[0])
                if v is None:
                    return None
                if len(args_eval) == 1:
                    return float(round(v))
                d = _to_float(args_eval[1])
                return float(round(v, int(d))) if d is not None else float(round(v))
            if name == "coalesce":
                for v in args_eval:
                    if v is not None:
                        fv = _to_float(v)
                        return fv if fv is not None else v
                return None
            if name == "safe_divide":
                if len(args_eval) != 2:
                    raise ValueError("safe_divide requires exactly 2 args")
                a = _to_float(args_eval[0])
                b = _to_float(args_eval[1])
                # BigQuery SAFE_DIVIDE semantics: NULL if missing or denom=0
                if a is None or b is None or b == 0:
                    return None
                return a / b
            if name == "eq":
                if len(args_eval) != 2:
                    raise ValueError("eq requires exactly 2 args")
                a, b = args_eval[0], args_eval[1]
                if a is None or b is None:
                    return None
                return bool(a == b)
            if name == "if":
                if len(args_eval) != 3:
                    raise ValueError("if requires exactly 3 args")
                return args_eval[1] if _truthy(args_eval[0]) else args_eval[2]
            if name in {"thisMonth", "this_month"}:
                if args_eval:
                    raise ValueError("thisMonth/this_month does not accept args")
                return cur
            if name == "date":
                if len(args_eval) != 1:
                    raise ValueError("date requires exactly 1 arg")
                v = args_eval[0]
                if isinstance(v, date):
                    return month_start(v)
                if isinstance(v, str):
                    return parse_period_start(v)
                return None
            raise ValueError(f"Unsupported func: {name}")

        if t == "measure":
            raise ValueError("measure node cannot be evaluated by the expression engine")
        raise ValueError(f"Unknown AST node type: {t}")

    for p in ordered:
        if m == "actual" and p > close_month_start:
            out[p] = None
            continue
        if m == "forecast" and p <= close_month_start:
            out[p] = None
            continue
        if p in overrides_norm:
            # What-if: this month is fixed; downstream self-refs read it from `out`/`forecast_out`.
            out[p] = overrides_norm[p]
        else:
            v = eval_node(ast, cur=p)
            fv = _to_float(v)
            out[p] = fv if fv is not None and math.isfinite(fv) else None
        if p in adjust_norm and p not in overrides_norm:
            # Transform the just-computed (rolled) value, then store it back so the NEXT month's self-ref
            # compounds onto the ADJUSTED value — a % over a range stacks month over month instead of every
            # month flattening to base×factor. A month FIXED by period_overrides is left untouched here
            # (period_overrides wins, per the contract): a fixed value stays fixed and rolls forward as-is.
            adj_kind, adj_val = adjust_norm[p]
            base_v = out[p]
            if adj_kind in ("fixed", "set"):
                adj_out: Optional[float] = adj_val
            elif base_v is None:
                adj_out = None
            elif adj_kind == "delta":
                adj_out = base_v + adj_val
            else:  # percent / pct
                adj_out = base_v * (1.0 + adj_val / 100.0)
            if adj_out is not None and math.isfinite(adj_out):
                out[p] = adj_out
        if m in {"forecast", "value"} and p > close_month_start:
            forecast_out[p] = out[p]

    return out
