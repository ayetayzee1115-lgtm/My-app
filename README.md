# StyleMirror (iPhone + Computer App)

StyleMirror is a browser-based app that runs on:
- iPhones/iPads (iOS Safari)
- Mac/Windows/Linux computers (Chrome, Safari, Firefox, Edge)

It helps you create style-matching prompts from writing samples.

## Run the app

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
3. Tap **Generate Style Prompt**.
4. Copy the generated prompt into your preferred LLM.

## Files

- `index.html`: app UI
- `styles.css`: responsive styling for phones and desktop
- `app.js`: style analysis + prompt generation logic

## Note

No system can guarantee perfectly identical writing every time. This app maximizes similarity by extracting measurable style signals and turning them into constraints.
