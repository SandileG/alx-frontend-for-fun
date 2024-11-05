#!/usr/bin/python3
"""
This script converts a Markdown file to HTML format.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: The Markdown file to be converted
    output_file: The name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""

import argparse
import hashlib
import pathlib
import re
import sys


def convert_md_to_html(input_file, output_file):
    """Convert Markdown to HTML."""
    with open(input_file, encoding='utf-8') as f:
        md_content = f.readlines()

    html_content = []
    in_list = False
    for line in md_content:
        # Handle headers
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            h_level = len(match.group(1))
            h_content = match.group(2).strip()
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
            continue

        # Handle unordered list items
        if re.match(r'^\- (.*)', line):
            if not in_list:
                html_content.append('<ul>\n')
                in_list = True
            li_content = re.sub(r'^\- (.*)', r'<li>\1</li>', line).strip()
            li_content = parse_bold_italic(li_content)
            html_content.append(f'{li_content}\n')
            continue

        # Check for ordered list items
        if re.match(r'^\* (.*)', line):
            if not in_list:
                html_content.append('<ol>\n')
                in_list = True
            li_content = re.sub(r'^\* (.*)', r'<li>\1</li>', line).strip()
            li_content = parse_bold_italic(li_content)
            html_content.append(f'{li_content}\n')
            continue

        # Close the list if we encountered a non-list line
        if in_list:
            html_content.append('</ul>\n')
            in_list = False

        # Handle paragraphs
        if line.strip():
            paragraph = f'<p>{line.strip()}</p>\n'
            paragraph = parse_bold_italic(paragraph)
            paragraph = parse_custom_syntax(paragraph)
            html_content.append(paragraph)
        else:
            html_content.append('<br/>\n')

    # Close any open list
    if in_list:
        html_content.append('</ul>\n')

    # Write HTML content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(html_content)


def parse_bold_italic(text):
    """Convert Markdown bold and italic syntax to HTML."""
    # Convert bold syntax
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Convert italic syntax
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
    return text


def parse_custom_syntax(text):
    """Convert custom Markdown syntax to HTML."""
    # Convert [[text]] to MD5 hash
    text = re.sub(r'\[\[(.+?)\]\]', lambda match: md5_hash(match.group(1)), text)

    # Remove all 'c' (case insensitive) from ((text))
    text = re.sub(r'\(\((.+?)\)\)', lambda match: remove_char(match.group(1), 'c'), text)

    return text


def md5_hash(text):
    """Return the MD5 hash of the given text in lowercase."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def remove_char(text, char):
    """Return the text with all occurrences of char removed."""
    return text.replace(char, '').replace(char.upper(), '')


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
