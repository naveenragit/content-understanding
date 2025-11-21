"""
One-time setup to configure Content Understanding model deployments.
Run this once - settings persist across all CU calls.

Usage:
    1. Set deployment names in .env file (optional) or edit defaults below
    2. Run: python src/setup_deployments.py
"""
import os
import logging
from azure.ai.projects import AIProjectClient
from azure.core.rest import HttpRequest
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace these with YOUR deployment names from Foundry
# These are the names you gave to your deployments, not the model names
DEPLOYMENTS = {
    "gpt-4.1": os.getenv("DEPLOYMENT_GPT4", "gpt-4.1"),                      # e.g., "gpt-4.1" or "my-gpt4-prod"
    "gpt-4.1-mini": os.getenv("DEPLOYMENT_GPT4_MINI", "gpt-4.1-mini"),            # e.g., "gpt-4.1-mini" or "gpt4-mini-v2"
    "text-embedding-3-large": os.getenv("DEPLOYMENT_EMBEDDING", "text-embedding-3-large")  # e.g., "text-embedding-3-large"
}

def configure_deployments():
    """Configure Content Understanding to use specific model deployments."""
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    cu_endpoint = os.environ.get("AZURE_CU_ENDPOINT", endpoint)
    
    logger.info(f"🔧 Configuring Content Understanding deployments...")
    logger.info(f"   Project: {endpoint}")
    logger.info(f"   CU Endpoint: {cu_endpoint}")
    logger.info(f"   Deployments: {DEPLOYMENTS}")
    
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
    ):
        url = f"{cu_endpoint}/contentunderstanding/defaults?api-version=2025-11-01"
        
        request = HttpRequest(
            method="PATCH",
            url=url,
            json={"modelDeployments": DEPLOYMENTS}
        )
        
        response = project_client.send_request(request)
        response.raise_for_status()
        
        logger.info(f"✓ Successfully configured deployments!")
        logger.info(f"   These settings will be used for all Content Understanding calls.")

if __name__ == "__main__":
    try:
        configure_deployments()
    except KeyError as e:
        logger.error(f"❌ Error: Missing environment variable {e}")
        logger.error(f"   Make sure you have created a .env file with:")
        logger.error(f"   - AZURE_AI_PROJECT_ENDPOINT")
        logger.error(f"   - AZURE_CU_ENDPOINT")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
