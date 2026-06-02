import sys, os
sys.stdout.reconfigure(encoding='utf-8')

OUT = "C:/ScottStuff/GalleryAgentAI/frontend/public/assets/illustrations"
os.makedirs(OUT, exist_ok=True)

DEFS = """
  <defs>
    <filter id="wc" x="-15%" y="-15%" width="130%" height="130%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035 0.028"
                    numOctaves="4" seed="7" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="7"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="wash" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="soft" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <filter id="crisp" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.06 0.05"
                    numOctaves="3" seed="12" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="4"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>"""

def wrap(body, w=400, h=260):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
        f'{DEFS}\n{body}\n</svg>\n'
    )

def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {name}")


# ── 1. Zines & Print ──────────────────────────────────────────────────────────
save("zines_and_print.svg", wrap("""
  <ellipse cx="205" cy="145" rx="170" ry="105" fill="#e8c060" opacity="0.13" filter="url(#wash)"/>
  <ellipse cx="185" cy="155" rx="140" ry="85"  fill="#d4a050" opacity="0.10" filter="url(#wash)"/>

  <g filter="url(#wc)">
    <rect x="88"  y="162" width="225" height="30" rx="3" fill="#c49a52" opacity="0.80"
          transform="rotate(-5,200,177)"/>
    <rect x="88"  y="162" width="20"  height="30" rx="2" fill="#9a7838" opacity="0.88"
          transform="rotate(-5,200,177)"/>
    <rect x="107" y="162" width="206" height="2"  fill="#f5ead8" opacity="0.45"
          transform="rotate(-5,200,177)"/>
    <rect x="107" y="190" width="206" height="2"  fill="#f5ead8" opacity="0.45"
          transform="rotate(-5,200,177)"/>
  </g>

  <g filter="url(#wc)">
    <rect x="130" y="112" width="145" height="54" rx="3" fill="#d4897a" opacity="0.78"
          transform="rotate(3,202,139)"/>
    <rect x="130" y="112" width="16"  height="54" rx="2" fill="#b86a5a" opacity="0.85"
          transform="rotate(3,202,139)"/>
    <rect x="145" y="113" width="129" height="2"  fill="#f5ead8" opacity="0.45"
          transform="rotate(3,202,139)"/>
    <rect x="145" y="164" width="129" height="2"  fill="#f5ead8" opacity="0.45"
          transform="rotate(3,202,139)"/>
    <line x1="158" y1="128" x2="264" y2="128" stroke="#f5e8d0" stroke-width="1.5"
          opacity="0.35" transform="rotate(3,202,139)"/>
    <line x1="158" y1="138" x2="240" y2="138" stroke="#f5e8d0" stroke-width="1"
          opacity="0.28" transform="rotate(3,202,139)"/>
  </g>

  <g filter="url(#wc)">
    <rect x="152" y="80" width="108" height="36" rx="3" fill="#8aae8a" opacity="0.75"
          transform="rotate(-3,206,98)"/>
    <rect x="152" y="80" width="13"  height="36" rx="2" fill="#6a8e6a" opacity="0.85"
          transform="rotate(-3,206,98)"/>
    <rect x="164" y="81" width="95"  height="2"  fill="#f5ead8" opacity="0.40"
          transform="rotate(-3,206,98)"/>
    <rect x="164" y="114" width="95" height="2"  fill="#f5ead8" opacity="0.40"
          transform="rotate(-3,206,98)"/>
  </g>

  <g filter="url(#crisp)">
    <rect x="178" y="60" width="60" height="22" rx="2" fill="#f5e0c0" opacity="0.88"
          transform="rotate(7,208,71)"/>
    <rect x="178" y="60" width="7"  height="22" rx="1" fill="#e8c060" opacity="0.90"
          transform="rotate(7,208,71)"/>
  </g>
"""))


# ── 2. Galleries ──────────────────────────────────────────────────────────────
save("galleries.svg", wrap("""
  <ellipse cx="200" cy="148" rx="130" ry="100" fill="#f5d870" opacity="0.18" filter="url(#wash)"/>
  <ellipse cx="200" cy="160" rx="90"  ry="70"  fill="#f0c850" opacity="0.14" filter="url(#wash)"/>

  <g filter="url(#wc)">
    <rect x="100" y="68" width="42" height="140" rx="6" fill="#c8b898" opacity="0.70"/>
    <rect x="258" y="68" width="42" height="140" rx="6" fill="#c8b898" opacity="0.70"/>
    <path d="M100 120 Q100 50 200 50 Q300 50 300 120" fill="#c8b898" opacity="0.70"/>
    <path d="M142 120 Q142 78 200 72 Q258 78 258 120 L258 210 L142 210 Z"
          fill="#f5e8c0" opacity="0.72" filter="url(#soft)"/>
    <ellipse cx="200" cy="56" rx="14" ry="10" fill="#b8a888" opacity="0.75"/>
  </g>

  <ellipse cx="200" cy="155" rx="60" ry="65" fill="#f8e8a0" opacity="0.25" filter="url(#wash)"/>

  <g filter="url(#crisp)" opacity="0.55">
    <rect x="155" y="105" width="18" height="24" rx="1" fill="#d4a060"/>
    <rect x="227" y="108" width="16" height="20" rx="1" fill="#c8897a"/>
  </g>

  <ellipse cx="200" cy="208" rx="70" ry="8" fill="#b8a888" opacity="0.22" filter="url(#soft)"/>
"""))


# ── 3. Cafes ─────────────────────────────────────────────────────────────────
save("cafes.svg", wrap("""
  <ellipse cx="200" cy="150" rx="150" ry="100" fill="#d4a050" opacity="0.14" filter="url(#wash)"/>
  <ellipse cx="195" cy="160" rx="100" ry="70"  fill="#e8c060" opacity="0.11" filter="url(#wash)"/>

  <g filter="url(#wc)">
    <ellipse cx="200" cy="197" rx="72" ry="10" fill="#c8a878" opacity="0.72"/>
    <ellipse cx="200" cy="197" rx="50" ry="6"  fill="#b89858" opacity="0.50"/>
  </g>

  <g filter="url(#wc)">
    <path d="M148 145 L155 195 Q200 202 245 195 L252 145 Q200 138 148 145 Z"
          fill="#f0e0c0" opacity="0.82"/>
    <path d="M148 145 Q200 138 252 145" fill="none" stroke="#c8a878" stroke-width="2"
          opacity="0.60"/>
    <ellipse cx="200" cy="145" rx="52" ry="9" fill="#8c6030" opacity="0.72"/>
    <ellipse cx="200" cy="145" rx="38" ry="6" fill="#7a5028" opacity="0.55"/>
    <path d="M196 142 Q200 139 204 142 Q207 145 200 150 Q193 145 196 142Z"
          fill="#c89060" opacity="0.40"/>
  </g>

  <g filter="url(#wc)">
    <path d="M248 158 Q275 158 275 172 Q275 186 248 184"
          fill="none" stroke="#c8a878" stroke-width="8" stroke-linecap="round"
          opacity="0.70"/>
  </g>

  <g filter="url(#soft)" opacity="0.45">
    <path d="M185 138 Q180 122 185 108 Q190 94 185 80"
          fill="none" stroke="#c8b898" stroke-width="3" stroke-linecap="round"/>
    <path d="M200 136 Q196 118 200 104 Q204 90 200 76"
          fill="none" stroke="#c8b898" stroke-width="3" stroke-linecap="round"/>
    <path d="M215 138 Q220 122 215 108 Q210 94 215 80"
          fill="none" stroke="#c8b898" stroke-width="3" stroke-linecap="round"/>
  </g>

  <g filter="url(#crisp)" opacity="0.38">
    <rect x="110" y="80"  width="28" height="36" rx="2" fill="#d4a878"/>
    <rect x="260" y="90"  width="24" height="30" rx="2" fill="#c8897a"/>
  </g>
"""))


# ── 4. Open Calls ────────────────────────────────────────────────────────────
save("open_calls.svg", wrap("""
  <ellipse cx="200" cy="140" rx="160" ry="100" fill="#c8d4e8" opacity="0.13" filter="url(#wash)"/>
  <ellipse cx="210" cy="150" rx="120" ry="80"  fill="#e8d8a0" opacity="0.12" filter="url(#wash)"/>

  <g filter="url(#wc)">
    <rect x="85" y="110" width="230" height="150" rx="6" fill="#f0e4c8" opacity="0.80"/>
    <path d="M85 110 L200 68 L315 110" fill="#e8d0a0" opacity="0.78"/>
    <path d="M85 110 L200 68 L315 110 L200 165 Z" fill="#dcc890" opacity="0.55"/>
    <path d="M85 260 L200 175 L315 260" fill="none" stroke="#c8b060" stroke-width="1.5"
          opacity="0.30"/>
  </g>

  <g filter="url(#crisp)">
    <rect x="155" y="88" width="90" height="100" rx="4" fill="#fffcf0" opacity="0.92"/>
    <rect x="155" y="88" width="90" height="18"  rx="4" fill="#c49a52" opacity="0.80"/>
    <rect x="155" y="100" width="90" height="6"  fill="#c49a52" opacity="0.80"/>
    <g fill="#8c7050" opacity="0.55">
      <circle cx="170" cy="122" r="2.5"/><circle cx="185" cy="122" r="2.5"/>
      <circle cx="200" cy="122" r="2.5"/><circle cx="215" cy="122" r="2.5"/>
      <circle cx="230" cy="122" r="2.5"/>
      <circle cx="170" cy="136" r="2.5"/><circle cx="185" cy="136" r="2.5"/>
      <circle cx="215" cy="136" r="2.5"/><circle cx="230" cy="136" r="2.5"/>
      <circle cx="170" cy="150" r="2.5"/><circle cx="185" cy="150" r="2.5"/>
      <circle cx="200" cy="150" r="2.5"/><circle cx="215" cy="150" r="2.5"/>
      <circle cx="230" cy="150" r="2.5"/>
      <circle cx="170" cy="164" r="2.5"/><circle cx="185" cy="164" r="2.5"/>
      <circle cx="200" cy="164" r="2.5"/>
    </g>
    <circle cx="200" cy="136" r="8" fill="none" stroke="#d4685a" stroke-width="2.5"
            opacity="0.80"/>
    <circle cx="200" cy="136" r="3.5" fill="#d4685a" opacity="0.70"/>
  </g>
"""))


# ── 5. Residencies ────────────────────────────────────────────────────────────
save("watch_list.svg", wrap("""
  <ellipse cx="200" cy="145" rx="160" ry="105" fill="#8aae8a" opacity="0.13" filter="url(#wash)"/>
  <ellipse cx="205" cy="155" rx="120" ry="80"  fill="#c8d4b0" opacity="0.12" filter="url(#wash)"/>

  <g filter="url(#wc)">
    <rect x="130" y="130" width="140" height="110" rx="4" fill="#f0e4c8" opacity="0.82"/>
    <rect x="183" y="192" width="34"  height="48"  rx="3" fill="#c49a62" opacity="0.72"/>
    <circle cx="212" cy="218" r="3" fill="#9a7840" opacity="0.80"/>
    <rect x="142" y="148" width="32" height="28" rx="3" fill="#d8e8f0" opacity="0.78"/>
    <rect x="226" y="148" width="32" height="28" rx="3" fill="#d8e8f0" opacity="0.78"/>
    <rect x="143" y="149" width="30" height="26" rx="2" fill="#f8e890" opacity="0.35"/>
    <rect x="227" y="149" width="30" height="26" rx="2" fill="#f8e890" opacity="0.35"/>
    <line x1="158" y1="148" x2="158" y2="176" stroke="#c8b898" stroke-width="1.5" opacity="0.50"/>
    <line x1="142" y1="162" x2="174" y2="162" stroke="#c8b898" stroke-width="1.5" opacity="0.50"/>
    <line x1="242" y1="148" x2="242" y2="176" stroke="#c8b898" stroke-width="1.5" opacity="0.50"/>
    <line x1="226" y1="162" x2="258" y2="162" stroke="#c8b898" stroke-width="1.5" opacity="0.50"/>
  </g>

  <g filter="url(#wc)">
    <path d="M118 134 L200 68 L282 134 Z" fill="#c8a878" opacity="0.78"/>
    <rect x="228" y="78" width="22" height="42" rx="2" fill="#b89878" opacity="0.72"/>
    <rect x="225" y="76" width="28" height="8"  rx="2" fill="#c0a880" opacity="0.72"/>
    <path d="M239 74 Q234 60 239 48 Q244 36 239 24"
          fill="none" stroke="#c8b898" stroke-width="3" stroke-linecap="round"
          opacity="0.30" filter="url(#soft)"/>
  </g>

  <g filter="url(#crisp)" opacity="0.70">
    <ellipse cx="140" cy="238" rx="18" ry="14" fill="#7aae7a"/>
    <ellipse cx="118" cy="232" rx="12" ry="10" fill="#8abe8a" opacity="0.85"/>
    <ellipse cx="260" cy="238" rx="18" ry="14" fill="#7aae7a"/>
    <ellipse cx="282" cy="232" rx="12" ry="10" fill="#8abe8a" opacity="0.85"/>
    <ellipse cx="200" cy="240" rx="10" ry="7"  fill="#a8ce88" opacity="0.75"/>
    <circle cx="128" cy="222" r="5" fill="#f0c0a0" opacity="0.80"/>
    <circle cx="272" cy="224" r="5" fill="#f0d0b0" opacity="0.80"/>
    <circle cx="200" cy="233" r="4" fill="#f8e0b0" opacity="0.75"/>
  </g>

  <ellipse cx="200" cy="242" rx="88" ry="8" fill="#8a9878" opacity="0.18" filter="url(#soft)"/>
"""))


# ── 6. Immediate Best Moves — gold star burst ─────────────────────────────────
save("immediate_best_moves.svg", wrap("""
  <ellipse cx="200" cy="130" rx="140" ry="110" fill="#e8c040" opacity="0.20" filter="url(#wash)"/>
  <ellipse cx="200" cy="130" rx="90"  ry="70"  fill="#f0d050" opacity="0.16" filter="url(#wash)"/>

  <g filter="url(#soft)" opacity="0.35" stroke="#c8a030" stroke-linecap="round">
    <line x1="200" y1="20"  x2="200" y2="50"  stroke-width="3.5"/>
    <line x1="200" y1="210" x2="200" y2="240" stroke-width="3.5"/>
    <line x1="60"  y1="130" x2="90"  y2="130" stroke-width="3.5"/>
    <line x1="310" y1="130" x2="340" y2="130" stroke-width="3.5"/>
    <line x1="96"  y1="56"  x2="117" y2="77"  stroke-width="2.5"/>
    <line x1="283" y1="56"  x2="262" y2="77"  stroke-width="2.5"/>
    <line x1="96"  y1="204" x2="117" y2="183" stroke-width="2.5"/>
    <line x1="283" y1="204" x2="262" y2="183" stroke-width="2.5"/>
  </g>

  <g filter="url(#wc)">
    <path d="M200 55 L214 105 L255 80 L230 118 L278 130
             L230 142 L255 180 L214 155 L200 205
             L186 155 L145 180 L170 142 L122 130
             L170 118 L145 80  L186 105 Z"
          fill="#e8b830" opacity="0.82"/>
    <path d="M200 90 L210 118 L238 105 L222 128 L248 130
             L222 132 L238 155 L210 142 L200 170
             L190 142 L162 155 L178 132 L152 130
             L178 128 L162 105 L190 118 Z"
          fill="#f8e060" opacity="0.72"/>
    <circle cx="200" cy="130" r="28" fill="#fef090" opacity="0.70"/>
    <circle cx="200" cy="130" r="16" fill="#fff8b0" opacity="0.80"/>
  </g>

  <g fill="#f0d060" opacity="0.65">
    <circle cx="200" cy="130" r="5"/>
    <circle cx="148" cy="88"  r="3"/>
    <circle cx="252" cy="88"  r="3"/>
    <circle cx="148" cy="172" r="3"/>
    <circle cx="252" cy="172" r="3"/>
    <circle cx="200" cy="62"  r="2.5"/>
    <circle cx="200" cy="198" r="2.5"/>
    <circle cx="132" cy="130" r="2.5"/>
    <circle cx="268" cy="130" r="2.5"/>
  </g>
"""))

print("Done — 6 illustrations generated.")
