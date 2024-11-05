#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import pathlib
import re


def convert_md_to_html(input_file, output_file):
    '''
    Converts markdown file to HTML file
    '''
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'(#){1,6} (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            # Get the content of the heading
            h_content = match.group(2)
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
        else:
            html_content.append(line)

    # Write the HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert markdown to HTML')
    parser.add_argument('input_file', help='path to input markdown file')
    parser.add_argument('output_file', help='path to output HTML file')
    args = parser.parse_args()

    # Check if the input file exists
    input_path = pathlib.Path(args.input_file)
    if not input_path.is_file():
        print(f'Missing {input_path}', file=sys.stderr)
        sys.exit(1)

    # Convert the markdown file to HTML
    convert_md_to_html(args.input_file, args.output_file)

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
