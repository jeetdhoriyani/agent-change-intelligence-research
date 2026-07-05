# Inclusion Criteria

A project may be included when it satisfies at least one category:

1. **Direct RTS:** selects tests based on source changes or dependency observations.
2. **Affected-target tooling:** identifies build, package, or task targets affected by changes.
3. **Change-impact tooling:** computes dependencies, call graphs, or likely impact of a patch.
4. **Research prototype:** implements a published change-impact or test-selection method.
5. **Commercial reference:** materially shapes user expectations, even if not open source.

## Exclusions

- Generic coverage tools with no change-based selection capability.
- General CI systems with no affected-target or test-selection feature.
- Prompt-only agent wrappers.
- Unverifiable project claims.

## Status labels

- `candidate`: discovered but not fully reviewed
- `verified`: core fields checked against primary sources
- `reviewed`: scoring and evidence independently reviewed
- `excluded`: investigated but outside scope
