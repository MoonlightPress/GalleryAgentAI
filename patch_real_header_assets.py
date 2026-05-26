from pathlib import Path

path = Path("mochi_app.py")
text = path.read_text(encoding="utf-8")

old = '''
hero = asset("assets/mochi_header.svg")
if hero:
    st.image(hero, use_container_width=True)
'''

new = '''
hero = "assets/headers/mochi_header.png"

if Path(hero).exists():
    st.image(hero, use_container_width=True)
'''

text = text.replace(old, new)

path.write_text(text, encoding="utf-8")

print("Patched real image header.")