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
    in_unordered_list = False
    in_ordered_list = False
    current_paragraph = []

    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            if current_paragraph:
                # If there's a paragraph before the heading, flush it
                paragraph = " ".join(current_paragraph).strip()
                html_content.append(f'<p>{paragraph}</p>\n')
                current_paragraph = []

            h_level = len(match.group(1))
            h_content = match.group(2).strip()
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
            continue
        
        # Check if the line is an unordered list item
        if line.startswith('- '):
            if current_paragraph:
                # Flush the current paragraph before starting a list
                paragraph = " ".join(current_paragraph).strip()
                html_content.append(f'<p>{paragraph}</p>\n')
                current_paragraph = []
            if not in_unordered_list:
                html_content.append('<ul>\n')
                in_unordered_list = True
            item_content = line[2:].strip()
            html_content.append(f'  <li>{item_content}</li>\n')
            continue
        
        # Check if the line is an ordered list item
        if line.startswith('* '):
            if current_paragraph:
                # Flush the current paragraph before starting a list
                paragraph = " ".join(current_paragraph).strip()
                html_content.append(f'<p>{paragraph}</p>\n')
                current_paragraph = []
            if not in_ordered_list:
                html_content.append('<ol>\n')
                in_ordered_list = True
            item_content = line[2:].strip()
            html_content.append(f'  <li>{item_content}</li>\n')
            continue
        
        # Handle paragraphs: detect blank lines
        if line.strip() == "":
            if current_paragraph:
                # If we have collected lines for a paragraph, flush it to HTML
                paragraph = " ".join(current_paragraph).strip()
                html_content.append(f'<p>{paragraph}</p>\n')
                current_paragraph = []
            continue
        
        # Handle normal text (paragraph lines)
        if current_paragraph:
            current_paragraph.append(line.strip())
        else:
            current_paragraph = [line.strip()]

    # Flush any remaining paragraph content
    if current_paragraph:
        paragraph = " ".join(current_paragraph).strip()
        html_content.append(f'<p>{paragraph}</p>\n')

    # Close any open lists at the end of the file
    if in_unordered_list:
        html_content.append('</ul>\n')
    if in_ordered_list:
        html_content.append('</ol>\n')

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
