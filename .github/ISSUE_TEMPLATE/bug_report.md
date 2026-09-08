---
name: Bug report
about: Something in the harness isn't working as expected
title: "[Bug]: "
labels: bug
assignees: ''
---

## Description
A clear, concise description of what went wrong.

## Steps to reproduce
1. Config used (run_config.json / relevant task JSONL snippet):
   ```json

   ```
2. Command run:
   ```bash

   ```
3. What happened:

## Expected behavior
What you expected to happen instead.

## Actual behavior / error output
```
paste the traceback, error message, or relevant log lines here
```

## Environment
- OS:
- Python version:
- smolagents version:
- Model provider/config (if relevant):
- Relevant packages (`pip freeze | grep -E "smolagents|litellm|pydantic"`):

## Relevant logs
If applicable, attach or paste relevant entries from `run_summary.jsonl`, a task's `results/{task_id}.json`, or the full event trace. Redact any API keys.

## Additional context
Anything else that might help — was this a single task or all tasks? Did it happen with a specific model/provider? Is it reproducible or intermittent?
