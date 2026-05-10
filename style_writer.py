#!/usr/bin/env python3
"""StyleWriter: generate text in a target writing style from examples.

This tool builds a compact "style profile" from sample texts and then uses it
as constraints for generation.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
WORD_RE = re.compile(r"[A-Za-z']+")


@dataclass
class StyleProfile:
    avg_sentence_length: float
    avg_paragraph_sentences: float
    punctuation_rate: dict[str, float]
    top_words: list[str]
    rhetorical_patterns: list[str]
    tone: str


def split_sentences(text: str) -> list[str]:
    sentences = [s.strip() for s in SENTENCE_SPLIT.split(text.strip()) if s.strip()]
    return sentences or [text.strip()]


def split_words(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def infer_tone(text: str) -> str:
    lower = text.lower()
    if any(x in lower for x in ["!", "amazing", "incredible", "must", "now"]):
        return "energetic and persuasive"
    if any(x in lower for x in ["therefore", "however", "evidence", "analysis"]):
        return "analytical and formal"
    if any(x in lower for x in ["i", "we", "feel", "remember", "story"]):
        return "personal and reflective"
    return "neutral and clear"


def detect_patterns(text: str) -> list[str]:
    patterns: list[str] = []
    if re.search(r"\?\s+[A-Z]", text):
        patterns.append("frequent rhetorical questions")
    if re.search(r"\b(not only|both|either|neither)\b", text.lower()):
        patterns.append("paired constructions")
    if re.search(r"\b(first|second|finally)\b", text.lower()):
        patterns.append("sequenced transitions")
    if re.search(r"\bI\b", text):
        patterns.append("first-person voice")
    return patterns or ["direct declarative statements"]


def build_style_profile(samples: list[str]) -> StyleProfile:
    all_text = "\n\n".join(samples)
    sentence_lengths = []
    paragraph_sentence_counts = []

    paragraphs = [p for p in all_text.split("\n\n") if p.strip()]
    for paragraph in paragraphs:
        sents = split_sentences(paragraph)
        paragraph_sentence_counts.append(len(sents))
        sentence_lengths.extend(len(split_words(s)) for s in sents)

    words = split_words(all_text)
    word_freq: dict[str, int] = {}
    for w in words:
        if len(w) < 4:
            continue
        word_freq[w] = word_freq.get(w, 0) + 1

    top_words = [w for w, _ in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:12]]

    punct = {"comma": ",", "semicolon": ";", "dash": "—", "colon": ":"}
    punctuation_rate = {
        name: (all_text.count(mark) / max(1, len(words))) for name, mark in punct.items()
    }

    return StyleProfile(
        avg_sentence_length=round(mean(sentence_lengths), 2) if sentence_lengths else 12.0,
        avg_paragraph_sentences=round(mean(paragraph_sentence_counts), 2)
        if paragraph_sentence_counts
        else 3.0,
        punctuation_rate=punctuation_rate,
        top_words=top_words,
        rhetorical_patterns=detect_patterns(all_text),
        tone=infer_tone(all_text),
    )


def prompt_from_profile(profile: StyleProfile, task: str) -> str:
    return f"""
You are writing assistant. Produce text for this task:
{task}

Match this style profile closely:
- Tone: {profile.tone}
- Avg sentence length: {profile.avg_sentence_length} words
- Avg sentences per paragraph: {profile.avg_paragraph_sentences}
- Common words to reuse organically: {', '.join(profile.top_words[:8])}
- Rhetorical patterns: {', '.join(profile.rhetorical_patterns)}
- Punctuation tendencies (relative frequency): {profile.punctuation_rate}

Rules:
1) Keep semantic accuracy for the requested task.
2) Preserve style signals without copying phrases verbatim.
3) Return only the final text.
""".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a style profile and generation prompt.")
    parser.add_argument("--samples", nargs="+", required=True, help="Paths to writing samples.")
    parser.add_argument("--task", required=True, help="What to write.")
    parser.add_argument("--out", default="style_profile.json", help="Output JSON profile path.")
    args = parser.parse_args()

    samples = [Path(p).read_text(encoding="utf-8") for p in args.samples]
    profile = build_style_profile(samples)

    Path(args.out).write_text(json.dumps(asdict(profile), indent=2), encoding="utf-8")

    print("=== STYLE PROFILE ===")
    print(json.dumps(asdict(profile), indent=2))
    print("\n=== GENERATION PROMPT ===")
    print(prompt_from_profile(profile, args.task))


if __name__ == "__main__":
    main()
