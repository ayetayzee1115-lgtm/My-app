# GhostPen (Style Learning Writing App)

GhostPen is a browser-based app that learns writing patterns from user-provided samples and generates prompts for creating original new chapters in a similar style.

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

1. Paste authorized style samples.
2. Enter what you want written (for example, a new chapter).
3. Set style alignment strength.
4. Tap **Generate Chapter Prompt**.
5. Copy the prompt into your preferred LLM.

## Files

- `index.html`: website UI
- `styles.css`: responsive styling for phones and desktop
- `app.js`: style analysis + prompt generation logic
- `style_writer.py`: CLI utility for profile + prompt generation

## Responsible use

- Use only samples that you own or are authorized to reuse.
- Keep outputs original and avoid impersonating real people.
- The app is designed for stylistic transfer, not plagiarism.
