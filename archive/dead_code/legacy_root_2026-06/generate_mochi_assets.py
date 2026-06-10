import os

os.makedirs("assets/mochi", exist_ok=True)

ASSETS = {
    "hero_cat.svg": """
<svg width="1200" height="260" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="28" fill="#fff3df"/>
<path d="M0 210 C220 160, 360 250, 520 190 C690 120, 850 210, 1200 145 L1200 260 L0 260 Z" fill="#e8f0dc"/>
<circle cx="930" cy="70" r="42" fill="#f6d9a8"/>
<rect x="80" y="120" width="210" height="75" rx="16" fill="#d8b98e"/>
<rect x="115" y="82" width="38" height="105" rx="8" fill="#b88c63"/>
<rect x="165" y="95" width="42" height="92" rx="8" fill="#8fae7e"/>
<rect x="218" y="75" width="35" height="112" rx="8" fill="#c9795d"/>
<ellipse cx="760" cy="170" rx="82" ry="35" fill="#d7b08c"/>
<circle cx="720" cy="118" r="42" fill="#5b5147"/>
<polygon points="690,88 705,50 724,88" fill="#5b5147"/>
<polygon points="735,88 755,50 765,94" fill="#5b5147"/>
<circle cx="706" cy="118" r="4" fill="#f6efe3"/>
<circle cx="735" cy="118" r="4" fill="#f6efe3"/>
<path d="M715 135 Q725 144 740 134" stroke="#f6efe3" stroke-width="3" fill="none"/>
<path d="M820 169 Q890 125 920 180" stroke="#5b5147" stroke-width="16" fill="none" stroke-linecap="round"/>
<text x="90" y="58" font-size="34" fill="#5f4e3f" font-family="Georgia">Mochi's Atelier</text>
<text x="92" y="92" font-size="17" fill="#7a6a56" font-family="Georgia">gentle opportunities, ready drafts, quiet momentum</text>
</svg>
""",
    "zines.svg": """
<svg width="420" height="120" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="20" fill="#fff6e8"/>
<rect x="35" y="44" width="72" height="42" rx="5" fill="#d76f5f"/>
<rect x="78" y="34" width="80" height="52" rx="5" fill="#88a978"/>
<rect x="130" y="50" width="76" height="36" rx="5" fill="#e1b96d"/>
<circle cx="315" cy="58" r="30" fill="#ead2b8"/>
<text x="40" y="28" font-size="18" fill="#5f4e3f" font-family="Georgia">Print / Zines</text>
</svg>
""",
    "cafe.svg": """
<svg width="420" height="120" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="20" fill="#f8f1df"/>
<ellipse cx="110" cy="70" rx="58" ry="18" fill="#caa57d"/>
<rect x="70" y="42" width="80" height="38" rx="14" fill="#dfe8ce"/>
<path d="M150 52 Q190 55 158 72" stroke="#b58c6e" stroke-width="8" fill="none"/>
<circle cx="105" cy="61" r="18" fill="#9fbd87"/>
<text x="38" y="28" font-size="18" fill="#5f4e3f" font-family="Georgia">Cafe Walls</text>
</svg>
""",
    "market.svg": """
<svg width="420" height="120" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="20" fill="#fff2ef"/>
<path d="M55 72 L95 35 L135 72 Z" fill="#d76f5f"/>
<path d="M135 72 L175 35 L215 72 Z" fill="#f2c46d"/>
<rect x="65" y="72" width="140" height="28" rx="6" fill="#b98c67"/>
<text x="38" y="28" font-size="18" fill="#5f4e3f" font-family="Georgia">Markets</text>
</svg>
""",
    "gallery.svg": """
<svg width="420" height="120" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="20" fill="#f6f2e9"/>
<rect x="60" y="35" width="80" height="58" rx="4" fill="#fffdf8" stroke="#bda98e" stroke-width="5"/>
<rect x="175" y="42" width="56" height="44" rx="4" fill="#fffdf8" stroke="#bda98e" stroke-width="5"/>
<circle cx="100" cy="65" r="17" fill="#94ad80"/>
<text x="38" y="28" font-size="18" fill="#5f4e3f" font-family="Georgia">Galleries</text>
</svg>
""",
    "residency.svg": """
<svg width="420" height="120" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" rx="20" fill="#eef5e8"/>
<rect x="60" y="55" width="95" height="44" rx="8" fill="#b88768"/>
<path d="M50 58 L108 25 L170 58 Z" fill="#8fae7e"/>
<rect x="95" y="72" width="25" height="27" fill="#fff4dc"/>
<path d="M230 88 C265 48, 310 48, 350 88" stroke="#b8c9a7" stroke-width="8" fill="none"/>
<text x="38" y="28" font-size="18" fill="#5f4e3f" font-family="Georgia">Residencies</text>
</svg>
"""
}

for name, svg in ASSETS.items():
    with open(f"assets/mochi/{name}", "w", encoding="utf-8") as f:
        f.write(svg.strip())

print("Created Mochi visual assets.")