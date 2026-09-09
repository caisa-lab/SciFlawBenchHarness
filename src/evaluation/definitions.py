import json
import re

from core.registry import Registry
from evaluation.base import VerificationResult

verifier_registry = Registry("verifiers")


@verifier_registry.register("content:contains_str")
def contains_str(got: str, expected: str, case_sensitive: bool = False) -> VerificationResult:
    passed = expected in got if case_sensitive else expected.lower() in got.lower()
    return VerificationResult(passed=passed, details=f"Got: {got} Expected: {expected}")


@verifier_registry.register("content:exact_str_match")
def exact_str_match(got: str, expected: str, case_sensitive: bool = False) -> VerificationResult:
    passed = expected.strip() == got.strip() if case_sensitive else expected.strip().lower() == got.strip().lower()
    return VerificationResult(passed=passed, details=f"Got: {got} Expected: {expected}")


@verifier_registry.register("content:numeric_match")
def single_numeric_match(got: str, expected: str, tol: float = 0.0, index: int = -1) -> VerificationResult:
    matches = re.findall(r"-?\d+\.?\d*", got)
    if not matches:
        return VerificationResult(passed=False, details=f"No numeric types included in answer - Got: {got}")
    try:
        got_val = float(matches[index])
    except IndexError:
        return VerificationResult(passed=False, details=f"Index {index} out of range for expected: {expected} and \
                                  received strings: {got}")
    try:
        expected_val = float(expected)
    except ValueError:
        return VerificationResult(passed=False, details=f"Expected value: {expected} is not a numeric type")

    passed = abs(got_val - expected_val) <= tol
    return VerificationResult(passed=passed, details=f"Expected value: {expected_val} Got value: {got_val} diff \
            {abs(got_val - expected_val)} and tol: {tol}")


@verifier_registry.register("content:numeric_within_range")
def numeric_within_range(got: str, minimum: float, maximum: float, index: int = -1) -> VerificationResult:
    matches = re.findall(r"-?\d+\.?\d*", got)
    if not matches:
        return VerificationResult(passed=False, details=f"No numeric types included in answer - Got: {got}")
    try:
        got_val = float(matches[index])
    except IndexError:
        return VerificationResult(passed=False, details=f"Index {index} out of range in received string: {got}")

    passed = got_val <= maximum and got_val >= minimum
    return VerificationResult(passed=passed, details=f"Got value: {got_val} minimum: {minimum} and maximum: {maximum}")


@verifier_registry.register("content:paper_json_match")
def paper_list_match(
    got: str, expected: list[dict], match_mode: str = "all"
) -> VerificationResult:  # TODO: make match_mode an StrEnum or give literal type hints
    try:
        parsed = json.loads(got)
        papers = parsed.get("papers", [])
    except (json.JSONDecodeError, AttributeError):
        return VerificationResult(passed=False, details="could not parse 'papers' field from output")

    got_ids = {p.get("arxiv_id", "") for p in papers if isinstance(p, dict)}
    expected_ids = {p["arxiv_id"] for p in expected}

    if not expected_ids:
        passed = len(got_ids) == 0
        return VerificationResult(passed=passed, details=f"expected no papers, got {len(got_ids)}")

    matched = got_ids & expected_ids

    passed = expected_ids.issubset(got_ids) if match_mode == "all" else len(matched) > 0

    return VerificationResult(passed=passed, details=f"matched {len(matched)}/{len(expected_ids)} expected papers")


import math

_SCI_RE = re.compile(r"(?P<coeff>-?\d+\.?\d*)\s*(?:[eE](?P<exp1>[+-]?\d+)|[x×]\s*10\s*\^?\s*(?P<exp2>[+-]?\d+))")


def _extract_scientific_values(text: str) -> list[float]:
    """Finds values written as '6.022e23', '6.022E+23', '6.022 x 10^23',
    or '6.022 × 10^23' — in order of appearance."""
    values = []
    for m in _SCI_RE.finditer(text):
        coeff = float(m.group("coeff"))
        exp = m.group("exp1") or m.group("exp2")
        values.append(coeff * (10 ** int(exp)))
    return values


def _round_sig_figs(x: float, sig: int) -> float:
    if x == 0:
        return 0.0
    return round(x, -int(math.floor(math.log10(abs(x)))) + (sig - 1))


@verifier_registry.register("content:scientific_notation")
def scientific_notation_numeric(
    got: str,
    expected: str,
    rel_tol: float = 0.01,
    sig_figs: int | None = None,
    index: int = -1,
) -> VerificationResult:
    got_values = _extract_scientific_values(got)
    if not got_values:
        return VerificationResult(passed=False, details=f"No scientific-notation value found in output - Got: {got}")
    try:
        got_val = got_values[index]
    except IndexError:
        return VerificationResult(
            passed=False,
            details=f"Index {index} out of range for {len(got_values)} scientific-notation values found in: {got}",
        )

    expected_values = _extract_scientific_values(expected)
    if expected_values:
        expected_val = expected_values[0]
    else:
        try:
            expected_val = float(expected)  # allow plain-float expected values too, e.g. "6.022e23" written as-is
        except ValueError:
            return VerificationResult(passed=False, details=f"Expected value could not be parsed: {expected!r}")

    if sig_figs is not None:
        passed = _round_sig_figs(got_val, sig_figs) == _round_sig_figs(expected_val, sig_figs)
        details = f"Got: {got_val:.4e} Expected: {expected_val:.4e} (compared at {sig_figs} sig figs)"
    else:
        bound = abs(expected_val) * rel_tol
        diff = abs(got_val - expected_val)
        passed = diff <= bound
        details = f"Got: {got_val:.4e} Expected: {expected_val:.4e} diff: {diff:.4e} rel_tol: {rel_tol}"

    return VerificationResult(passed=passed, details=details)


@verifier_registry.register("format:json_output")
def json_output(got: str) -> VerificationResult:
    try:
        json.loads(got)
    except json.JSONDecodeError as e:
        return VerificationResult(passed=False, details=f"Failed to parse as json: {e}")
    return VerificationResult(passed=True, details="Valid Json provided")
