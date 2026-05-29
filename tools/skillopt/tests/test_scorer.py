from lib.scorer import match_pattern, parse_size_complexity


def test_match_pattern_substring():
    assert match_pattern("hello world", {"contains": "world"}) is True
    assert match_pattern("hello world", {"contains": "missing"}) is False


def test_match_pattern_regex():
    assert match_pattern("Size: M", {"regex": r"Size:\s*[XSML]+"}) is True
    assert match_pattern("Foo Size: huge bar", {"regex": r"Size:\s*[XSML]+"}) is False


def test_parse_size_complexity_from_output():
    text = """Task: Add a feature
Size: M
Complexity: medium
Confidence: high"""
    parsed = parse_size_complexity(text)
    assert parsed["size"] == "M"
    assert parsed["complexity"] == "medium"
    assert parsed["confidence"] == "high"


def test_parse_handles_dashed_size():
    text = "Size: XS-S\nComplexity: high"
    assert parse_size_complexity(text)["size"] == "XS-S"


def test_parse_missing_fields_returns_partial():
    text = "Some output without size or complexity tags"
    parsed = parse_size_complexity(text)
    assert "size" not in parsed
    assert "complexity" not in parsed
