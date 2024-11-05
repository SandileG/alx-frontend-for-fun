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
    in_unordered_list = False  # Track whether we're currently in an unordered list
    in_ordered_list = False    # Track whether we're currently in an ordered list
    current_paragraph = []      # Store lines for the current paragraph

    for line in md_content:
        # Check if the line is a heading
        match = re.match(r'^(#{1,6}) (.*)', line)
        if match:
            # Get the level of the heading
            h_level = len(match.group(1))
            # Get the content of the heading
            h_content = match.group(2).strip()  # Strip any extra whitespace
            # Append the HTML equivalent of the heading
            html_content.append(f'<h{h_level}>{h_content}</h{h_level}>\n')
            continue
        
        # Check if the line is an unordered list item
        if line.startswith('- '):
            if in_ordered_list:  # Close ordered list if we were in one
                html_content.append('</ol>\n')
                in_ordered_list = False
            if not in_unordered_list:
                html_content.append('<ul>\n')  # Start the unordered list
                in_unordered_list = True
            # Get the content of the list item
            item_content = line[2:].strip()  # Remove '- ' and strip whitespace
            html_content.append(f'  <li>{item_content}</li>\n')  # Append list item
            continue
        
        # Check if the line is an ordered list item
        if line.startswith('* '):
            if in_unordered_list:  # Close unordered list if we were in one
                html_content.append('</ul>\n')
                in_unordered_list = False
            if not in_ordered_list:
                html_content.append('<ol>\n')  # Start the ordered list
                in_ordered_list = True
            # Get the content of the list item
            item_content = line[2:].strip()  # Remove '* ' and strip whitespace
            html_content.append(f'  <li>{item_content}</li>\n')  # Append list item
            continue
        
        # Handle paragraphs: detect blank lines
        if line.strip() == "":
            if current_paragraph:
                # If we have collected lines for a paragraph, flush it to HTML
                paragraph = " ".join(current_paragraph).strip()
                html_content.append(f'<p>{paragraph}</p>\n')
                current_paragraph = []  # Reset for the next paragraph
            continue
        
        # Handle normal text (paragraph lines)
        current_paragraph.append(line.strip())  # Add line to current paragraph

    # If there's any remaining paragraph content after the loop, add it
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
