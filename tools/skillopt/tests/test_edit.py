from lib.edit import apply_ops, EditError
from lib.types import EditOp
import pytest


SAMPLE_SKILL = """---
name: foo
description: test skill
---

# Foo

## Section A

Body of A.

## Section B

Body of B.
"""


def test_replace_section_body():
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="New body of A.", rationale="test")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "Body of A" not in result
    assert "New body of A." in result
    assert "Body of B." in result


def test_add_new_section_at_end():
    ops = [EditOp(kind="add", section_heading="## Section C",
                  payload="Body of C.", rationale="add")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section C" in result
    assert result.index("## Section C") > result.index("## Section B")


def test_delete_section():
    ops = [EditOp(kind="delete", section_heading="## Section A",
                  rationale="cut")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section A" not in result
    assert "Body of A" not in result
    assert "## Section B" in result


def test_frontmatter_preserved():
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="x", rationale="")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert result.startswith("---\nname: foo")
    assert "description: test skill" in result


def test_delete_nonexistent_section_raises():
    ops = [EditOp(kind="delete", section_heading="## Section Z",
                  rationale="")]
    with pytest.raises(EditError, match="not found"):
        apply_ops(SAMPLE_SKILL, ops)


def test_add_duplicate_section_raises():
    ops = [EditOp(kind="add", section_heading="## Section A",
                  payload="x", rationale="")]
    with pytest.raises(EditError, match="already exists"):
        apply_ops(SAMPLE_SKILL, ops)


def test_ops_applied_in_order():
    ops = [
        EditOp(kind="delete", section_heading="## Section A", rationale=""),
        EditOp(kind="add", section_heading="## Section A", payload="restored", rationale=""),
    ]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert "## Section A" in result
    assert "restored" in result
    assert "Body of A" not in result


def test_replace_strips_leading_heading_from_payload():
    """Optimizer sometimes includes the heading in the payload. Don't duplicate it."""
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="## Section A\n\nfresh body of A.", rationale="")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert result.count("## Section A") == 1
    assert "fresh body of A." in result


def test_add_strips_leading_heading_from_payload():
    ops = [EditOp(kind="add", section_heading="## Section C",
                  payload="## Section C\n\nC body here.", rationale="")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert result.count("## Section C") == 1
    assert "C body here." in result


def test_payload_without_heading_still_works():
    """Don't strip when payload doesn't start with the heading."""
    ops = [EditOp(kind="replace", section_heading="## Section A",
                  payload="Just body, no heading.", rationale="")]
    result = apply_ops(SAMPLE_SKILL, ops)
    assert result.count("## Section A") == 1
    assert "Just body, no heading." in result
