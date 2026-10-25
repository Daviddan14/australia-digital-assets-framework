"""Make scripts/reference.docx, the style template pandoc uses for the Word file.

    python3 scripts/reference_docx.py

Sans-serif throughout (the brand kit never substitutes a serif), slate text,
brand red reserved for the title rule. Needs pandoc and python-docx.
"""

import os
import subprocess

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Pt, RGBColor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "reference.docx")
FONT = "Arial"
INK = RGBColor(0x0F, 0x1A, 0x22)
ACCENT = RGBColor(0xB3, 0x27, 0x2A)

subprocess.run(["pandoc", "-o", OUT, "--print-default-data-file", "reference.docx"], check=True)

doc = Document(OUT)
for style in doc.styles:
    if style.type != 1:  # paragraph styles only
        continue
    font = style.font
    font.name = FONT
    font.color.rgb = INK
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts")
    if fonts is not None:
        for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
            fonts.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}" + attr, FONT)
        for attr in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
            key = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}" + attr
            if key in fonts.attrib:
                del fonts.attrib[key]

sizes = {"Normal": 10.5, "Body Text": 10.5, "First Paragraph": 10.5, "Compact": 10.5,
         "Title": 24, "Subtitle": 13, "Heading 1": 18, "Heading 2": 15, "Heading 3": 12, "Heading 4": 10.5}
for name, size in sizes.items():
    if name in doc.styles:
        st = doc.styles[name]
        st.font.size = Pt(size)
        if name.startswith("Heading") or name == "Title":
            st.font.bold = True
        if name in ("Body Text", "First Paragraph", "Normal"):
            st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            st.paragraph_format.line_spacing = 1.25
            st.paragraph_format.space_after = Pt(6)
for name in ("Heading 4", "Hyperlink"):
    if name in doc.styles:
        doc.styles[name].font.color.rgb = ACCENT
doc.save(OUT)
print("wrote", OUT)
