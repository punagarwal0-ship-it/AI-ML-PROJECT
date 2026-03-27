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
