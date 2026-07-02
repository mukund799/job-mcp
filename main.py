import os

import requests
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
TIMEOUT = int(os.getenv("TIMEOUT", "30"))

# initialize FastMCP
mcp = FastMCP("job_mcp", host=HOST, port=PORT, stateless_http=True)

@mcp.custom_route("/", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse({"status": "ok", "service": "job-mcp"})

# Export the ASGI app for Render/Uvicorn
asgi_app = mcp.streamable_http_app()

@mcp.tool()
def get_job_details_from_linkedin_uri(linkedin_uri: str):
    """
    Fetch job details from a LinkedIn job posting URI. scrap the job description from the LinkedIn page and return it as a dictionary.
    Args:
        linkedin_uri (str): The LinkedIn job posting URI.
    Returns:
        dict: A dictionary containing job details.
    """
    response = requests.get(linkedin_uri, timeout=TIMEOUT)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch job details from LinkedIn URI: {linkedin_uri}")
    return {
        "linkedin_uri": linkedin_uri,
        "description": response.text,
    }

def main():
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()