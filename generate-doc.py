import argparse
from pathlib import Path

import wikipedia
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
# we know some glyphs are missing, suppress warnings
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        default="/tmp/weekly-print.pdf",
        help="PDF output file (default: %(default)s)",
    )
    parser.add_argument("--image", help="image to add to PDF")

    args = parser.parse_args()

    page = get_random_page()

    pdf = Path(args.output)
    c = canvas.Canvas(f"{pdf}", pagesize=A4)
    pdfmetrics.registerFont(TTFont('DejaVu Serif', 'DejaVuSerif.ttf'))
    start_pos_x = 50
    start_pos_y = 780
    pos_y = start_pos_y

    c.setFont("DejaVu Serif", 18)
    for line in get_lines(page.title):
        c.drawString(start_pos_x, pos_y, line)
        pos_y -= 30

    c.setFontSize(12)
    for line in get_lines(page.summary):
        c.drawString(start_pos_x, pos_y, line)
        pos_y -= 20

    if args.image:
        pos_y -= 200
        image = Path(args.image)
        if image.exists() and image.is_file():
            c.drawImage(image, start_pos_x + 100, pos_y, width=200, height=100)

    c.showPage()
    c.save()


def get_random_page():
    while True:
        try:
            page = wikipedia.page(wikipedia.random())
            break
        except:  # Try again if any error from the library occurs
            pass

    return page


def get_lines(text):
    wrap_line_length = 75
    lines = []
    line = ""
    length = 0
    for c in text:
        line += c
        length += 1
        if length > wrap_line_length and c.isspace():
            lines.append(line)
            line = ""
            length = 0

    # Add last line
    lines.append(line)
    return lines


if __name__ == "__main__":
    main()
