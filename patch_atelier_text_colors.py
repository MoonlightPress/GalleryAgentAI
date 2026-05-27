from pathlib import Path

path = Path("atelier_portal.py")
text = path.read_text(encoding="utf-8")

insert = """
/* HARD RESET TEXT COLORS */
html, body, .stApp, .block-container, p, span, div, label {
    color: #3f3027 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #3f3027 !important;
}

[data-testid="stMarkdownContainer"] {
    color: #3f3027 !important;
}

.stTabs [data-baseweb="tab"] {
    color: #6b5947 !important;
}

.stTabs [aria-selected="true"] {
    color: #b45f50 !important;
}

small, .caption, [data-testid="stCaptionContainer"] {
    color: #7a6a58 !important;
}

button, button p {
    color: #3f3027 !important;
}

"""

text = text.replace("<style>", "<style>\n" + insert)

path.write_text(text, encoding="utf-8")

print("Patched atelier_portal.py text colors.")