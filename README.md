# llm-eval-harness

A tiny, dependency-free **evaluation harness for LLM apps**. Define cases in JSONL, plug in any function that calls your model, score with exact/contains/regex/LLM-judge scorers and get a pass rate plus per-case failures. Built to be the first eval you actually run, and a CI gate you can trust.

> If you can't measure it, you can't ship changes to prompts, models or retrieval safely.

## Quickstart

```bash
git clone https://github.com/learnaiengineering-dev/llm-eval-harness
cd llm-eval-harness
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python examples/run_demo.py
```

## Define cases

`cases.jsonl`:

```json
{"id": "capital-au", "input": "Capital of Australia?", "expected": "Canberra", "scorer": "contains"}
{"id": "date-format", "input": "Today as ISO date", "expected": "^\\d{4}-\\d{2}-\\d{2}$", "scorer": "regex"}
```

## Run

```python
from llm_eval import load_cases, run_eval

def my_app(prompt: str) -> str:
    ...  # call your model or pipeline

report = run_eval(my_app, load_cases("cases.jsonl"))
print(report.summary())
assert report.pass_rate >= 0.9   # use as a CI gate
```

## Scorers

| Scorer | Passes when |
|---|---|
| `exact` | output equals expected (trimmed, case-insensitive) |
| `contains` | expected appears in output |
| `regex` | expected pattern matches output |
| `judge` | an LLM you supply returns `PASS` for a rubric (pass `judge_llm=`) |

## Good practice

- Start with 20 real failures from your logs, not synthetic cases.
- Keep deterministic scorers where possible; use judges only for fuzzy criteria, and spot-check them.
- Track pass rate over time and fail CI on regressions.

---

## Part of Learn AI Engineering

This repo is a free resource from [Learn AI Engineering](https://learnaiengineering.dev/?utm_source=github&utm_medium=repo&utm_campaign=llm-eval-harness) — *Build production AI systems.*

- Structured learning paths, labs and portfolio projects: [https://learnaiengineering.dev](https://learnaiengineering.dev/?utm_source=github&utm_medium=repo&utm_campaign=llm-eval-harness)
- Want the production-ready version (enterprise templates, deployment, evals, runbooks)? See the **FDE Toolkit** on the portal.
- More free repos: [github.com/learnaiengineering-dev](https://github.com/learnaiengineering-dev)

Licensed under MIT.
