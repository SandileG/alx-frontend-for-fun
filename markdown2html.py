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
import sys


def convert_md_to_html(input_file, output_file):
    """
    Converts markdown file to HTML file.
    """
    # Read the contents of the input file
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False
    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            h_content = match.group(2).strip()
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
            continue
        
        # Check for unordered list items
        if re.match(r'^\- (.*)', line):
            if not in_list:
                html_content.append('<ul>\n')
                in_list = True
            li_content = re.sub(r'^\- (.*)', r'<li>\1</li>', line).strip()
            html_content.append(f'{li_content}\n')
            continue
        
        # Check for ordered list items
        if re.match(r'^\* (.*)', line):
            if not in_list:
                html_content.append('<ol>\n')
                in_list = True
            li_content = re.sub(r'^\* (.*)', r'<li>\1</li>', line).strip()
            html_content.append(f'{li_content}\n')
            continue

        # If we were in a list and encounter a non-list line, close the list
        if in_list:
            html_content.append('</ul>\n' if line.startswith('- ') else '</ol>\n')
            in_list = False

        # Handle paragraphs
        if line.strip():
            html_content.append(f'<p>{line.strip()}</p>\n')
        else:
            # If it's an empty line, add a line break for separation
            html_content.append('<br/>\n')

    # If we end with an open list, close it
    if in_list:
        html_content.append('</ul>\n' if re.match(r'^\- ', md_content[-1]) else '</ol>\n')

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
