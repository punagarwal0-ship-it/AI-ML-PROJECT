import textwrap
import shutil

W=min(shutil.get_terminal_size().columns,90)
DIV="─"*W

def verdict_tag(score):
    if score>=75: return "PROFESSIONAL"
    if score>=50: return "MIXED"
    if score>=30: return "SENSATIONAL"
    return "PROPAGANDA"

def score_bar(score,width=40):
    n=int((score/100)*width)
    return f"[{'█'*n+'░'*(width-n)}] {score}/100"

def pct_bar(pct,width=20):
    n=int((pct/100)*width)
    return f"[{'█'*n+'░'*(width-n)}] {pct}%"

def print_banner():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║        NEUTRALITY  INDEX  v1.0       ║")
    print("  ║   Language · Intent · Sources        ║")
    print("  ╚══════════════════════════════════════╝")
    print("  No left. No right. Just language.\n")

def print_menu():
    print(DIV)
    print("  MAIN MENU\n")
    print("  1. Analyse pasted article text")
    print("  2. Analyse article from URL")
    print("  3. View analysis history")
    print("  4. Export history to CSV")
    print("  5. Clear history")
    print("  6. Help")
    print("  7. Exit\n")

def print_divider():
    print(f"\n{DIV}")

def print_result(result):
    score=result.get("neutrality_score",0)
    verdict=result.get("verdict","")
    summary=result.get("writer_intent_summary","")
    flags=result.get("sensational_flags",[])
    markers=result.get("professional_markers",[])
    sources=result.get("sources_found",[])
    bd=result.get("language_breakdown",{})
    print(f"\n{DIV}")
    print("  ANALYSIS RESULT")
    if result.get("timestamp"):
        print(f"  {result['timestamp']}")
    if result.get("source"):
        print(f"  Source: {result['source']}")
    print(DIV)
    print(f"\n  NEUTRALITY SCORE")
    print(f"  {score_bar(score)}")
    print(f"  Verdict: {verdict}  [{verdict_tag(score)}]\n")
    print("  WRITER INTENT")
    for line in textwrap.wrap(summary,width=W-4):
        print(f"  {line}")
    print()
    print("  LANGUAGE BREAKDOWN")
    print(f"  Emotive language    {pct_bar(bd.get('emotive_language_pct',0))}")
    print(f"  Attributed claims   {pct_bar(bd.get('attributed_claims_pct',0))}")
    print(f"  Absolute claims     {pct_bar(bd.get('absolute_claims_pct',0))}")
    print(f"  Hedged language     {pct_bar(bd.get('hedged_language_pct',0))}")
    print()
    if flags:
        print(f"  SENSATIONAL FLAGS ({len(flags)})")
        for f in flags:
            print(f"  ! \"{f.get('phrase','')}\"")
            for line in textwrap.wrap(f.get("reason",""),width=W-8):
                print(f"      {line}")
        print()
    if markers:
        print(f"  PROFESSIONAL MARKERS ({len(markers)})")
        for m in markers:
            print(f"  + \"{m.get('phrase','')}\"")
            for line in textwrap.wrap(m.get("reason",""),width=W-8):
                print(f"      {line}")
        print()
    if sources:
        print(f"  SOURCES FOUND ({len(sources)})")
        for s in sources:
            print(f"  • {s.get('name','')}  [{s.get('type','')}]  [{s.get('credibility','')}]")
        print()
    print(DIV)

def print_history_table(history):
    print(f"\n  HISTORY  ({len(history)} records)\n")
    print(f"  {'#':<4} {'Date':<20} {'Score':<7} {'Verdict':<22} {'Source'}")
    print(f"  {'─'*4} {'─'*19} {'─'*6} {'─'*21} {'─'*25}")
    for i,rec in enumerate(history,1):
        date=rec.get("timestamp","")[:16]
        score=rec.get("neutrality_score","")
        verdict=rec.get("verdict","")[:20]
        source=rec.get("source","")[:30]
        print(f"  {i:<4} {date:<20} {score:<7} {verdict:<22} {source}")

def print_help():
    print(f"\n{DIV}")
    print("  HELP\n")
    print("  Analyses news articles for professional vs sensational language.")
    print("  Does NOT measure political bias — measures WRITER INTENT.\n")
    print("  SCORE RANGES")
    print("  75-100  Professional   Evidence-based, attributed, measured language")
    print("  50- 74  Mixed          Some professional markers, some emotive language")
    print("  30- 49  Sensational    Primarily emotive, few sources, loaded language")
    print("   0- 29  Propaganda     Near-total manipulation, no attribution\n")
    print("  SETUP")
    print("  export GEMINI_API_KEY=your_key_here\n")
    print("  INSTALL")
    print("  pip install requests beautifulsoup4 pandas\n")
    print(DIV)

def print_error(msg):
    print(f"\n  [!] {msg}\n")

def print_success(msg):
    print(f"\n  [+] {msg}\n")
