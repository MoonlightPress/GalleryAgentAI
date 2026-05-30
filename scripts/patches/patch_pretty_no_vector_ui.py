from pathlib import Path

path = Path("mochi_app.py")
text = path.read_text(encoding="utf-8")

# Hide the ugly SVG image calls visually by replacing section images with styled banners.
text = text.replace(
'''    img = asset(config["image"])
    if img:
        st.image(img, use_container_width=True)

    section_opps = [''',
'''    st.markdown(
        f"""
        <div style="
            margin-top: 28px;
            margin-bottom: 14px;
            padding: 18px 22px;
            border-radius: 24px;
            border: 1px solid #d9bf96;
            background:
                radial-gradient(circle at 8% 18%, rgba(190,130,98,.20), transparent 18%),
                radial-gradient(circle at 92% 24%, rgba(130,160,115,.20), transparent 16%),
                linear-gradient(135deg, #fffaf0 0%, #f3e4ce 100%);
            box-shadow: 0 8px 24px rgba(78, 55, 30, .10);
            position: relative;
        ">
            <div style="
                font-family: Georgia, serif;
                font-size: 1.45rem;
                font-weight: 700;
                color: #4f3c2f;
                letter-spacing: .01em;
            ">{section}</div>
            <div style="
                margin-top: 4px;
                color: #7b6a55;
                font-size: .94rem;
            ">Curated opportunities, source links, and ready-to-send drafts.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    section_opps = ['''
)

# Replace card CSS with prettier version.
text = text.replace(
'''.mochi-card {
    background: rgba(255, 252, 246, .95);
    border: 1px solid #e4d2b9;
    border-radius: 18px;
    padding: 14px;
    min-height: 210px;
    box-shadow: 0 3px 10px rgba(91, 72, 45, .08);
}''',
'''.mochi-card {
    background:
        linear-gradient(#fffdf8, #fff9ef),
        radial-gradient(circle at top left, rgba(190,130,98,.12), transparent 30%);
    border: 1px solid #d9c19a;
    border-radius: 22px;
    padding: 16px;
    min-height: 220px;
    box-shadow:
        0 8px 20px rgba(84, 57, 29, .10),
        inset 0 0 0 1px rgba(255,255,255,.65);
    position: relative;
}'''
)

text = text.replace(
'''.mochi-card-title {
    font-weight: 700;
    font-size: 1rem;
    color: #4d4035;
}''',
'''.mochi-card-title {
    font-family: Georgia, serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #4a372b;
    line-height: 1.22;
}'''
)

text = text.replace(
'''.detail-box {
    background: #fffaf1;
    border: 1px solid #e0ccb0;
    border-radius: 20px;
    padding: 18px;
    margin-top: 12px;
}''',
'''.detail-box {
    background:
        linear-gradient(180deg, #fffdf8 0%, #fff7ea 100%);
    border: 1px solid #d6bb91;
    border-radius: 28px;
    padding: 24px;
    margin-top: 18px;
    box-shadow: 0 12px 32px rgba(84, 57, 29, .13);
}'''
)

# Add prettier global accents after style opening.
text = text.replace(
'''<style>
.stApp {''',
'''<style>
:root {
    --paper: #fbf4e8;
    --ink: #49382c;
    --muted: #7c6a55;
    --gold: #c9a96b;
    --leaf: #8fa77d;
    --rose: #c98370;
}

.stApp {'''
)

path.write_text(text, encoding="utf-8")
print("Patched Mochi UI: removed ugly vector section art, added paper/filigree styling.")