"""
Extract and display annotation text from Content Understanding results.

Usage:
    python extract_annotations.py results/your_result.json
"""

import json
import sys
from pathlib import Path


def get_annotation_details(annotation: dict) -> dict:
    """Extract basic details from an annotation."""
    return {
        'id': annotation.get('id', 'unknown'),
        'kind': annotation.get('kind', 'unknown'),
        'author': annotation.get('author', 'unknown'),
        'created': annotation.get('createdAt', 'unknown'),
        'spans': annotation.get('spans', [])
    }


def format_annotation_entry(index: int, annotation: dict, markdown_content: str) -> list[str]:
    """Format a single annotation entry into lines of text."""
    details = get_annotation_details(annotation)
    lines = []
    
    lines.append(f"Annotation #{index}: {details['id']}")
    lines.append(f"  Type: {details['kind']}")
    lines.append(f"  Author: {details['author']}")
    lines.append(f"  Created: {details['created']}")
    
    if details['spans']:
        for span_idx, span in enumerate(details['spans']):
            offset = span['offset']
            length = span['length']
            annotated_text = markdown_content[offset:offset + length]
            
            lines.append(f"  Span {span_idx + 1}:")
            lines.append(f"    Offset: {offset}, Length: {length}")
            lines.append(f"    Text: \"{annotated_text}\"")
    else:
        lines.append("  (No text spans - annotation may be document-level)")
    
    lines.append("")  # Empty line for separation
    return lines


def save_output_to_file(lines: list[str], source_file: str) -> str:
    """Save the formatted lines to a file."""
    result_path = Path(source_file)
    output_filename = result_path.stem + "_results.txt"
    output_path = result_path.parent / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return str(output_path)


def extract_annotation_text(result_file: str):
    """Extract text for each annotation using offset and length."""
    
    with open(result_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Validate structure
    if not data.get('result') or not data['result'].get('contents'):
        print("Invalid result format: missing 'result' or 'contents'")
        return

    content = data['result']['contents'][0]
    markdown = content.get('markdown', '')
    annotations = content.get('annotations', [])
    
    if not annotations:
        print("No annotations found in the document.")
        return
    
    # Prepare header
    header_lines = [
        f"{'='*80}",
        f"Found {len(annotations)} annotation(s)",
        f"{'='*80}",
        ""
    ]
    
    all_output_lines = list(header_lines)
    
    # Process annotations
    for i, annotation in enumerate(annotations, 1):
        entry_lines = format_annotation_entry(i, annotation, markdown)
        all_output_lines.extend(entry_lines)
    
    # Print to console
    for line in all_output_lines:
        print(line)
        
    # Save to file
    saved_path = save_output_to_file(all_output_lines, result_file)
    print(f"\nExtracted text saved to: {saved_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_annotations.py <result_file.json>")
        print("\nExample:")
        print("  python extract_annotations.py results/document_result.json")
        sys.exit(1)
    
    result_file = sys.argv[1]
    
    if not Path(result_file).exists():
        print(f"Error: File not found: {result_file}")
        sys.exit(1)
    
    extract_annotation_text(result_file)


if __name__ == "__main__":
    main()
