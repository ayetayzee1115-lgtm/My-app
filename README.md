# StyleWriter

A compact AI helper that can mimic a target writing style from examples.

## What it does

`style_writer.py`:
1. Reads sample texts from a target style.
2. Extracts a **style profile** (sentence length, rhythm, punctuation habits, recurring words, tone).
3. Produces a ready-to-use **LLM prompt** to generate new text in that style.

> Note: no model can guarantee *perfectly identical* writing in every case. This tool gets very close by turning style into explicit constraints.

## Usage

```bash
python3 style_writer.py \
  --samples samples/author1.txt samples/author2.txt \
  --task "Write a 300-word product launch email" \
  --out profile.json
```

The command prints:
- a JSON style profile
- a generation prompt you can send to your preferred LLM

## Responsible use

- Use with permission when imitating a living person's distinctive style.
- Avoid deception, impersonation, and plagiarism.
- Keep factual correctness higher priority than style matching.
