from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
def offline(event, args):
    if event.startswith("socket.") or event in {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn"}:
        raise RuntimeError("Demo offline: conexión o proceso externo rechazado")
sys.addaudithook(offline)
spec = importlib.util.spec_from_file_location("original_sample", HERE / "source" / "timeseries_engine.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
checks = []
def check(name, condition):
    assert condition, name
    checks.append({"case": name, "passed": True})
cases = [{'name': 'Crecimiento compuesto', 'growth_percent': 10, 'overrides': {}, 'result': [110.0, 121.0, 133.1, 146.41], 'passed': True}, {'name': 'Override febrero', 'growth_percent': 10, 'overrides': {'2026-02-01': 150}, 'result': [110.0, 150.0, 165.0, 181.5], 'passed': True}, {'name': 'Crecimiento cero', 'growth_percent': 0, 'overrides': {}, 'result': [100.0, 100.0, 100.0, 100.0], 'passed': True}]
from datetime import date
periods = [date(2026, month, 1) for month in range(1,5)]
close = date(2025,12,1)
for item in cases:
    formula = {"type":"binary", "op":"mul", "left":{"type":"ref", "driver_id":"self", "offset_months":-1, "series":"actual"}, "right":{"type":"const", "value":1+item["growth_percent"]/100}}
    result = module.compute_expression_series_monthly(formula, periods=periods, owner_driver_id="revenue", mode="forecast", close_month_start=close, get_value=lambda _id,_mode,period:100.0 if period==close else None, period_overrides=item["overrides"])
    actual = [round(result[p],4) for p in periods]
    check(item["name"], actual == item["result"])
print(json.dumps({"checks": checks, "passed": len(checks), "network": "forbidden"}, ensure_ascii=False))
