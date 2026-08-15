# F9 · Deck theme & generation workflow

**For:** the AI-generated slide deck (OpenAI image model → Gemini upscale).
**Constraint set:** Google Meet screen share · large Arabic examples · real matplotlib charts
composited in · formal engineering defence.

---

## ⚠️ Read this before generating anything

### 1. Rotate the two API keys

They were pasted in plaintext. Revoke and reissue:
- OpenAI → platform.openai.com/api-keys
- Gemini → Google AI Studio

Then put them in a **gitignored** `.env` at the repo root:

```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

and confirm `.env` is in `.gitignore` before anything else. Never paste them into a file that
`git add .` would catch.

### 2. The image model cannot render Arabic

This is the single biggest risk to your workflow. `gpt-image-1` and every current image model
**garble Arabic**: reversed letter order, broken ligatures, disconnected glyphs, invented characters.
Your deck's highest-value content is Arabic — «ما هي الأسماء الخمسة في اللغة العربية؟»،
«أب، أخ، حم، فو، ذو»، the three-card regulation comparison. A generated slide will render these as
nonsense, and an Arabic-speaking panel will see it instantly.

**So change the plan slightly:** generate the **visual layer** — background, illustration, layout
furniture, colour fields, icon work — and leave **empty labelled zones** where text goes. Then place
**all text as real text** on top, in PowerPoint or Canva. Latin text too: the model misspells that
as well, just less obviously.

You still get the look you want, and every word is correct and editable an hour before the defence.

### 3. Never let the model draw a chart

Same rule as F7. It will invent plausible bar heights. Composite the real PNGs.

---

## The palette — "Emerald & Teal on white"

White ground with green, as you wanted — but the green is pulled toward teal so it sits beside your
existing chart colours instead of fighting them.

| Role | Hex | Use |
|---|---|---|
| **Ground** | `#FFFFFF` | slide background, always |
| **Ink** | `#0F1E1C` | headings and body — near-black with a green bias, softer than pure black on a compressed video stream |
| **Muted** | `#5A6B67` | captions, secondary labels |
| **Primary — emerald** | `#0E6E5C` | grounded · correct · corpus · *ours* |
| **Secondary — teal** | `#1F6F8A` | system/technical elements — **this is your existing chart primary, unchanged** |
| **Warning — ochre** | `#B4622B` | hallucinated · wrong · memory-based |
| **Rule** | `#DCE4E2` | dividers, borders, table lines |
| **Tint** | `#EAF3F0` | panel fills, highlighted table rows |
| **Gradient** | `#0E6E5C → #1F6F8A` | accents, the RQ band, the winning row |

**Why the gradient is emerald→teal and not green→purple.** Short hue travel reads as one family and
survives video compression. A green→purple sweep is a big hue jump that bands badly on Meet, and it
would clash with the muted teal/purple already inside your charts.

### Why ochre for "wrong" and not red

Green/red is the obvious good/bad pairing and it is the wrong choice here. Roughly 8% of men have
red-green colour deficiency; you have an engineering panel of unknown composition, on a video call
where compression degrades colour further. **Emerald vs ochre stays separable under both deuteranopia
and protanopia**, and it holds up after compression. It also reads as more serious — red/green is a
dashboard convention, not a thesis one.

### The semantic mapping — this is the theme's real job

Your content has one binary running through the whole talk. Encode it once and the panel learns it
without being told:

| Meaning | Colour | Where it appears |
|---|---|---|
| grounded / correct / from the corpus / ours | **emerald** | slide 5 upper fork · slide 12 pseudo-doc card · slide 16 CSQE · slide 17 winning row · slide 22 |
| hallucinated / wrong / from memory | **ochre** | slide 3 answer arrow · slide 5 lower fork · slide 15 generated names |
| neutral system / technical | **teal** | pipeline boxes, diagrams, chart primary |
| baseline / before / prior work | **grey** | baseline rows, "no QE" bars, the empty Arabic bookshelf |

By slide 15 the panel already knows ochre means *the machine made this up*. That is worth more than
any label.

---

## Typography

| | Face | Notes |
|---|---|---|
| **Arabic** | **IBM Plex Sans Arabic**, or Cairo | Modern, opens well at display size, pairs with a Latin sans. Set Arabic **20–30% larger** than the Latin beside it — Arabic needs more optical size for the same legibility. |
| **Latin** | **Inter**, or Segoe UI | Clean, wide language coverage, renders well compressed |
| **Numbers** | Latin face, **tabular figures** | Every metric on every slide must align in a column |

Do **not** use Times on slides. It is right for the thesis and wrong for a screen — thin strokes
disappear under video compression. The charts keep their serif; that visual difference actually helps
them read as *evidence* rather than decoration.

**Minimum sizes for Meet:** headline 40pt, body 22pt, caption 16pt, chart labels 14pt equivalent.
Nothing below 14.

---

## Reusable prompt preamble

Put this at the top of every slide prompt, then add the slide-specific description.

```
Design a single 16:9 presentation slide, 1920x1080, for a formal university
engineering thesis defence.

STYLE
Pure white background (#FFFFFF). Clean, modern, editorial. Generous whitespace.
Flat vector illustration — no photographs, no 3D renders, no drop shadows, no
glassmorphism, no stock-photo people.

COLOUR
Primary emerald #0E6E5C. Secondary teal #1F6F8A. Accent ochre #B4622B used only
for things that are wrong or hallucinated. Neutral grey #5A6B67 for secondary
elements, #DCE4E2 for rules and borders, #EAF3F0 for panel fills. Where a
gradient is used it runs emerald #0E6E5C to teal #1F6F8A only.

TEXT
Leave all text areas EMPTY as clean blank zones with correct proportions and
alignment. Do not render any letters, words, numbers, or labels of any kind.
Text will be overlaid afterwards.

LAYOUT
[slide-specific description goes here]
```

The **TEXT** paragraph is the important one and it must survive every edit. Without it the model
fills the slide with garbled pseudo-Arabic and misspelt English.

---

## Worked example — slide 5 (the bottleneck fork)

```
[preamble above]

LAYOUT
A single entry point on the left edge represented as a small rounded rectangle.
From it, two paths diverge and run horizontally to the right edge, splitting
into an upper and a lower track with clear vertical separation.

UPPER TRACK, drawn in emerald #0E6E5C: three evenly spaced document icons,
then an identical simple geometric icon representing a language model, then an
empty rounded panel at the right edge with a small check mark in its corner.

LOWER TRACK, drawn in ochre #B4622B: three evenly spaced document icons drawn
in the same style as the upper track, then THE SAME language-model icon at
identical size and identical neutral grey #5A6B67, then an empty rounded panel
at the right edge with a small cross mark in its corner.

The language-model icon must be visually identical on both tracks — same size,
same shape, same colour — because the point is that only the documents differ.
Leave a small empty caption zone between the two icons.

Behind both tracks, very faint at 12% opacity in grey, a four-box horizontal
pipeline diagram, with the second box slightly more visible than the others.

Leave empty text zones: a headline strip across the top, a one-line caption
under each track, and a short caption between the two model icons.
```

That is the shape every slide prompt should take: **geometry, colour, and empty text zones.** Never
ask it for words.

---

## Should the charts be restyled?

Your four deck charts — `fig_4_5_models_bar_v1`, `fig_4_5b_models_bar_bm25_v1`,
`fig_4_11_progression_v2_annot`, `fig_4_7_repetition_v1` — are currently Times serif on a light
ground with the muted thesis palette. Against a white modern slide they will look like they came from
a different document.

**Cheap fix, and I can do it:** a deck-only mplstyle that overrides font to a sans, sets a pure white
figure ground, and remaps the highlight colour to emerald `#0E6E5C` while leaving every data value
untouched. Rerun the four existing scripts against it and you get deck-native charts with identical
numbers. About twenty minutes.

**Leave them alone if:** you would rather the charts look like they were lifted straight from the
thesis. That is a legitimate choice for a defence — it signals the numbers are the thesis's numbers,
not something made for the slides.

My recommendation: **restyle them.** The one thing you cannot afford is a panel wondering whether the
slide numbers and the thesis numbers are the same numbers, and matching typography removes that
question faster than a caption does.

---

## Order of work

1. Rotate keys, create gitignored `.env`
2. Lock the palette above (or tell me what to change)
3. Restyle the four charts — 20 min, optional
4. Generate slide **visual layers** one at a time, text zones empty
5. Upscale via Gemini to 4K, 16:9
6. Overlay all text in PowerPoint or Canva
7. Composite the real chart PNGs
8. Export to PDF and present the PDF
