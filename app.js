const sentenceSplit = /(?<=[.!?])\s+/;
const wordRe = /[A-Za-z']+/g;

function splitWords(text) {
  return (text.match(wordRe) || []).map((w) => w.toLowerCase());
}

function splitSentences(text) {
  const out = text.trim().split(sentenceSplit).map((s) => s.trim()).filter(Boolean);
  return out.length ? out : [text.trim()];
}

function inferTone(text) {
  const lower = text.toLowerCase();
  if (["!", "amazing", "incredible", "must", "now"].some((x) => lower.includes(x))) return "energetic and persuasive";
  if (["therefore", "however", "evidence", "analysis"].some((x) => lower.includes(x))) return "analytical and formal";
  if ([" i ", " we ", "feel", "remember", "story"].some((x) => ` ${lower} `.includes(x))) return "personal and reflective";
  return "neutral and clear";
}

function detectPatterns(text) {
  const patterns = [];
  if (/\?\s+[A-Z]/.test(text)) patterns.push("frequent rhetorical questions");
  if (/\b(not only|both|either|neither)\b/i.test(text)) patterns.push("paired constructions");
  if (/\b(first|second|finally)\b/i.test(text)) patterns.push("sequenced transitions");
  if (/\bI\b/.test(text)) patterns.push("first-person voice");
  return patterns.length ? patterns : ["direct declarative statements"];
}

function buildProfile(samples) {
  const paragraphs = samples.split(/\n\n+/).filter((p) => p.trim());
  const sentenceLengths = [];
  const paraCounts = [];

  paragraphs.forEach((p) => {
    const sents = splitSentences(p);
    paraCounts.push(sents.length);
    sents.forEach((s) => sentenceLengths.push(splitWords(s).length));
  });

  const words = splitWords(samples);
  const freq = {};
  words.forEach((w) => {
    if (w.length >= 4) freq[w] = (freq[w] || 0) + 1;
  });

  const topWords = Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([w]) => w);

  const avg = (arr, fallback) => arr.length ? Number((arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2)) : fallback;

  return {
    avg_sentence_length: avg(sentenceLengths, 12),
    avg_paragraph_sentences: avg(paraCounts, 3),
    punctuation_rate: {
      comma: (samples.match(/,/g) || []).length / Math.max(1, words.length),
      semicolon: (samples.match(/;/g) || []).length / Math.max(1, words.length),
      dash: (samples.match(/—/g) || []).length / Math.max(1, words.length),
      colon: (samples.match(/:/g) || []).length / Math.max(1, words.length),
    },
    top_words: topWords,
    rhetorical_patterns: detectPatterns(samples),
    tone: inferTone(samples),
  };
}

function buildPrompt(profile, task, strictness) {
  return `You are a writing assistant. Produce original text for this task:\n${task}\n\nMatch this style profile closely:\n- Tone: ${profile.tone}\n- Avg sentence length: ${profile.avg_sentence_length} words\n- Avg sentences per paragraph: ${profile.avg_paragraph_sentences}\n- Common words to reuse organically: ${profile.top_words.slice(0, 8).join(", ")}\n- Rhetorical patterns: ${profile.rhetorical_patterns.join(", ")}\n- Punctuation tendencies (relative frequency): ${JSON.stringify(profile.punctuation_rate)}\n\nRules:\n1) Keep semantic accuracy for the requested task.\n2) Preserve style signals without copying phrases verbatim.\n3) Do not imitate real living authors or private individuals without consent; use only authorized samples.\n4) Keep output original and avoid references that imply identity with the source author.\n5) Return only the final text.\n6) Style strictness level: ${strictness}/10 (higher means stronger stylistic alignment).`;
}

document.getElementById("analyzeBtn").addEventListener("click", () => {
  const strictness = Number(document.getElementById("strictness").value || 8);
  const samples = document.getElementById("samples").value.trim();
  const task = document.getElementById("task").value.trim();
  if (!samples || !task) return alert("Please add both style samples and a task.");

  const profile = buildProfile(samples);
  document.getElementById("profileOut").textContent = JSON.stringify(profile, null, 2);
  document.getElementById("promptOut").value = buildPrompt(profile, task, strictness);
});

document.getElementById("copyBtn").addEventListener("click", async () => {
  const text = document.getElementById("promptOut").value;
  if (!text) return;
  await navigator.clipboard.writeText(text);
  alert("Prompt copied.");
});
