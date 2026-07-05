# Privacy-Preserving Telemetry Schema

Remote telemetry should be disabled by default.

Never collect source code, file names, repository names, test names, diffs, prompts, command arguments, or environment variables.

## Core events

- `repository_index_completed`
- `diff_analysis_completed`
- `test_selection_completed`
- `selected_tests_executed`
- `full_suite_comparison_completed`
- `safe_fallback_triggered`
- `analysis_failed`
- `agent_tool_invoked`

## Common fields

```json
{
  "schema_version": 1,
  "tool_version": "0.1.0",
  "event": "test_selection_completed",
  "execution_mode": "cli",
  "repository_size_bucket": "10k-100k",
  "test_count_bucket": "1k-10k",
  "analysis_duration_bucket": "10-30s",
  "selected_fraction_bucket": "10%-25%",
  "safe_fallback_triggered": false
}
```

Exact repository identifiers are intentionally absent.
