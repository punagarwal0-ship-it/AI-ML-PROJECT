import textwrap
from analyser import analyse_text, analyse_url
from storage import save_result, load_history, clear_history, export_history
from display import (
    print_banner, print_menu, print_result,
    print_history_table, print_help, print_error,
    print_success, print_divider
)

def run_cli():
    print_banner()
    while True:
        print_menu()
        choice=input("  Enter your choice: ").strip()
        if choice=="1":
            handle_paste()
        elif choice=="2":
            handle_url()
        elif choice=="3":
            handle_history()
        elif choice=="4":
            handle_export()
        elif choice=="5":
            handle_clear()
        elif choice=="6":
            print_help()
        elif choice=="7" or choice.lower() in ("exit","quit","q"):
            print("\n  Goodbye.\n")
            break
        else:
            print_error("Invalid choice. Enter a number from 1 to 7.")

def handle_paste():
    print_divider()
    print("  PASTE ARTICLE")
    print("  Paste your article below. Type END on a new line when done.\n")
    lines=[]
    while True:
        try:
            line=input()
        except EOFError:
            break
        if line.strip().upper()=="END":
            break
        lines.append(line)
    text="\n".join(lines).strip()
    if not text:
        print_error("No text entered.")
        return
    wc=len(text.split())
    if wc<50:
        print_error(f"Too short ({wc} words). Need at least 50.")
        return
    print(f"\n  [{wc} words] Analysing...")
    result=analyse_text(text)
    if result is None:
        print_error("Analysis failed. Check your API key.")
        return
    label=input("\n  Label this article (e.g. outlet name, optional): ").strip()
    result["source"]=label if label else "Unlabelled"
    result["input_type"]="pasted"
    save_result(result)
    print_result(result)

def handle_url():
    print_divider()
    print("  ANALYSE FROM URL\n")
    url=input("  Enter article URL: ").strip()
    if not url.startswith("http"):
        print_error("Invalid URL. Must start with http:// or https://")
        return
    print("\n  Fetching...")
    text,err=analyse_url(url)
    if err:
        print_error(f"Could not fetch: {err}")
        return
    wc=len(text.split())
    print(f"  [{wc} words extracted] Analysing...")
    result=analyse_text(text)
    if result is None:
        print_error("Analysis failed. Check your API key.")
        return
    result["source"]=url
    result["input_type"]="url"
    save_result(result)
    print_result(result)

def handle_history():
    print_divider()
    history=load_history()
    if not history:
        print("\n  No analyses saved yet.\n")
        return
    print_history_table(history)
    pick=input("\n  Enter row number for full details (or Enter to go back): ").strip()
    if pick.isdigit():
        idx=int(pick)-1
        if 0<=idx<len(history):
            print_result(history[idx])
        else:
            print_error("Row number out of range.")

def handle_export():
    print_divider()
    history=load_history()
    if not history:
        print("\n  No data to export.\n")
        return
    path=input("  Export filename (default: export.csv): ").strip()
    if not path:
        path="export.csv"
    if not path.endswith(".csv"):
        path+=".csv"
    export_history(history, path)
    print_success(f"Exported {len(history)} records to {path}")

def handle_clear():
    print_divider()
    confirm=input("  This deletes all saved analyses. Type YES to confirm: ").strip()
    if confirm=="YES":
        clear_history()
        print_success("History cleared.")
    else:
        print("  Cancelled.")


