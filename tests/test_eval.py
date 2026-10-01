from llm_eval import Case, run_eval
from llm_eval.scorers import contains, exact, regex


def test_scorers():
    assert exact(" Yes ", "yes")
    assert contains("It is Canberra.", "canberra")
    assert regex("2026-10-01", r"^\d{4}-\d{2}-\d{2}$")
    assert not regex("nope", r"\d+")


def test_pass_rate_and_failures():
    cases = [Case("a", "q1", "x"), Case("b", "q2", "y")]
    report = run_eval(lambda p: "x" if p == "q1" else "z", cases)
    assert report.pass_rate == 0.5
    assert [f.case.id for f in report.failures] == ["b"]
    assert "FAIL b" in report.summary()


def test_app_exception_is_captured():
    def app(_):
        raise RuntimeError("boom")

    report = run_eval(app, [Case("a", "q", "x")])
    assert report.failures[0].error.startswith("RuntimeError")


def test_judge_requires_llm_and_works():
    case = Case("j", "q", "mentions refunds", scorer="judge")
    assert run_eval(lambda _: "ans", [case]).failures  # no judge_llm -> error captured
    assert run_eval(lambda _: "ans", [case], judge_llm=lambda p: "PASS").pass_rate == 1.0
    assert run_eval(lambda _: "ans", [case], judge_llm=lambda p: "FAIL").pass_rate == 0.0


def test_unknown_scorer_is_error():
    assert run_eval(lambda _: "x", [Case("a", "q", "x", scorer="nope")]).failures
