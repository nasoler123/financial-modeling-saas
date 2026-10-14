# Financial Modeling SaaS

A business assumption becomes a model, an interface and a reusable calculation.

[Run the sample](#run-the-sample) · [Architecture](docs/architecture.md) · [Design decisions](docs/decisions.md) · [Code tour](docs/code-tour.md) · [Español](docs/LEEME.md)

![Financial Modeling SaaS illustrated architecture](docs/overview.svg)

## The project

A financial model needs more than a generated formula: editable assumptions, periods, actual versus forecast values, dependencies, overrides and an interface that preserves the meaning of the calculation.

**My work.** I built a financial modeling product with editable drivers, budget grids and dashboards, a formula parser and backend execution, and then adapted the same capabilities to a Google Sheets sidebar. I led the product and technical construction, using AI-assisted development alongside integration and verification.

**Period.** 2025–July 2026; a previous product generation.

**Project outcome.** The proprietary frontend was built but did not acquire customers. It remains evidence of product and engineering work.

## What you can inspect here

This repository runs the original monthly AST evaluator. React components, dependency compilation and the Sheets adapter are selected excerpts. It does not boot the original SaaS frontend or connect a Google account.

| Entry | What to look at |
|---|---|
| [timeseries_engine.py](source/timeseries_engine.py) | Original executable component |
| [demo.py](demo.py) | Synthetic fixtures and 3 checked behaviors |
| [Architecture](docs/architecture.md) | The wider system and the sample boundary |
| [Design decisions](docs/decisions.md) | Tradeoffs with source links |
| [Code tour](docs/code-tour.md) | 8 selected excerpts from the wider construction |
| [Provenance](provenance.json) | Original paths, commits, hashes and documented redactions |

## Run the sample

Requires **Python 3.10+**, with no package installation or account setup.

```sh
git clone https://github.com/nasoler123/financial-modeling-saas.git
cd financial-modeling-saas
python3 -I demo.py
python3 verify.py
```

The sample runs offline with synthetic data; it rejects socket operations and external subprocesses. `verify.py` checks the result receipt, source hash, local links, instruction parity and credential patterns. These checks cover the published sample rather than the full production system.

Expected observations:

- 10% monthly growth from 100 produces 110, 121, 133.10 and 146.41.
- Setting February to 150 produces 110, 150, 165 and 181.50.
- Zero growth keeps the series at 100.

[Recorded local results](verification.json).

## Stack in context

React · TypeScript · Python · AST / SQL · driver dependencies · Google Apps Script.

The stack describes the wider construction. The executable sample uses Python's standard library; the remaining integrations appear in the code tour.

## Related work

This case belongs to the evolution of **Chals AI**, from document automation and a financial product to agent tooling and managed data infrastructure. The cases overlap; they are not four separate companies.

[Invoice Automation](https://github.com/nasoler123/invoice-automation) · [AI Agent Harness](https://github.com/nasoler123/ai-agent-harness) · [Data Platform and MCP](https://github.com/nasoler123/data-platform-mcp)

[Ignacio Soler](https://github.com/nasoler123) · [LinkedIn](https://www.linkedin.com/in/ignacio-soler-esteban/)
