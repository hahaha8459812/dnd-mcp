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

# 1. 引入一位新帮手 (FastAPI)，他就是我们的“标准接待员”
from fastapi import FastAPI

from mcp.server.fastmcp import FastMCP
from src.core import api_helpers, formatters, prompts, tools, resources
from src.core.cache import APICache

# 2. 为我们的专家改个名，以免和接待员重名
mcp_app = FastMCP("dnd-knowledge-navigator")

# (配置我们专家 mcp_app 的所有工具和资源，这部分不变)
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "dnd_mcp_server.log")
cache_dir = os.path.join(os.path.dirname(__file__), "cache")
cache = APICache(ttl_hours=24, persistent=True, cache_dir=cache_dir)
resources.register_resources(mcp_app, cache)
tools.register_tools(mcp_app, cache)
prompts.register_prompts(mcp_app)


# 3. 创建标准的接待员 app，Uvicorn 服务器会直接和他对话
app = FastAPI()

# 4. 让接待员引导访客：告诉接待员，把所有来访者都引导给我们的专家 mcp_app
# 这叫做“挂载 (Mount)”，是解决这个问题的关键一步
app.mount("/", mcp_app)


# 5. 我们不再需要 main() 和 if __name__ == "__main__" 了
# 因为 Uvicorn 会直接加载上面创建的那个标准的 app 实例，
# 这样代码更简洁，也更符合云平台部署的标准。
