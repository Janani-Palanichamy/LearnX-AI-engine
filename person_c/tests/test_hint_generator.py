from person_c.hint_generator import generate_catalogue_hint, get_personalized_hint


def test_generate_catalogue_hint_returns_known_hint():
    hint = generate_catalogue_hint("MIS-04", "L1")
    assert isinstance(hint, str)
    assert len(hint) > 0


def test_get_personalized_hint_uses_catalogue_for_known_misconception():
    diagnosis = {
        "skill": "SKL-02",
        "misconception_id": "MIS-04",
        "misconception": "Infinite Loop",
        "confidence": 0.85
    }
    hint = get_personalized_hint("while True:\n    pass\n", diagnosis, "L1")
    assert hint["hint_source"] == "person_a_catalogue"
    assert hint["hint_level"] == "L1"
