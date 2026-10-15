# Financial Modeling SaaS

**A financial modeling product with editable assumptions and AI assistance**

*A Chals AI case study — built by Ignacio Soler.*

<a id="the-project"></a>

I built a financial planning product where users could edit business assumptions, calculate projections, compare budgets and explore scenarios through an integrated interface and chat. I later adapted the modeling capabilities to a Google Sheets sidebar.

I built this project end to end on my own, using AI tools for all programming. My work covered product definition, technical decisions, implementation, integration and validation.

[Watch the frontend](#watch-the-frontend) · [Explore the implementation](#explore-the-implementation) · [Run the component sample](#run-the-component-sample) · [Español](docs/LEEME.md)

## What I built

- A React and TypeScript interface with editable drivers, budget grids and dashboards.
- A formula parser and backend calculation engine for monthly projections and dependencies.
- A Google Sheets adaptation that brought the modeling capabilities into spreadsheets.

**Status:** Built during 2025–July 2026 as an earlier Chals AI product. The proprietary frontend did not acquire customers.

## Watch the frontend

Three guided frontend walkthroughs show scenario analysis, financial modeling and custom agent creation. They use synthetic data and scripted interactions from an earlier product generation.

### Analysis and what-if · 57s

https://github.com/user-attachments/assets/69282a3f-8c7d-4804-9ecb-95bc54f11465

[Open the full-screen demo](https://chalsai.com/demo.html?script=analysis-whatif&utm_source=github&utm_medium=portfolio&utm_campaign=financial-modeling-saas) · [Download MP4](docs/demos/analysis-whatif.mp4)

### Modeling and budget · 63s

https://github.com/user-attachments/assets/2d61e940-98b4-4818-83e8-7e2fbc52519e

[Open the full-screen demo](https://chalsai.com/demo.html?script=modeling-budget&utm_source=github&utm_medium=portfolio&utm_campaign=financial-modeling-saas) · [Download MP4](docs/demos/modeling-budget.mp4)


### Custom agent creation · 85s

https://github.com/user-attachments/assets/418023e3-7c39-4082-ba8b-140ba44dab4a

[Open the full-screen demo](https://chalsai.com/demo.html?script=custom-agents&utm_source=github&utm_medium=portfolio&utm_campaign=financial-modeling-saas) · [Download MP4](docs/demos/custom-agents.mp4)

[Media provenance](docs/demos/manifest.json).

![Financial Modeling SaaS illustrated architecture](docs/overview.svg)

## Explore the implementation

The runnable component contains the original monthly AST evaluator. Selected source excerpts document the wider work: React components, formula parsing, dependency compilation and the Google Sheets adapter.

| Entry | What to look at |
|---|---|
| [timeseries_engine.py](source/timeseries_engine.py) | Original executable component |
| [demo.py](demo.py) | Synthetic fixtures and 3 checked behaviors |
| [Architecture](docs/architecture.md) | The wider system and the sample boundary |
| [Design decisions](docs/decisions.md) | Tradeoffs with source links |
| [Code tour](docs/code-tour.md) | 8 selected excerpts from the wider construction |
| [Provenance](provenance.json) | Original paths, commits, hashes and documented redactions |

**Stack across the project:** React · TypeScript · Python · AST / SQL · Google Apps Script.

This public case study includes selected original code and an isolated runnable sample with synthetic data. Production integrations and customer data remain private. Original paths, commits, hashes and redactions are recorded in [provenance.json](provenance.json).

<a id="run-the-sample"></a>

## Run the component sample

Run the original monthly AST evaluator locally with synthetic data. Requires **Python 3.10+**, with no package installation or account setup.

```sh
git clone https://github.com/nasoler123/financial-modeling-saas.git
cd financial-modeling-saas
python3 -I demo.py
python3 verify.py
```

Expected observations:

- 10% monthly growth from 100 produces 110, 121, 133.10 and 146.41.
- Setting February to 150 produces 110, 150, 165 and 181.50.
- Zero growth keeps the series at 100.

The sample runs offline and rejects network connections and external subprocesses. `verify.py` checks local links, instruction parity, the source hash, credential patterns and the recorded results of the component checks. [Recorded local results](verification.json).

## More from Chals AI

These projects cover my work across business automation, financial software, AI agents and data infrastructure.

[Data Platform and MCP](https://github.com/nasoler123/data-platform-mcp) · [AI Agent Harness](https://github.com/nasoler123/ai-agent-harness) · [Invoice Automation](https://github.com/nasoler123/invoice-automation)

[Ignacio Soler](https://github.com/nasoler123) · [LinkedIn](https://www.linkedin.com/in/ignacio-soler-esteban/)
