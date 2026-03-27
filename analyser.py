import os
import json
import re
import anthropic
import requests
from bs4 import BeautifulSoup

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

def analyse_text(text):
    key=os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("\n  [!] ANTHROPIC_API_KEY not set.")
        return None
    try:
        client=anthropic.Anthropic(api_key=key)
        msg=client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=PROMPT,
            messages=[{"role":"user","content":f"Analyse this article:\n\n{text}"}]
        )
        raw=msg.content[0].text.strip()
        clean=re.sub(r"```json|```","",raw).strip()
        return json.loads(clean)
    except anthropic.AuthenticationError:
        print("\n  [!] Invalid API key.")
        return None
    except anthropic.RateLimitError:
        print("\n  [!] Rate limit hit. Wait and try again.")
        return None
    except json.JSONDecodeError:
        print("\n  [!] Could not parse response. Try again.")
        return None
    except Exception as e:
        print(f"\n  [!] Error: {e}")
        return None

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



