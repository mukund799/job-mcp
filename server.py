import os
from mcp.server.fastmcp import FastMCP
from mcp import types

from shared.config import Config

config = Config()

mcp = FastMCP(
    "job_mcp",
    host=config.HOST,
    port=config.PORT,
    stateless_http=True,
)