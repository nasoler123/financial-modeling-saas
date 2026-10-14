# Code tour

[Project](../README.md) · [Architecture](architecture.md) · [Design decisions](decisions.md)

## Start with executable code

1. Read [timeseries_engine.py](../source/timeseries_engine.py).
2. Inspect the synthetic inputs and assertions in [demo.py](../demo.py).
3. Compare [verification.json](../verification.json) with a fresh local run.

## Selected source from the wider system

| Component | Inspect | Form |
|---|---|---|
| React financial prototype | [Open excerpt](../evidence/E06.md) | Código |
| Registration UI state | [Open excerpt](../evidence/E07.md) | Código |
| Formula parser to AST | [Open excerpt](../evidence/E08.md) | Código |
| Tarjan dependency components | [Open excerpt](../evidence/E09.md) | Código |
| Editable budget grid state | [Open excerpt](../evidence/E10.md) | Código |
| Sheets adapter contract | [Open excerpt](../evidence/E19.md) | Contrato |
| Google identity exchange | [Open excerpt](../evidence/E20.md) | Código |
| Workspace IAM and Connected Sheets | [Open excerpt](../evidence/E21.md) | Contrato |

These excerpts retain original commit references. Incomplete classes, functions or integrations are presented as excerpts; the bounded executable module is separate. Redactions protect identifiers and are recorded in [provenance.json](../provenance.json).
