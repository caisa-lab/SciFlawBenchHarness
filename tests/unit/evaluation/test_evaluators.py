from evaluation.base import run_check
from evaluation.definitions import verifier_registry

def test_basic_logic_contains_str():
    result = run_check(verifier_registry.get("content:contains_str"), "Hello", expected="hell", case_sensitive=False )
    assert result.passed

    result = run_check(verifier_registry.get("content:contains_str"), "Hello", expected="Hell", case_sensitive=True )
    assert result.passed

    result = run_check(verifier_registry.get("content:contains_str"), "Hello", expected="hell", case_sensitive=True )
    assert not result.passed

    result = run_check(verifier_registry.get("content:contains_str"), "Hello", expected="akl;wejklr;", case_sensitive=True )
    assert not result.passed
    

def test_basic_logic_exact_str_match():
    result = run_check(verifier_registry.get("content:exact_str_match"), "Hello", expected="hello", case_sensitive=False )
    assert result.passed

    result = run_check(verifier_registry.get("content:exact_str_match"), "Hello", expected="Hello", case_sensitive=True )
    assert result.passed

    result = run_check(verifier_registry.get("content:exact_str_match"), "Hello", expected="hello", case_sensitive=True )
    assert not result.passed

    result = run_check(verifier_registry.get("content:exact_str_match"), "Hello", expected="alkjdsf;", case_sensitive=True )
    assert not result.passed

def test_basic_logic_numeric_match():
    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="10", index=0)
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="11", index=0)
    assert not result.passed

    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="-19", index=1)
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="80" )
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="83", tol=6.0 )
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_match"), "10 -19 80", expected="83", tol=2.0 )
    assert not result.passed


def test_basic_logic_numeric_range():
    result = run_check(verifier_registry.get("content:numeric_within_range"), "10 -19 80", minimum=5, maximum=15, index=0)
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_within_range"), "10 -19 80", minimum=15, maximum=30, index=0)
    assert not result.passed

    result = run_check(verifier_registry.get("content:numeric_within_range"), "10 -19 80", minimum=-19, maximum=15, index=1)
    assert result.passed

    result = run_check(verifier_registry.get("content:numeric_within_range"), "10 -19 80", minimum=80, maximum=90)
    assert result.passed

def test_basic_logic_scientific_notation():
    result = run_check(verifier_registry.get("content:scientific_notation"), "1.0x10^1, -1.9e10 1.9", expected="1e1",index=0)
    assert result.passed

    result = run_check(verifier_registry.get("content:scientific_notation"), "1.0x10^2 -1.9x10^0 1.9", expected="-1.9e0", index=1)
    assert result.passed
    
    result = run_check(verifier_registry.get("content:scientific_notation"), "jakl;dsfjal;fds 1.38x10^4", expected="1.38e4")
    assert result.passed

    result = run_check(verifier_registry.get("content:scientific_notation"), "jakl;dsfjal;fds 1.38x10^4", expected="1.38e5")
    assert not result.passed

    result = run_check(verifier_registry.get("content:scientific_notation"), "jakl;dsfjal;fds 1.38 x 10^4", expected="1.38e4")
    assert result.passed

    result = run_check(verifier_registry.get("content:scientific_notation"), "jakl;dsfjal;fds 1.38e4", expected="1.38e4")
    assert result.passed

def test_basic_json_ouptut():
    result = run_check(verifier_registry.get("content:json_output"), "{}", expected={})
    assert result.passed

    result = run_check(verifier_registry.get("content:json_output"), "{\"number\": 1}", expected={'number': 1})
    assert result.passed

    result = run_check(verifier_registry.get("content:json_output"), "{\"number\": 1}", expected={'num': 1})
    assert not result.passed

    result = run_check(verifier_registry.get("content:json_output"), "{\"number\": 1}", expected={'number': 10})
    assert not result.passed


