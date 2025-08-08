#!/usr/bin/env python3
"""
D&D Knowledge Navigator - Main server entry point.

This script starts the FastMCP server that provides D&D 5e information
through the Model Context Protocol (MCP).
"""
import logging
import sys
import traceback
import os
import uvicorn
from mcp.server.fastmcp import FastMCP

from src.core import api_helpers
from src.core import formatters
from src.core import prompts
from src.core import tools
from src.core import resources
from src.core.cache import APICache

# --- 将 app 的创建和配置移到全局作用域 ---
app = FastMCP("dnd-knowledge-navigator")

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dnd_mcp_server.log")
cache_dir = os.path.join(os.path.dirname(__file__), "cache")
cache = APICache(ttl_hours=24, persistent=True, cache_dir=cache_dir)

resources.register_resources(app, cache)
tools.register_tools(app, cache)
prompts.register_prompts(app)

def main():
    """Main entry point for the D&D Knowledge Navigator server."""
    try:
        print("Starting D&D Knowledge Navigator in Stdio mode...", file=sys.stderr)
        # --- 在这里，我们将启动方式修改为网络模式，并使用新端口 9452 ---
        uvicorn.run(app, host="0.0.0.0", port=9452)
        print("App run completed", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1

if __name__ == "__main__":
    # 现在，直接运行此脚本就会以网络模式启动
    sys.exit(main())
