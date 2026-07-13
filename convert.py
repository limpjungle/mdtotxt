import sys
import os
import argparse
import re

import markdown
from bs4 import BeautifulSoup


def md_to_plain_text(md_content: str) -> str:
    # Markdown to HTML
    html = markdown.markdown(md_content)
    # Txt from HTML
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    # delete empty strings
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Convert .md to .txt, deletete Markdown."
    )
    parser.add_argument("input", help="Path to input .md file")
    parser.add_argument("-o", "--output", help="Path to output .txt File.")
    args = parser.parse_args()

    # Check input file
    if not os.path.isfile(args.input):
        print(f'Error: file "{args.input}" not found.', file=sys.stderr)
        sys.exit(1)

    # Read .md
    with open(args.input, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Converting
    plain_text = md_to_plain_text(md_content)

    # Name output file
    if args.output:
        out_path = args.output
    else:
        base = os.path.splitext(args.input)[0]
        out_path = base + ".txt"

    # Write result
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(plain_text)

    print(f"Done: {out_path}")


if __name__ == "__main__":
    main()
