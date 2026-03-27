import sys
from cli import run_cli

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\n[!] Session ended. Goodbye.")
        sys.exit(0)
