from starlette.requests import Request
from starlette.responses import JSONResponse

from server import mcp

# Import all tools
import tools.linkedin
import tools.naukri
import tools.shared

@mcp.custom_route("/", methods=["GET"])
async def health_check(request: Request):
    return JSONResponse(
        {
            "status": "ok",
            "service": "job-mcp",
        }
    )

asgi_app = mcp.streamable_http_app()

def main():
    mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()