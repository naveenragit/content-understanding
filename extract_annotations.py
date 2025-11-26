"""
Extract and display annotation text from Content Understanding results.

Usage:
    python extract_annotations.py results/your_result.json
"""

import json
import sys
from pathlib import Path


def extract_annotation_text(result_file: str):
    """Extract text for each annotation using offset and length."""
    
    with open(result_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get the markdown content (the full extracted text)
    markdown = data['result']['contents'][0]['markdown']
    
    # Get annotations
    annotations = data['result']['contents'][0].get('annotations', [])
    
    if not annotations:
        print("No annotations found in the document.")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(annotations)} annotation(s)")
    print(f"{'='*80}\n")
    
    for i, annotation in enumerate(annotations, 1):
        ann_id = annotation.get('id', 'unknown')
        kind = annotation.get('kind', 'unknown')
        author = annotation.get('author', 'unknown')
        created = annotation.get('createdAt', 'unknown')
        
        print(f"Annotation #{i}: {ann_id}")
        print(f"  Type: {kind}")
        print(f"  Author: {author}")
        print(f"  Created: {created}")
        
        # Extract the text using spans
        spans = annotation.get('spans', [])
        if spans:
            for span_idx, span in enumerate(spans):
                offset = span['offset']
                length = span['length']
                
                # Extract the actual text from markdown
                annotated_text = markdown[offset:offset + length]
                
                print(f"  Span {span_idx + 1}:")
                print(f"    Offset: {offset}, Length: {length}")
                print(f"    Text: \"{annotated_text}\"")
        else:
            print(f"  (No text spans - annotation may be document-level)")
        
        print()


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
