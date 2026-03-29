import os
import json
import re
import requests
from bs4 import BeautifulSoup

MODELDIR="model"
LABELS={0:"Highly Sensational",1:"Leans Sensational",2:"Mixed Intent",3:"Mostly Professional",4:"Highly Professional"}
SCORES={0:15,1:35,2:55,3:75,4:90}

PROMPT="""You are a media neutrality analyst. You do NOT assess political leaning. You assess the INTENT of the writer based purely on language mechanics.

Return ONLY valid JSON with this exact structure and no extra text:
{
  "neutrality_score": <integer 0-100, where 100 is fully neutral/professional>,
  "verdict": "<one of: Highly Professional | Mostly Professional | Mixed Intent | Leans Sensational | Highly Sensational>",
  "writer_intent_summary": "<2-3 sentence assessment of the writer's apparent intent>",
  "sensational_flags": [
    { "phrase": "<exact phrase from article>", "reason": "<why it is sensational>" }
  ],
  "professional_markers": [
    { "phrase": "<exact phrase from article>", "reason": "<why it is professional>" }
  ],
  "sources_found": [
    { "name": "<source name or person cited>", "type": "<named expert | institution | study | unnamed | data>", "credibility": "<verified | unverified | anonymous>" }
  ],
  "language_breakdown": {
    "emotive_language_pct": <0-100>,
    "attributed_claims_pct": <0-100>,
    "absolute_claims_pct": <0-100>,
    "hedged_language_pct": <0-100>
  }
}

Sensational signals: ALL CAPS for emphasis, power verbs with no evidence (destroys, slams), loaded adjectives (shocking, explosive), unnamed sources stated as fact, absolute claims, fear-inducing framing.
Professional signals: named attribution, conditional language (may, suggests), attributed quotes, referenced studies, acknowledgment of uncertainty, balanced framing.
Return ONLY the JSON object."""

def local_model_available():
    return os.path.isdir(MODELDIR) and os.path.isfile(os.path.join(MODELDIR,"config.json"))

def analyse_with_model(text):
    from transformers import DistilBertTokenizer,DistilBertForSequenceClassification
    import torch
    tokenizer=DistilBertTokenizer.from_pretrained(MODELDIR)
    model=DistilBertForSequenceClassification.from_pretrained(MODELDIR)
    model.eval()
    inputs=tokenizer(text,return_tensors="pt",truncation=True,max_length=256,padding=True)
    with torch.no_grad():
        out=model(**inputs)
    idx=out.logits.argmax(-1).item()
    score=SCORES[idx]
    verdict=LABELS[idx]
    emotive=80 if idx<=1 else 20
    attributed=10 if idx<=1 else 70
    return {
        "neutrality_score":score,
        "verdict":verdict,
        "writer_intent_summary":f"Local model classified this article as {verdict.lower()} based on learned language patterns.",
        "sensational_flags":[],
        "professional_markers":[],
        "sources_found":[],
        "language_breakdown":{
            "emotive_language_pct":emotive,
            "attributed_claims_pct":attributed,
            "absolute_claims_pct":70 if idx<=1 else 15,
            "hedged_language_pct":5 if idx<=1 else 60,
        }
    }

def analyse_with_gemini(text):
    key=os.environ.get("GEMINI_API_KEY")
    if not key:
        print("\n  [!] GEMINI_API_KEY not set and no local model found.")
        return None
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    body={
        "system_instruction":{"parts":[{"text":PROMPT}]},
        "contents":[{"parts":[{"text":f"Analyse this article:\n\n{text}"}]}],
        "generationConfig":{"temperature":0.2}
    }
    try:
        res=requests.post(url,json=body,timeout=30)
        res.raise_for_status()
        raw=res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        clean=re.sub(r"```json|```","",raw).strip()
        return json.loads(clean)
    except requests.exceptions.ConnectionError:
        print("\n  [!] Connection failed.")
        return None
    except requests.exceptions.Timeout:
        print("\n  [!] Request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"\n  [!] HTTP error: {e}")
        return None
    except (json.JSONDecodeError,KeyError):
        print("\n  [!] Could not parse response.")
        return None
    except Exception as e:
        print(f"\n  [!] Error: {e}")
        return None

def analyse_text(text):
    if local_model_available():
        try:
            return analyse_with_model(text)
        except Exception as e:
            print(f"\n  [!] Local model error: {e}. Falling back to Gemini.")
    return analyse_with_gemini(text)

def analyse_url(url):
    try:
        headers={"User-Agent":"Mozilla/5.0 (compatible; NeutralityIndex/1.0)"}
        res=requests.get(url,headers=headers,timeout=10)
        res.raise_for_status()
        soup=BeautifulSoup(res.text,"html.parser")
        for tag in soup(["script","style","nav","footer","header","aside","form"]):
            tag.decompose()
        block=soup.find("article")
        paras=block.find_all("p") if block else soup.find_all("p")
        text=" ".join(p.get_text(separator=" ",strip=True) for p in paras)
        text=re.sub(r"\s+"," ",text).strip()
        if len(text.split())<50:
            return None,"Not enough text extracted. Try pasting manually."
        return text,None
    except requests.exceptions.ConnectionError:
        return None,"Connection failed. Check the URL."
    except requests.exceptions.Timeout:
        return None,"Request timed out."
    except requests.exceptions.HTTPError as e:
        return None,f"HTTP error: {e}"
    except Exception as e:
        return None,str(e)
