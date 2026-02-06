import asyncio
import sys
import os
import json
from mcp.server.fastmcp import FastMCP # Wait, prompt says NO fastmcp. Use standard SDK.

# Import standard SDK
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import logic
try:
    from logic import fetch_gold_passbook_twd, calculate_gold_value
except ImportError:
    # Dummy implementation if import fails (e.g. during dev/lint)
    def fetch_gold_passbook_twd():
        return {"error": "Logic module import failed"}
    def calculate_gold_value(grams, rate_type):
        return {"error": "Logic module import failed"}

# Initialize Server
app = Server("mcp-tw-gold-price")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_gold_passbook_twd",
            description="Get current Gold Passbook buying and selling prices in TWD from Bank of Taiwan.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="calculate_gold_value",
            description="Calculate the total value of gold in TWD based on weight (grams).",
            inputSchema={
                "type": "object",
                "properties": {
                    "grams": {
                        "type": "number",
                        "description": "Weight of gold in grams.",
                    },
                    "rate_type": {
                        "type": "string",
                        "enum": ["buying", "selling"],
                        "description": "Rate type: 'buying' (Bank buys from you) or 'selling' (Bank sells to you). Default is 'buying'.",
                        "default": "buying"
                    }
                },
                "required": ["grams"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    if name == "get_gold_passbook_twd":
        try:
            data = await asyncio.to_thread(fetch_gold_passbook_twd)
            return [TextContent(type="text", text=json.dumps(data, indent=2, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "calculate_gold_value":
        grams = arguments.get("grams")
        rate_type = arguments.get("rate_type", "buying")
        
        try:
            data = await asyncio.to_thread(calculate_gold_value, grams, rate_type)
            return [TextContent(type="text", text=json.dumps(data, indent=2, ensure_ascii=False))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    else:
        raise McpError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        sys.stderr.write(f"Server crashed: {e}\n")
        sys.exit(1)
