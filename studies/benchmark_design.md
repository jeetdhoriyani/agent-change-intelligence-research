# Benchmark Design

## Unit of analysis

A historical repository change with a known base commit, patch, test suite, and observed regression-revealing tests.

## Required record

```yaml
repository: owner/project
base_commit: abc123
task: Fix cache invalidation after configuration update
ground_truth:
  modified_files:
    - src/cache.py
  relevant_tests:
    - tests/test_cache.py::test_config_invalidation
budgets:
  context_tokens: 20000
  test_runtime_seconds: 300
```

## Baselines

1. Full suite
2. Tests in changed directories
3. Name and path heuristics
4. Import-graph selection
5. Coverage-dependency selection
6. Candidate hybrid engine

## Primary metrics

- safety recall
- full-suite disagreement rate
- runtime reduction
- net time saved
- context precision and recall
- agent task success
