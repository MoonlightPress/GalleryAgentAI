
from pathlib import Path
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python project_file_finder.py <name-part>")
        return

    needle = sys.argv[1].lower()
    matches = []

    for path in Path(".").rglob("*"):
        if "__pycache__" in str(path):
            continue
        if needle in path.name.lower():
            matches.append(path)

    if not matches:
        print("No matches.")
        return

    for path in matches:
        print(path)

if __name__ == "__main__":
    main()
