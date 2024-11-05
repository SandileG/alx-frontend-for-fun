#!/usr/bin/python3
"""
Markdown to HTML conversion script.
This script parses Markdown syntax and outputs the corresponding HTML.
"""

import sys
import os
import re


def main():
    # Check if the number of arguments is less than 3
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Process file to convert Markdown headings to HTML
    with open(markdown_file, 'r') as md_file,
    open(output_file, 'w') as html_file:
        for line in md_file:
            heading_match = re.match(r'^(#{1,6}) (.+)', line)
            if heading_match:
                heading_level = len(heading_match.group(1))
                heading_text = heading_match.group(2)
                html_file.write(
                    f"<h{heading_level}>{heading_text}</h{heading_level}>\n"
                )

    # Exit successfully if conversion is complete
    sys.exit(0)


if __name__ == "__main__":
    main()
