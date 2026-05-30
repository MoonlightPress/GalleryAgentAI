
from pathlib import Path

def main():
    print("\nSAFE FILENAME AUDIT")
    print("=" * 70)

    local_defs = []
    calls = []

    for path in Path(".").rglob("*.py"):
        if "__pycache__" in str(path):
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        if "def safe_filename" in text or "def safe_slug" in text:
            local_defs.append(str(path))

        if "safe_filename(" in text or "safe_slug(" in text:
            calls.append(str(path))

    print("\nFiles defining safe filename helpers:")
    for item in local_defs:
        print("-", item)

    print("\nFiles calling safe filename helpers:")
    for item in calls:
        print("-", item)

    print("\nExpected:")
    print("- utils_filename.py should define the helpers.")
    print("- other files should import from utils_filename.py, not define their own.")


if __name__ == "__main__":
    main()
