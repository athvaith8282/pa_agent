from mcp.server.fastmcp import FastMCP
from f1_tools import resgister_tools


mcp = FastMCP(name="F1_MCP")
resgister_tools(mcp)
mcp.run(transport="stdio")