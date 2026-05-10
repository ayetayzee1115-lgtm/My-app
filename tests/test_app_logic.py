import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from style_writer import build_style_profile, prompt_from_profile


def test_profile_has_expected_fields():
    profile = build_style_profile([
        "First, we test tone. However, structure matters.",
        "Finally, we verify repeated language and punctuation."
    ])
    assert profile.avg_sentence_length > 0
    assert profile.avg_paragraph_sentences > 0
    assert isinstance(profile.top_words, list)
    assert isinstance(profile.punctuation_rate, dict)


def test_prompt_includes_task_and_rules():
    profile = build_style_profile(["I remember the story. It was vivid."])
    prompt = prompt_from_profile(profile, "Write a short intro")
    assert "Write a short intro" in prompt
    assert "Rules:" in prompt
