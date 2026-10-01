from pathlib import Path

from llm_eval import load_cases, run_eval


def fake_app(prompt: str) -> str:
    return {"Capital of Australia?": "Canberra", "Today as ISO date": "2026-10-01"}.get(prompt, "no")


report = run_eval(fake_app, load_cases(Path(__file__).with_name("cases.jsonl")))
print(report.summary())

