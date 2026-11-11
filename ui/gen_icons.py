#!/usr/bin/env python3
"""Generate monochrome SVG icon CSS custom properties and splice them into style.css.

usage: python3 ui/gen_icons.py ui/style.src.css ui/style.css
The template must contain the marker /*@ICONS@*/ which is replaced by the :root block.
"""
import sys
from urllib.parse import quote

FILE = "M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"
FOLD = "M14 3v5h5"


def f(*extra):
    return [FILE, FOLD, *extra]


ICONS = {
    "file": f(),
    "code": f("m10 12.5-2 2.25 2 2.25", "m14 12.5 2 2.25-2 2.25"),
    "doc": f("M9 13h6", "M9 17h6", "M9 9h1.5"),
    "book": ["M4 5.5A2.5 2.5 0 0 1 6.5 3H20v14H6.5A2.5 2.5 0 0 0 4 19.5z", "M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"],
    "image": ["M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z", "M10.5 9a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z", "m21 15-4.5-4.5L6 21"],
    "audio": ["M9 18V5l12-2v13", "M9 18a3 3 0 1 1-6 0 3 3 0 0 1 6 0z", "M21 16a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"],
    "video": ["M4 5h10a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z", "m16 10 6-3.5v11L16 14"],
    "pdf": f("M10 18v-5h1.75a1.6 1.6 0 0 1 0 3.2H10"),
    "slides": ["M4 4h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z", "M12 16v4", "M8 20h8", "m7 12 3-3 2 2 4-4"],
    "subs": ["M5 5h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z", "M7 15h4", "M14 15h3", "M7 11h2", "M12 11h5"],
    "sheet": ["M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z", "M3 9h18", "M3 15h18", "M9 3v18"],
    "archive": ["M4 4h16a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z", "M5 9v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V9", "M10 13h4"],
    "folder": ["M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"],
    "up": ["m14 9-5-5-5 5", "M20 20h-7a4 4 0 0 1-4-4V4"],
    "folder-plus": ["M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z", "M12 10v6", "M9 13h6"],
    "file-plus": f("M12 11v6", "M9 14h6"),
    "upload": ["M12 15V3", "m7 8 5-5 5 5", "M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"],
    "download": ["M12 3v12", "m7 10 5 5 5-5", "M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"],
    "close": ["M6 6l12 12", "M18 6 6 18"],
    "check": ["m5 12.5 4.5 4.5L19 7"],
    "alert": ["M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z", "M12 7.5v5.5", "M12 16.5v.01"],
    "sun": ["M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0z", "M12 2v2", "M12 20v2", "m4.9 4.9 1.4 1.4", "m17.7 17.7 1.4 1.4", "M2 12h2", "M20 12h2", "m4.9 19.1 1.4-1.4", "m17.7 6.3 1.4-1.4"],
    "moon": ["M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"],
    
}


def svg(paths):
    body = "".join(f"<path d='{d}'/>" for d in paths)
    s = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' "
         "stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'>" + body + "</svg>")
    # keep it readable: only escape what a CSS url("") data URI needs
    return quote(s, safe=" '=/:.,-")


def main():
    src, out = sys.argv[1], sys.argv[2]
    lines = [":root {"]
    for name, paths in ICONS.items():
        lines.append(f'  --i-{name}: url("data:image/svg+xml,{svg(paths)}");')
    lines.append("}")
    css = open(src, encoding="utf-8").read()
    assert "/*@ICONS@*/" in css
    open(out, "w", encoding="utf-8").write(css.replace("/*@ICONS@*/", "\n".join(lines)))


if __name__ == "__main__":
    main()
