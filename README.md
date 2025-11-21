# Azure Content Understanding - Python CLI Tool

A Python CLI tool for using Azure Content Understanding with Azure AI Foundry projects.

## Overview

Azure Content Understanding (CU) extracts structured data from documents like invoices, receipts, and forms using AI-powered analysis. This tool provides an easy-to-use command-line interface for document analysis with support for 80+ prebuilt analyzers, add-on features, and markdown configuration options.

**Key Features:**
- 🚀 Simple CLI interface with sensible defaults
- 📊 80+ prebuilt analyzers (invoices, receipts, contracts, etc.)
- 🎯 Add-on features (barcodes, formulas, annotations)
- 📝 Configurable markdown output with figure analysis
- 💾 Auto-save results to JSON and Markdown
- 🔐 Azure authentication via DefaultAzureCredential

---

## Quick Start (5 Minutes)

### Prerequisites

- Python 3.8 or higher
- An Azure AI Foundry project ([create one here](https://ai.azure.com))
- Azure CLI installed and authenticated (`az login`)

### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your endpoints (see below)

# 3. Authenticate with Azure
az login

# 4. Test with a sample document
python src/main.py analyze https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf
```

### Get Your Endpoints

1. Go to [Azure AI Foundry portal](https://ai.azure.com)
2. Open your project → **Settings** → **Project properties**
3. Copy the **Project endpoint** for `AZURE_AI_PROJECT_ENDPOINT`
4. For `AZURE_CU_ENDPOINT`, remove the `/api/projects/<project-name>` part

**Example `.env` file:**
```env
AZURE_AI_PROJECT_ENDPOINT=https://<your-foundry-resource>.services.ai.azure.com/api/projects/<your-project>
AZURE_CU_ENDPOINT=https://<your-foundry-resource>.services.ai.azure.com
```

---

## Quick Reference

### Basic Commands

```bash
# Help
python src/main.py --help

# Basic analysis (uses prebuilt-layout by default)
python src/main.py analyze <url-or-file>

# Specific analyzer
python src/main.py analyze -a prebuilt-invoice <url-or-file>

# Save outputs
python src/main.py analyze -o output.json -m output.md <url-or-file>

# Show full markdown
python src/main.py analyze --full <url-or-file>
```

### Common Analyzers

```bash
-a prebuilt-layout              # Layout analysis (default)
-a prebuilt-documentSearch      # Document search for RAG
-a prebuilt-invoice             # Invoices
-a prebuilt-receipt             # Receipts
-a prebuilt-idDocument          # IDs, passports
-a prebuilt-contract            # Contracts
-a prebuilt-tax.us.w2           # W-2 tax forms
```

[View all 80+ analyzers →](https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/prebuilt-analyzers)

### Add-on Features

```bash
--features barcodes              # Extract barcodes (FREE)
--features formulas              # Extract LaTeX formulas (PAID)
--features ocrHighResolution     # High-res OCR (PAID)
--features styleFont             # Font properties (PAID)
--features languages             # Language detection (FREE)
--features keyValuePairs         # Form fields (FREE)

# Combine multiple
--features barcodes,formulas,languages
```

### Markdown Configuration

```bash
# Figure options
--enable-figure-description               # Add AI descriptions to images
--enable-figure-analysis                  # Extract charts/tables/diagrams
--chart-format chartJs                    # Charts as JSON (default)
--chart-format markdown                   # Charts as Markdown tables

# Annotation options
--enable-annotation                       # Extract annotations
--annotation-format frontMatter           # YAML + HTML spans (default)
--annotation-format markdown              # Native Markdown syntax
--annotation-format none                  # JSON only
```

### Common Workflows

```bash
# Invoice processing
python src/main.py analyze -a prebuilt-invoice --features keyValuePairs invoice.pdf

# Scientific paper
python src/main.py analyze --features formulas --enable-figure-description paper.pdf

# Business report with charts
python src/main.py analyze --enable-figure-analysis --chart-format markdown report.pdf

# Reviewed document
python src/main.py analyze --enable-annotation reviewed-doc.pdf

# RAG pipeline
python src/main.py analyze -a prebuilt-documentSearch --enable-figure-description -m doc.md source.pdf

# Comprehensive analysis
python src/main.py analyze \
    --features barcodes,formulas,languages \
    --enable-annotation \
    --enable-figure-description \
    --enable-figure-analysis \
    -o result.json -m result.md --full \
    document.pdf
```

---

## Common Prebuilt Analyzers

Content Understanding provides 80+ prebuilt analyzers for different use cases:

**Common Analyzers:**
- `prebuilt-layout` - Layout analysis with tables, figures, and structure (recommended default)
- `prebuilt-documentSearch` - Document ingestion for RAG with layout, figures, charts, summaries
- `prebuilt-invoice` - Invoices, utility bills, sales orders
- `prebuilt-receipt` - Sales receipts
- `prebuilt-idDocument` - IDs, passports, driver licenses (worldwide)
- `prebuilt-tax.us.w2` - W-2 forms
- `prebuilt-contract` - Business contracts

**Categories Available:**
- Content extraction (OCR, layout)
- RAG analyzers (document/image/audio/video search)
- Financial documents (invoices, receipts, bank statements)
- Identity documents (IDs, passports, insurance cards)
- US tax documents (1040, W-2, 1099s, 1098s)
- US mortgage documents (1003, 1004, closing disclosures)
- Business & legal documents (contracts, purchase orders)
- And many more specialized analyzers

**Full List:** https://learn.microsoft.com/azure/ai-services/content-understanding/concepts/prebuilt-analyzers

---

## Usage Examples

### By Document Type

| Document Type | Command |
|---------------|---------|
| Invoice | `python src/main.py analyze -a prebuilt-invoice --features keyValuePairs invoice.pdf` |
| Receipt | `python src/main.py analyze -a prebuilt-receipt receipt.jpg` |
| Contract | `python src/main.py analyze -a prebuilt-contract --enable-annotation contract.pdf` |
| Research paper | `python src/main.py analyze --features formulas --enable-figure-description paper.pdf` |
| Technical doc | `python src/main.py analyze --features barcodes,formulas --enable-figure-analysis spec.pdf` |
| Presentation | `python src/main.py analyze --enable-figure-description --enable-figure-analysis slides.pdf` |
| Form | `python src/main.py analyze --features keyValuePairs form.pdf` |
| Engineering drawing | `python src/main.py analyze --features ocrHighResolution blueprint.pdf` |

### Save Options

```bash
# Auto-save to results/ folder (enabled by default)
python src/main.py analyze document.pdf
# Creates: results/document_result.json and results/document_output.md

# Custom output files
python src/main.py analyze -o custom.json -m custom.md document.pdf

# Disable auto-save
python src/main.py analyze --no-save-results document.pdf

# Show full output in console
python src/main.py analyze --full document.pdf
```

---

## Advanced Usage

### REST API (cURL)

### Example: Analyze Document (cURL)

```bash
# Start analysis with prebuilt-layout analyzer (recommended default)
curl -i -X POST "https://<your-foundry-resource>.services.ai.azure.com/contentunderstanding/analyzers/prebuilt-layout:analyze?api-version=2025-11-01" \
  -H "Authorization: Bearer $(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)" \
  -H "Content-Type: application/json" \
  -d '{
        "inputs":[{"url": "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"}]
      }'

# Or use a different analyzer - just change the analyzer name in the URL:
# ...analyzers/prebuilt-invoice:analyze...
# ...analyzers/prebuilt-documentSearch:analyze...
# ...analyzers/prebuilt-receipt:analyze...
```

The response includes:
- Status: `202 Accepted`
- `Operation-Location` header with the full URL to poll

### Poll for Results

```bash
# Extract the Operation-Location URL from the response headers
# Example: https://<your-foundry-resource>.services.ai.azure.com/contentunderstanding/analyzerResults/28bea330-d7e0-4159-b14c-9985df3fe4f4?api-version=2025-11-01

# Poll using that URL
curl -X GET "<operation-location-url>" \
  -H "Authorization: Bearer $(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)"

# The operation-location URL already includes the api-version parameter, so use it as-is
```

**Authentication:**
```bash
az login --tenant <your-tenant-id>
az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv
```

If you want Content Understanding to use your own Foundry model deployments:

**Prerequisites:** Active deployments in your Foundry project for GPT-4.1, GPT-4.1-mini, and text-embedding-3-large

**Setup:**
1. Edit `src/setup_deployments.py` with your deployment names
2. Run: `python src/setup_deployments.py`

This is a one-time setup - settings persist across all CU calls.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing environment variable" | Create `.env` file with both `AZURE_AI_PROJECT_ENDPOINT` and `AZURE_CU_ENDPOINT` |
| "Authentication failed" | Run `az login` to authenticate with Azure |
| "Invalid endpoint" | **CU endpoint** should NOT include `/api/projects/...` |
| Empty features | Ensure document contains that content type (e.g., barcodes) |
| Unexpected costs | Review which features are paid: `formulas`, `ocrHighResolution`, `styleFont` |

**Common Pitfall - Wrong Endpoint:**
```python
# ❌ Wrong - includes project path
cu_endpoint = "https://<resource>.services.ai.azure.com/api/projects/<project>"

# ✅ Correct - base URL only
cu_endpoint = "https://<resource>.services.ai.azure.com"
```

---

## Documentation

### Guides
- **[FEATURES.md](FEATURES.md)** - Detailed guide on add-on features (barcodes, formulas, annotations, etc.)
- **[MARKDOWN.md](MARKDOWN.md)** - Complete guide to markdown output and configuration options
- **[examples.py](examples.py)** - Code examples for various use cases

### Official Resources
- [Content Understanding Documentation](https://learn.microsoft.com/azure/ai-services/content-understanding/)
- [Markdown Output Documentation](https://learn.microsoft.com/azure/ai-services/content-understanding/document/markdown)
- [Azure AI Projects SDK](https://pypi.org/project/azure-ai-projects/)
- [Prebuilt Analyzers](https://learn.microsoft.com/azure/ai-services/content-understanding/prebuilt-models)
- [Document Intelligence Add-on Capabilities](https://learn.microsoft.com/azure/ai-services/document-intelligence/concept/add-on-capabilities)
