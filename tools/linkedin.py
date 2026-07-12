from main import mcp
import requests
from shared.config import Config

config = Config()

@mcp.tool()
def test_tool():
    """
    A simple test tool to verify that the MCP is working correctly.
    Returns:
        str: A simple message indicating that the tool is working.
    
    """
    return "Hello from the test tool!"

@mcp.tool()
def get_job_details_from_linkedin_uri(linkedin_uri: str):
    """
    Fetch job details from a LinkedIn job posting URI. scrap the job description from the LinkedIn page and return it as a dictionary.
    Args:
        linkedin_uri (str): The LinkedIn job posting URI.
    Returns:
        dict: A dictionary containing job details.
    """
    response = requests.get(linkedin_uri, timeout=config.TIMEOUT)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch job details from LinkedIn URI: {linkedin_uri}")
    return {
        "linkedin_uri": linkedin_uri,
        "description": response.text,
    }