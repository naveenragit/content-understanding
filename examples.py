"""
Comprehensive examples for Content Understanding CLI.

This script demonstrates various usage patterns organized by category:
1. Basic Analysis
2. Analyzer Selection
3. Add-on Features (barcodes, formulas, annotations, etc.)
4. Markdown Configuration (figure descriptions, chart extraction, annotations)
5. Document Type Workflows
6. Complex Scenarios

To run examples:
1. Set up your .env file with Azure credentials
2. Set RUN_EXAMPLES = True below
3. Run: python examples.py

Or uncomment individual examples to run them selectively.
"""

import subprocess
import sys
from pathlib import Path

# Set to True to actually run the examples
RUN_EXAMPLES = False

def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def run_example(description: str, command: list[str], category: str = ""):
    """Run or display an example command."""
    if category:
        print(f"📂 {category}")
    print(f"📋 {description}")
    print(f"💻 {' '.join(command)}\n")
    
    if RUN_EXAMPLES:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        else:
            print("❌ Error!")
            print(result.stderr)
    else:
        print("⏭️  Skipped (set RUN_EXAMPLES=True to run)\n")

# Sample document URLs for testing
SAMPLE_INVOICE = "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"
SAMPLE_DOC = "https://example.com/document.pdf"

def main():
    python_exe = sys.executable
    
    print("Content Understanding - Comprehensive Examples")
    print("=" * 80)
    if not RUN_EXAMPLES:
        print("\n⚠️  Set RUN_EXAMPLES = True to execute commands")
    print("=" * 80)
    
    # ===========================
    # BASIC ANALYSIS
    # ===========================
    print_section("1. Basic Analysis")
    
    run_example(
        "Basic analysis with default analyzer",
        [python_exe, "src/main.py", SAMPLE_INVOICE],
        "Basic"
    )
    
    run_example(
        "Show full markdown output",
        [python_exe, "src/main.py", "--full", SAMPLE_INVOICE],
        "Basic"
    )
    
    run_example(
        "Save to custom files",
        [python_exe, "src/main.py", "-o", "result.json", "-m", "result.md", SAMPLE_INVOICE],
        "Basic"
    )
    
    # ===========================
    # ANALYZER SELECTION
    # ===========================
    print_section("2. Analyzer Selection")
    
    run_example(
        "Invoice analyzer",
        [python_exe, "src/main.py", "-a", "prebuilt-invoice", SAMPLE_INVOICE],
        "Analyzers"
    )
    
    run_example(
        "Receipt analyzer",
        [python_exe, "src/main.py", "-a", "prebuilt-receipt", "https://example.com/receipt.jpg"],
        "Analyzers"
    )
    
    run_example(
        "Document search for RAG",
        [python_exe, "src/main.py", "-a", "prebuilt-documentSearch", "-m", "rag_doc.md", SAMPLE_DOC],
        "Analyzers"
    )
    
    run_example(
        "Contract analyzer",
        [python_exe, "src/main.py", "-a", "prebuilt-contract", "https://example.com/contract.pdf"],
        "Analyzers"
    )
    
    # ===========================
    # ADD-ON FEATURES
    # ===========================
    print_section("3. Add-on Features")
    
    run_example(
        "Extract barcodes (FREE)",
        [python_exe, "src/main.py", "--features", "barcodes", SAMPLE_DOC],
        "Features"
    )
    
    run_example(
        "Extract formulas (PAID)",
        [python_exe, "src/main.py", "--features", "formulas", "https://example.com/paper.pdf"],
        "Features"
    )
    
    run_example(
        "Multiple features",
        [python_exe, "src/main.py", "--features", "barcodes,formulas,languages", SAMPLE_DOC],
        "Features"
    )
    
    run_example(
        "High-resolution OCR (PAID)",
        [python_exe, "src/main.py", "--features", "ocrHighResolution", "https://example.com/blueprint.pdf"],
        "Features"
    )
    
    # ===========================
    # MARKDOWN CONFIGURATION
    # ===========================
    print_section("4. Markdown Configuration")
    
    run_example(
        "Enable figure descriptions",
        [python_exe, "src/main.py", "--enable-figure-description", SAMPLE_DOC],
        "Markdown Config"
    )
    
    run_example(
        "Extract charts as Chart.js JSON",
        [python_exe, "src/main.py", "--enable-figure-analysis", "--chart-format", "chartJs", SAMPLE_DOC],
        "Markdown Config"
    )
    
    run_example(
        "Extract charts as Markdown tables",
        [python_exe, "src/main.py", "--enable-figure-analysis", "--chart-format", "markdown", SAMPLE_DOC],
        "Markdown Config"
    )
    
    run_example(
        "Combined figure processing",
        [python_exe, "src/main.py", "--enable-figure-description", "--enable-figure-analysis", SAMPLE_DOC],
        "Markdown Config"
    )
    
    run_example(
        "Extract annotations (front matter)",
        [python_exe, "src/main.py", "--enable-annotation", "--annotation-format", "frontMatter", SAMPLE_DOC],
        "Markdown Config"
    )
    
    run_example(
        "Extract annotations (markdown syntax)",
        [python_exe, "src/main.py", "--enable-annotation", "--annotation-format", "markdown", SAMPLE_DOC],
        "Markdown Config"
    )
    
    # ===========================
    # DOCUMENT TYPE WORKFLOWS
    # ===========================
    print_section("5. Document Type Workflows")
    
    run_example(
        "Scientific paper",
        [python_exe, "src/main.py", "--features", "formulas", "--enable-figure-description", "--enable-figure-analysis", "https://example.com/paper.pdf"],
        "Workflows"
    )
    
    run_example(
        "Business report",
        [python_exe, "src/main.py", "--enable-figure-description", "--enable-figure-analysis", "--chart-format", "markdown", "https://example.com/report.pdf"],
        "Workflows"
    )
    
    run_example(
        "Reviewed document",
        [python_exe, "src/main.py", "--enable-annotation", "--annotation-format", "frontMatter", "https://example.com/reviewed-doc.pdf"],
        "Workflows"
    )
    
    run_example(
        "Technical specification",
        [python_exe, "src/main.py", "--features", "barcodes,formulas", "--enable-figure-analysis", "https://example.com/spec.pdf"],
        "Workflows"
    )
    
    # ===========================
    # COMPREHENSIVE EXAMPLES
    # ===========================
    print_section("6. Comprehensive Analysis")
    
    run_example(
        "All features and options",
        [python_exe, "src/main.py",
         "-a", "prebuilt-layout",
         "--features", "barcodes,formulas,languages",
         "--enable-annotation",
         "--enable-figure-description",
         "--enable-figure-analysis",
         "-o", "comprehensive.json",
         "-m", "comprehensive.md",
         "--full",
         SAMPLE_DOC],
        "Comprehensive"
    )
    
    # Summary
    print_section("Summary")
    print("""
📚 All Examples Defined!

To run these examples:
1. Set up your .env file with Azure credentials  
2. Set RUN_EXAMPLES = True at the top of this file
3. Run: python examples.py

Or uncomment individual examples to run them selectively.

For more information:
  - README.md - Main documentation
  - FEATURES.md - Add-on features guide
  - MARKDOWN.md - Markdown representation guide
    """)

if __name__ == "__main__":
    main()
