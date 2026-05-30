
import re
import unicodedata

WINDOWS_FORBIDDEN = r'<>:"/\\|?*'


def safe_filename(value, fallback="untitled", max_len=90, max_length=None):
    """
    Windows-safe filename helper.

    Supports both:
    - max_len
    - max_length

    This is intentional so older scripts do not crash.
    """

    if max_length is not None:
        max_len = max_length

    if value is None:
        value = fallback

    text = str(value).strip()

    if not text:
        text = fallback

    text = unicodedata.normalize("NFKC", text)

    for ch in WINDOWS_FORBIDDEN:
        text = text.replace(ch, "_")

    text = re.sub(r"[\x00-\x1f\x7f]", "", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" .")

    if not text:
        text = fallback

    if len(text) > max_len:
        text = text[:max_len].rstrip(" ._")

    return text or fallback


def safe_slug(value, fallback="untitled", max_len=90, max_length=None):
    if max_length is not None:
        max_len = max_length

    text = safe_filename(
        value,
        fallback=fallback,
        max_len=max_len,
    ).lower()

    text = re.sub(
        r"[^a-z0-9ぁ-んァ-ン一-龯ー]+",
        "_",
        text,
    )

    text = re.sub(r"_+", "_", text)
    text = text.strip("_")

    if not text:
        text = fallback

    return text[:max_len].strip("_") or fallback
