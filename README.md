# GhostPen (Any-Style Writing Website)

GhostPen is a browser-based website that helps you generate high-fidelity prompts to mimic almost any writing style.

It runs on:
- iPhones/iPads (iOS Safari)
- Mac/Windows/Linux computers (Chrome, Safari, Firefox, Edge)

## Run the website

From this folder:

```bash
python3 -m http.server 8000
```

Then open:
- `http://localhost:8000` on your computer, or
- from your iPhone on the same Wi-Fi, open `http://<your-computer-local-ip>:8000`

## How it works

1. Paste style samples.
2. Enter what you want written.
3. Set style strictness.
4. Tap **Generate Style-Clone Prompt**.
5. Copy the prompt into your preferred LLM.

## Files

- `index.html`: website UI
- `styles.css`: responsive styling for phones and desktop
- `app.js`: style analysis + prompt generation logic

## Note

No system can guarantee perfectly identical writing every time. GhostPen pushes similarity as far as possible while avoiding direct plagiarism.
