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
import uvicorn  # 确保导入 uvicorn
from mcp.server.fastmcp import FastMCP

# Import from our reorganized structure
from src.core import api_helpers
from src.core import formatters
from src.core import prompts
from src.core import tools
from src.core import resources
from src.core.cache import APICache

# --- 全局作用域配置 ---
app = FastMCP("dnd-knowledge-navigator")
cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
cache = APICache(ttl_hours=24, persistent=True, cache_dir=cache_dir)

resources.register_resources(app, cache)
tools.register_tools(app, cache)
prompts.register_prompts(app)
# ---------------------

# 这个 if __name__ == "__main__" 块是 Hugging Face 启动的入口
if __name__ == "__main__":
    # 从环境变量中获取端口，Hugging Face 默认提供 7860
    # 如果在本地运行，没有 PORT 环境变量，则回退使用 9451
    port = int(os.environ.get('PORT', 9451))
    
    # 在云平台上，必须监听 0.0.0.0
    host = '0.0.0.0'
    
    print(f"Starting server on {host}:{port}")
    
    # 使用 uvicorn 来以网络模式运行我们的 app
    uvicorn.run(app, host=host, port=port)
