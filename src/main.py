"""
Content Understanding example using azure-ai-projects SDK.

Usage:
    python main.py --help
    python main.py https://example.com/document.pdf
    python main.py --analyzer prebuilt-layout https://example.com/doc.pdf
    python main.py C:/Users/YourName/Desktop/invoice.pdf
"""

import os
import time
import base64
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from azure.ai.projects import AIProjectClient
from azure.core.rest import HttpRequest
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import typer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("azure").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Constants
API_VERSION = "2025-11-01"
POLL_TIMEOUT = 300  # 5 minutes timeout for analysis
POLL_INTERVAL = 1

# Create Typer app
app = typer.Typer(help="Content Understanding CLI tool")


def analyze_document(
    project_client: AIProjectClient,
    cu_endpoint: str,
    analyzer_id: str,
    file_path_or_url: str,
    api_version: str = API_VERSION,
    features: Optional[list[str]] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze a document using Content Understanding.
    
    Args:
        project_client: Authenticated AIProjectClient
        cu_endpoint: Content Understanding endpoint (base URL)
        analyzer_id: Analyzer to use (e.g., "prebuilt-invoice")
        file_path_or_url: Local file path or URL of the document to analyze
        api_version: API version
        features: Optional list of add-on features (e.g., ["annotations", "barcodes", "formulas"])
        config: Optional configuration dict (e.g., {"enableAnnotation": True, "enableFigureDescription": True, "enableFigureAnalysis": True, "chartFormat": "chartJs"})
        
    Returns:
        Analysis result
    """
    # Start analysis
    analyze_url = f"{cu_endpoint}/contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={api_version}"
    
    # Add features query parameter if provided
    if features:
        features_param = ",".join(features)
        analyze_url += f"&features={features_param}"
    
    # Check if input is a local file path
    path = Path(file_path_or_url)
    if path.exists() and path.is_file():
        # Read local file and convert to base64
        with open(path, 'rb') as f:
            file_data = f.read()
        base64_data = base64.b64encode(file_data).decode('utf-8')
        
        request_body = {"inputs": [{"data": base64_data}]}
        if config:
            request_body["config"] = config
            logger.debug(f"Sending config: {config}")
        
        request = HttpRequest(
            method="POST",
            url=analyze_url,
            json=request_body
        )
    else:
        # Treat as URL
        request_body = {"inputs": [{"url": file_path_or_url}]}
        if config:
            request_body["config"] = config
            logger.debug(f"Sending config: {config}")
        
        request = HttpRequest(
            method="POST",
            url=analyze_url,
            json=request_body
        )
    
    response = project_client.send_request(request)
    response.raise_for_status()
    
    # Content Understanding returns results asynchronously
    # The response contains an Operation-Location header with the URL to poll for results
    operation_location = response.headers.get("Operation-Location")
    
    # Poll the operation URL until analysis completes
    start_time = time.time()
    while True:
        if time.time() - start_time > POLL_TIMEOUT:
            raise TimeoutError(f"Analysis timed out after {POLL_TIMEOUT} seconds")

        request = HttpRequest(method="GET", url=operation_location)
        response = project_client.send_request(request)
        response.raise_for_status()
        
        result = response.json()
        status = result.get("status")
        
        if status == "Succeeded":
            return result
        elif status == "Failed":
            raise RuntimeError(f"Analysis failed: {result}")
        elif status in ["Running", "NotStarted"]:
            time.sleep(POLL_INTERVAL)
        else:
            raise ValueError(f"Unknown status: {status}")


@app.command()
def analyze(
    file_path_or_url: str = typer.Argument(..., help="Local file path or URL of the document to analyze"),
    analyzer: str = typer.Option("prebuilt-layout", "--analyzer", "-a", help="Analyzer to use"),
    features: str = typer.Option(None, "--features", help="Comma-separated add-on features (e.g., 'annotations,barcodes,formulas,ocrHighResolution,styleFont,languages,keyValuePairs')"),
    enable_annotation: bool = typer.Option(False, "--enable-annotation", help="Enable annotation extraction (highlights, underlines, strikethrough, comments)"),
    annotation_format: str = typer.Option("frontMatter", "--annotation-format", help="Annotation format: 'frontMatter' (default), 'markdown', or 'none'"),
    enable_figure_description: bool = typer.Option(False, "--enable-figure-description", help="Enable AI-generated descriptions for images and figures"),
    enable_figure_analysis: bool = typer.Option(False, "--enable-figure-analysis", help="Enable figure analysis (charts, tables, diagrams) for images"),
    chart_format: str = typer.Option("chartJs", "--chart-format", help="Chart format: 'chartJs' (default) or 'markdown'"),
    output: str = typer.Option(None, "--output", "-o", help="Save result to file (JSON)"),
    output_md: str = typer.Option(None, "--output-md", "-m", help="Save markdown to file"),
    show_full: bool = typer.Option(False, "--full", "-f", help="Show full markdown output"),
    save_results: bool = typer.Option(True, "--save-results/--no-save-results", help="Auto-save results to results folder"),
):
    """Analyze a document using Content Understanding."""
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    cu_endpoint = os.environ.get("AZURE_CU_ENDPOINT", endpoint)
    
    # Parse features if provided
    features_list = None
    if features:
        features_list = [f.strip() for f in features.split(",")]
        typer.echo(f"🎯 Add-on features enabled: {', '.join(features_list)}")
    
    # Build config object
    config = {}
    if enable_annotation:
        config["enableAnnotation"] = True
        config["returnDetails"] = True
        config["annotationFormat"] = annotation_format
        typer.echo(f"📝 Annotation extraction enabled (format: {annotation_format})")
    
    if enable_figure_description:
        config["enableFigureDescription"] = True
        typer.echo(f"🖼️  Figure description enabled")
    
    if enable_figure_analysis:
        config["enableFigureAnalysis"] = True
        config["chartFormat"] = chart_format
        typer.echo(f"📊 Figure analysis enabled (chart format: {chart_format})")
    
    # Only pass config if it has values
    config = config if config else None
    
    # Check if it's a local file
    path = Path(file_path_or_url)
    if path.exists() and path.is_file():
        typer.echo(f"📁 Local file detected: {path.name}")
    
    typer.echo(f"🔍 Analyzing document with {analyzer}...")
    
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    ):
        result = analyze_document(
            project_client=project_client,
            cu_endpoint=cu_endpoint,
            analyzer_id=analyzer,
            file_path_or_url=file_path_or_url,
            features=features_list,
            config=config
        )
        
        status = result['status']
        typer.echo(f"✓ Status: {status}")
        
        if status == "Succeeded":
            markdown = result['result']['contents'][0]['markdown']
            
            # Auto-save results if enabled
            if save_results:
                import json
                from datetime import datetime
                
                # Create results directory if it doesn't exist
                results_dir = Path("results")
                results_dir.mkdir(exist_ok=True)
                
                # Generate filename based on input file or timestamp
                if path.exists() and path.is_file():
                    base_name = path.stem
                else:
                    base_name = f"result_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Save JSON result
                json_path = results_dir / f"{base_name}_result.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                typer.echo(f"💾 Saved full result to: {json_path}")
                
                # Save markdown
                md_path = results_dir / f"{base_name}_output.md"
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                typer.echo(f"📝 Saved markdown to: {md_path}")
            
            # Save to custom file if specified
            if output:
                import json
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)
                typer.echo(f"💾 Saved custom result to: {output}")
            
            # Save markdown to custom file if specified
            if output_md:
                with open(output_md, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                typer.echo(f"📝 Saved custom markdown to: {output_md}")
            
            # Show markdown
            if show_full:
                typer.echo(f"\n📄 Extracted Markdown:\n{markdown}")
            else:
                typer.echo(f"\n📄 Extracted Markdown (preview):\n{markdown[:500]}...")
                typer.echo(f"\n(Use --full to see complete output)")


if __name__ == "__main__":
    app()
