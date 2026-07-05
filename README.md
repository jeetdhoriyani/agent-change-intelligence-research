# Agent Change Intelligence Research

Research-backed prototype for agent-native Python change-impact analysis and regression-test selection.

## Runnable prototype

The first executable version identifies Python files and function/class definitions changed since a Git reference.

```bash
python -m pip install -e '.[dev]'
changeintel --repo . --base HEAD~1
changeintel --repo . --base origin/main --format json
```

Python API:

```python
from changeintel import analyze_repository

result = analyze_repository(".", base_ref="HEAD~1")
for symbol in result.symbols:
    print(symbol.change_type, symbol.path, symbol.qualified_name)
```

Current scope:

- Python repositories
- Git diffs, including added, deleted, modified, and renamed files
- functions, async functions, classes, and qualified method names
- human-readable and versioned JSON output
- local-only execution with no telemetry

The next product increment will build a reverse import graph and rank affected pytest tests.

## Research questions

1. Which open-source projects perform change-impact analysis, affected-target analysis, or regression-test selection?
2. What technical and product gaps remain for coding-agent-native tooling?
3. How should usage, safety, adoption, and economic value be measured?

## Studies

### Study 1 — Open-source landscape

Build a reproducible database of direct competitors, adjacent build-system tools, dependency analyzers, academic prototypes, and commercial reference products.

### Study 2 — Use and value matrix

Track use cases, personas, execution environments, quality metrics, adoption signals, and privacy-preserving telemetry events.

## Initial hypothesis

The market gap is not test selection alone. It is an agent-native change-intelligence layer that returns affected code, relevant tests, risks, evidence, confidence, and bounded validation plans through stable Python, CLI, and MCP interfaces.

## Repository map

- `src/changeintel/`: executable Python package
- `tests/`: unit and integration tests
- `landscape/`: inclusion rules and competitor database
- `taxonomy/`: use-case matrix, metric definitions, and telemetry schema
- `studies/`: analysis scripts and benchmark design
- `datasets/`: candidate tools and benchmark repositories
- `reports/`: published findings
