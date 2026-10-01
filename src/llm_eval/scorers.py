import re
from typing import Callable, Optional


def exact(output: str, expected: str) -> bool:
    return output.strip().lower() == expected.strip().lower()


def contains(output: str, expected: str) -> bool:
    return expected.lower() in output.lower()


def regex(output: str, expected: str) -> bool:
    return re.search(expected, output) is not None


JUDGE_PROMPT = """You are grading an AI answer.
Rubric: {rubric}

Answer to grade:
{output}

Reply with exactly PASS or FAIL."""


def judge(output: str, expected: str, judge_llm: Optional[Callable[[str], str]] = None) -> bool:
    if judge_llm is None:
        raise ValueError("judge scorer requires judge_llm")
    verdict = judge_llm(JUDGE_PROMPT.format(rubric=expected, output=output))
    return verdict.strip().upper().startswith("PASS")


SCORERS = {"exact": exact, "contains": contains, "regex": regex}

