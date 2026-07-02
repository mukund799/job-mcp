from main import mcp
@mcp.tool()
def test_tool():
    """
    A simple test tool to verify that the MCP is working correctly.
    Returns:
        str: A simple message indicating that the tool is working.
    
    """
    return "Hello from the test tool!"