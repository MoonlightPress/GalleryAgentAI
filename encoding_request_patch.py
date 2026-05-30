
from pathlib import Path

TARGETS = [
    Path("web_verification_engine.py"),
    Path("application_page_crawler.py"),
]

PATCH_SNIPPETS = [
    (
        "r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)\n        return r.status_code, r.text, r.url, None",
        "r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)\n        r.encoding = r.apparent_encoding or r.encoding\n        return r.status_code, r.text, r.url, None",
    ),
    (
        "r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)\n        return r.status_code, r.url, r.text, None",
        "r = requests.get(url, timeout=15, headers=HEADERS, allow_redirects=True)\n        r.encoding = r.apparent_encoding or r.encoding\n        return r.status_code, r.url, r.text, None",
    ),
]

def main():
    patched = 0

    for path in TARGETS:
        if not path.exists():
            print(f"SKIP missing {path}")
            continue

        text = path.read_text(encoding="utf-8")
        old = text

        for before, after in PATCH_SNIPPETS:
            if before in text and after not in text:
                text = text.replace(before, after)

        if text != old:
            backup = path.with_suffix(path.suffix + ".before_encoding_patch")
            backup.write_text(old, encoding="utf-8")
            path.write_text(text, encoding="utf-8")
            patched += 1
            print(f"PATCHED {path}")
        else:
            print(f"NO CHANGE {path}")

    print(f"Encoding patch complete. Files patched: {patched}")

if __name__ == "__main__":
    main()
