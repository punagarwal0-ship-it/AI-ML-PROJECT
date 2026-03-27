# AI-ML-PROJECT
BYOP activity
# Neutrality Index — Python CLI

A command-line tool that rates news articles on professional vs sensational language.
No left. No right. Just language.

---

## What It Does

Paste any news article or give it a URL. The tool returns:

- **Neutrality Score (0–100)** — how professionally written the article is
- **Verdict** — one of five levels from Highly Professional to Highly Sensational
- **Writer Intent Summary** — plain English assessment of what the writer appears to be trying to do
- **Sensational Flags** — exact phrases flagged as manipulative, with reasons
- **Professional Markers** — exact phrases flagged as evidence-based, with reasons
- **Language Breakdown** — four percentage bars in the terminal
- **Source Audit** — every cited source tagged by type and credibility

All results are saved to a CSV file automatically.

---

## Setup

**1. Install dependencies**
```bash
pip install anthropic requests beautifulsoup4
```

**2. Set your API key**
```bash
# Mac / Linux
export ANTHROPIC_API_KEY=your_key_here

# Windows
set ANTHROPIC_API_KEY=your_key_here
```

**3. Run**
```bash
python main.py
```

---

## Menu Options

```
1. Analyse pasted article text     — paste text directly, type END when done
2. Analyse article from URL        — scrapes and analyses a live news page
3. View analysis history           — table of all past analyses, selectable for detail
4. Export history to CSV           — save a clean flat CSV of all scores
5. Clear history                   — deletes history.csv
6. Help                            — scoring guide inside the app
7. Exit
```

---

## Score Ranges

| Score   | Label          | Meaning                                              |
|---------|----------------|------------------------------------------------------|
| 75–100  | Professional   | Evidence-based, attributed, measured language        |
| 50–74   | Mixed          | Mix of professional and emotive language             |
| 30–49   | Sensational    | Primarily emotive, few sources, loaded language      |
| 0–29    | Propaganda     | Near-total manipulation, no attribution              |

---

## File Structure

```
main.py           Entry point — starts the CLI, handles Ctrl+C cleanly
cli.py            Menu routing and all user input handling
analyser.py       Anthropic API call + URL scraping with BeautifulSoup
storage.py        CSV read, write, export, and clear
display.py        All terminal output — banners, bars, tables, errors
requirements.txt  Pinned dependencies
history.csv       Auto-created on first analysis, stores all results
```

---

## How the Score Is Produced

The analysis is done by Claude (claude-sonnet-4-20250514) using a system prompt that defines sensational and professional signals explicitly. The model returns structured JSON — the Python code just parses and displays it.

**Sensational signals the model looks for:**
ALL CAPS for emphasis, loaded verbs (destroys, slams, obliterates), unnamed sources stated as fact, absolute claims with no evidence, exclamation marks for drama, fear-inducing framing.

**Professional signals the model looks for:**
Named attribution (according to Dr. X), conditional language (may, suggests, appears), cited studies or data, attributed quotes, acknowledgment of uncertainty, balanced framing.

---

## Limitations

- Assesses language quality, not factual accuracy. A well-written false article will score highly.
- Source credibility is structural — named means verified, unnamed means anonymous. It does not independently confirm quotes.
- Articles under 50 words are rejected as too short for reliable percentage breakdowns.

---

## Requirements

- Python 3.8+
- An Anthropic API key (get one at console.anthropic.com)
