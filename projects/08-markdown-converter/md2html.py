#!/usr/bin/env python3
"""
Markdown Converter - Convert Markdown to HTML
"""
import argparse
import re
from pathlib import Path
from typing import Optional


def convert_headers(text: str) -> str:
    """Convert markdown headers to HTML."""
    for i in range(6, 0, -1):
        pattern = r'^#{' + str(i) + r'}\s+(.+)$'
        replacement = f'<h{i}>\\1</h{i}>'
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text


def convert_bold(text: str) -> str:
    """Convert bold text."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    return text


def convert_italic(text: str) -> str:
    """Convert italic text."""
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
    return text


def convert_code(text: str) -> str:
    """Convert inline code and code blocks."""
    # Code blocks
    text = re.sub(
        r'```(\w+)?\n(.*?)```',
        r'<pre><code class="language-\1">\2</code></pre>',
        text,
        flags=re.DOTALL
    )
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def convert_links(text: str) -> str:
    """Convert links and images."""
    # Images
    text = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1">', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


def convert_lists(text: str) -> str:
    """Convert unordered and ordered lists."""
    lines = text.split('\n')
    result = []
    in_ul = False
    in_ol = False
    
    for line in lines:
        # Unordered list
        if re.match(r'^[\s]*[-*+]\s+', line):
            if not in_ul:
                result.append('<ul>')
                in_ul = True
            content = re.sub(r'^[\s]*[-*+]\s+', '', line)
            result.append(f'<li>{content}</li>')
        # Ordered list
        elif re.match(r'^[\s]*\d+\.\s+', line):
            if not in_ol:
                result.append('<ol>')
                in_ol = True
            content = re.sub(r'^[\s]*\d+\.\s+', '', line)
            result.append(f'<li>{content}</li>')
        else:
            if in_ul:
                result.append('</ul>')
                in_ul = False
            if in_ol:
                result.append('</ol>')
                in_ol = False
            result.append(line)
    
    if in_ul:
        result.append('</ul>')
    if in_ol:
        result.append('</ol>')
    
    return '\n'.join(result)


def convert_blockquotes(text: str) -> str:
    """Convert blockquotes."""
    lines = text.split('\n')
    result = []
    in_quote = False
    
    for line in lines:
        if line.startswith('>'):
            if not in_quote:
                result.append('<blockquote>')
                in_quote = True
            content = line[1:].strip()
            result.append(content)
        else:
            if in_quote:
                result.append('</blockquote>')
                in_quote = False
            result.append(line)
    
    if in_quote:
        result.append('</blockquote>')
    
    return '\n'.join(result)


def convert_paragraphs(text: str) -> str:
    """Wrap text in paragraphs."""
    lines = text.split('\n\n')
    result = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('<'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    
    return '\n\n'.join(result)


def markdown_to_html(markdown: str, full_html: bool = False) -> str:
    """Convert Markdown to HTML."""
    html = markdown
    
    # Apply conversions
    html = convert_code(html)
    html = convert_headers(html)
    html = convert_bold(html)
    html = convert_italic(html)
    html = convert_links(html)
    html = convert_lists(html)
    html = convert_blockquotes(html)
    html = convert_paragraphs(html)
    
    if full_html:
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Converted Document</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #ddd; margin: 0; padding-left: 20px; color: #666; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    return html


def main():
    parser = argparse.ArgumentParser(description="Markdown to HTML Converter")
    parser.add_argument("input", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file")
    parser.add_argument("-f", "--full", action="store_true", help="Generate full HTML document")
    parser.add_argument("-p", "--print", action="store_true", help="Print to stdout")
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"❌ File not found: {args.input}")
        return
    
    # Read Markdown
    markdown = args.input.read_text()
    
    # Convert
    html = markdown_to_html(markdown, args.full)
    
    if args.print:
        print(html)
    else:
        output_file = args.output or args.input.with_suffix('.html')
        output_file.write_text(html)
        print(f"✅ Converted: {args.input} -> {output_file}")


if __name__ == "__main__":
    main()

# complex test
