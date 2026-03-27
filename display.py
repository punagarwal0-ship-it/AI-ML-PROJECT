import textwrap
import shutil

W=min(shutil.get_terminal_size().columns,90)
DIV="─"*W

def verdict_tag(score):
    if score>=75: return "PROFESSIONAL"
    if score>=50: return "MIXED"
    if score>=30: return "SENSATIONAL"
    return "PROPAGANDA"
  
