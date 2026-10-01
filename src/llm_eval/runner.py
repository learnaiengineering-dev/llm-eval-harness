import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from .scorers import SCORERS, judge


@dataclass
class Case:
    id: str
    input: str
    expected: str
    scorer: str = "contains"


@dataclass
class CaseResult:
    case: Case
    output: str
    passed: bool
    error: Optional[str] = None


@dataclass
class Report:
    results: list[CaseResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        return sum(r.passed for r in self.results) / len(self.results) if self.results else 0.0

    @property
    def failures(self) -> list[CaseResult]:
        return [r for r in self.results if not r.passed]

    def summary(self) -> str:
        lines = [f"{len(self.results) - len(self.failures)}/{len(self.results)} passed ({self.pass_rate:.0%})"]
        for r in self.failures:
            why = r.error or f"got {r.output!r}, expected {r.case.expected!r} ({r.case.scorer})"
            lines.append(f"  FAIL {r.case.id}: {why}")
        return "\n".join(lines)


def load_cases(path: str | Path) -> list[Case]:
    cases = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            cases.append(Case(**json.loads(line)))
    return cases


def run_eval(
    app: Callable[[str], str],
    cases: list[Case],
    judge_llm: Optional[Callable[[str], str]] = None,
) -> Report:
    report = Report()
    for case in cases:
        try:
            output = app(case.input)
            if case.scorer == "judge":
                passed = judge(output, case.expected, judge_llm)
            elif case.scorer in SCORERS:
                passed = SCORERS[case.scorer](output, case.expected)
            else:
                raise ValueError(f"unknown scorer: {case.scorer}")
            report.results.append(CaseResult(case, output, passed))
        except Exception as exc:  # one broken case must not hide the rest
            report.results.append(CaseResult(case, "", False, f"{type(exc).__name__}: {exc}"))
    return report

