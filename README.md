# AI-ML-PROJECT
BYOP activity

## Student Details
* **Name:** Puneet Agarwal
* **Registration Number:** 25bai11166
* **Branch:** First Year B.Tech – BTech CSE AI ML
 
# Neutrality Index

A command-line tool that analyses news articles and rates them on professional vs sensational language. It does not assess political leaning — it assesses writer intent through language mechanics.

---

## How It Works

The tool uses a locally trained DistilBERT model trained on a labelled news dataset (`history.csv`). Given an article, it classifies it into one of three categories:

- **Highly Sensational** — loaded language, unnamed sources, absolute claims
- **Mixed Intent** — mix of professional and emotive language
- **Mostly Professional** — attributed claims, conditional language, named sources

---

## Getting Started From This Repository

**Step 1 — Clone the repo**
```
git clone https://github.com/punagarwal0-ship-it/news_neutrality.git
cd news_neutrality
```

**Step 2 — Install dependencies**
```
pip install -r requirements.txt
```

**Step 3 — Train the model**
```
python train.py
```
This reads `history.csv` and fine-tunes DistilBERT locally. Creates a `model/` folder in your project directory. Takes 5–15 minutes depending on your machine.

**Step 4 — Run the app**
```
python main.py
```

---

## Menu Options

```
1. Analyse pasted article text     — paste text, type END when done
2. Analyse article from URL        — scrapes and analyses a live news page
3. View analysis history           — table of all past analyses
4. Export history to CSV           — saves a flat CSV of all scores
5. Clear history                   — resets history.csv
6. Help                            — scoring guide inside the app
7. Exit
```

---

## Score Ranges

| Score   | Label          | Meaning                                        |
|---------|----------------|------------------------------------------------|
| 70–100  | Professional   | Attributed, measured, evidence-based language  |
| 40–69   | Mixed          | Mix of professional and emotive language       |
| 0–39    | Sensational    | Loaded language, unnamed sources, fear tactics |

---

## File Structure

```
main.py           Entry point
cli.py            Menu routing and input handling
analyser.py       Local model inference and URL scraping
storage.py        CSV read, write, export, clear
display.py        All terminal output
train.py          Model training script
history.csv       Labelled dataset used for training
requirements.txt  Dependencies
model/            Created after running train.py — not committed to repo
```

---

## Notes

- The `model/` folder is excluded from the repository via `.gitignore`. Run `train.py` after cloning to generate it locally.
- `history.csv` is the labelled dataset the model trains on. It is included in the repo.
- Articles under 50 words are rejected as too short for reliable classification.

---

## Requirements

- Python 3.8+
- All dependencies listed in `requirements.txt`
