from server import mcp
import requests
from shared.config import Config

config = Config()

@mcp.tool()
def naukri_get_job_details_from_uri(naukri_uri: str):
    """
    Fetch job details from a Naukri job posting URI. scrap the job description from the Naukri page and return it as a dictionary.
    Args:
        naukri_uri (str): The Naukri job posting URI.
    Returns:
        dict: A dictionary containing job details.
    """
    response = requests.get(naukri_uri, timeout=config.TIMEOUT)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch job details from Naukri URI: {naukri_uri}")
    return {
        "naukri_uri": naukri_uri,
        "description": response.text,
    }