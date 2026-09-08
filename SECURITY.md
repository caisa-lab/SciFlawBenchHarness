# Security Policy

## What this project is

This is a benchmark harness for running LLM agents (via `smolagents`) against a
set of tasks, across multiple model providers, with tool access (web search,
code execution, file download/reading, etc.). It is a research/evaluation
tool, not a hardened multi-tenant service. Treat it accordingly: run it in an
environment you control, against models and task sources you trust, unless
you've deliberately hardened the pieces called out below.

## Known, inherent risk surfaces

These are architectural properties of the harness, not bugs — worth
understanding before you point this at untrusted input of any kind.

- **Model-generated code execution is not sandboxed by default.**
  `CodeAgent` executes model-generated Python via smolagents'
  `LocalPythonExecutor`, which smolagents itself documents as *not* a
  security boundary — its restrictions can be bypassed. Task subprocess
  isolation (separate OS process per task) limits blast radius but does
  **not** make arbitrary code execution safe. If you plan to run this
  against untrusted task definitions or allow a model to generate code with
  broader system access, use a real sandbox (e.g. smolagents' E2B or Docker
  executor) instead of the local executor.
- **Tools that fetch external content** (web search, webpage visiting, PDF/
  document download) fetch and parse content from arbitrary URLs a model
  chooses to visit, including ones surfaced by search results. Downloaded
  files are constrained to a per-task scratch directory with size/time
  limits, but the content itself (page text, PDF contents) is untrusted and
  flows back into the model's context.
- **The calculator tool executes user/model-supplied expressions** via
  `sympy` in a subprocess with CPU, memory, and wall-clock limits
  (`resource.setrlimit` + `subprocess.run(timeout=...)`). These limits
  bound resource exhaustion; they do not make the expression evaluator a
  general-purpose sandbox.
- **API keys and secrets are read from environment variables only** and are
  never written to task/run config files, logs, or trace output. Config
  files reference the *name* of an environment variable (`api_key_env`),
  never a key value. If you find a code path that logs, serializes, or
  otherwise persists a resolved secret value, that's a vulnerability — see
  below.
- **Multiprocessing uses the `spawn` start method** specifically to avoid
  fork-related deadlocks from inherited locks in imported libraries; each
  task subprocess is independently constructed with no shared memory with
  the parent or sibling tasks.

## Reporting a vulnerability

If you find a security issue in the harness itself — a secret leaking into
logs, a path-traversal in a tool's file handling, a way for task/model output
to escape its intended sandboxing/containment, or similar — please report it
privately rather than opening a public issue:

- Open a private report via GitHub's **Security Advisories** tab on this
  repository ("Report a vulnerability"), or
- Email: `<your contact address here>`

Please include: the affected file/component, a minimal reproduction (a task
definition or config that triggers it, where applicable), and the potential
impact as you see it.

## What's out of scope

- Vulnerabilities in third-party dependencies (`smolagents`, `litellm`,
  `sympy`, `markitdown`, model provider SDKs, etc.) — please report those
  upstream. We'll happily take a heads-up if one of them affects this
  project's usage of that dependency, but the fix belongs in that project.
- The general fact that model-generated code execution and untrusted tool
  content are inherently risky — that's a documented, known property of
  this architecture (see above), not something to report as a new finding,
  unless you've found a way to escalate it further than described here.
- Behavior of the LLMs/models being benchmarked themselves (e.g. a model
  producing harmful output as its *answer* to a task) — that's a model
  behavior question, not a harness security issue.

## Response expectations

This is a small/research project without a dedicated security team.
Reports will be acknowledged as promptly as possible on a best-effort basis;
there's no formal SLA. Fixes for genuine harness-level issues (secret
leakage, containment bypass, etc.) will be prioritized over feature work.
