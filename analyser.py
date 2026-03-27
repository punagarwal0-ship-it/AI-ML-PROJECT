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
