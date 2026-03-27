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
