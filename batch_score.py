import pandas as pd
import time
import os
import sys
from analyser import analyse_text
from storage import save_result

FILE="News_Category_Dataset.csv"
LIMIT=500
DELAY=10

def load_articles():
    if not os.path.isfile(FILE):
        print(f"[!] {FILE} not found in current folder.")
        sys.exit(1)
    df=pd.read_csv(FILE)
    possible=["short_description","headline","abstract","body","text","content","article"]
    col=next((c for c in possible if c in df.columns),None)
    if col is None:
        print(f"[!] Could not find text column. Columns found: {list(df.columns)}")
        sys.exit(1)
    print(f"[+] Using column: {col}")
    articles=df[col].dropna().astype(str).tolist()
    articles=[a for a in articles if len(a.split())>=50]
    return articles

def run():
    if not os.environ.get("GEMINI_API_KEY"):
        print("[!] GEMINI_API_KEY not set.")
        sys.exit(1)
    articles=load_articles()
    total=min(LIMIT,len(articles))
    print(f"[+] Scoring {total} articles. Estimated time: ~{total*DELAY//60} minutes.\n")
    done=0
    failed=0
    for i,text in enumerate(articles[:total]):
        print(f"  [{i+1}/{total}] Analysing...",end="\r")
        result=analyse_text(text)
        if result:
            result["source"]="kaggle"
            result["input_type"]="batch"
            save_result(result)
            done+=1
        else:
            failed+=1
        time.sleep(DELAY)
    print(f"\n[+] Done. {done} saved, {failed} failed.")
    print("[+] history.csv is ready for training.")

if __name__=="__main__":
    run()
