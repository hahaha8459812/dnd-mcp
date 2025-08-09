# 文件名: dnd_mcp_server.py
# 作用: 这是我们整个 D&D 知识库服务器的核心文件，负责创建和配置所有的服务逻辑。

# --- 基础模块导入 ---
import os
from fastapi import FastAPI  # 导入 FastAPI，这是我们用来创建标准网络服务的“接待员”。
from mcp.server.fastmcp import FastMCP  # 导入项目本身的 FastMCP 框架，这是我们的“顶尖专家”。
from src.core import resources, tools, prompts  # 导入项目内部的资源、工具和提示词模块。
from src.core.cache import APICache  # 导入缓存处理模块。

# --- 步骤 1: 创建并配置我们的“顶尖专家” (mcp_app) ---
# mcp_app 是一个专业的 FastMCP 应用实例，它只懂得处理 MCP 协议。
# 我们给它取一个专门的名字，以区别于最终对外服务的 app。
mcp_app = FastMCP("dnd-knowledge-navigator")

# 为 mcp_app 配置它需要的各种工具和资源。
# a. 配置缓存目录
cache_dir = os.path.join(os.path.dirname(__file__), "cache")
cache = APICache(ttl_hours=24, persistent=True, cache_dir=cache_dir)
# b. 将资源、工具、提示词都注册到 mcp_app 上
resources.register_resources(mcp_app, cache)
tools.register_tools(mcp_app, cache)
prompts.register_prompts(mcp_app)


# --- 步骤 2: 创建我们的“标准接待员” (app) ---
# app 是一个标准的 FastAPI 应用实例。它懂得标准的 HTTP 协议，能够应对所有类型的网络请求，
# 包括来自 Render 平台的健康检查。这是最终暴露给外界的、可以直接运行的对象。
app = FastAPI()


# --- 步骤 3: 让“接待员”引导 VIP 客户给“专家” (最关键的一步) ---
# 我们使用 .mount() 方法，将专业的 mcp_app “挂载”到标准 app 的根路径("/")上。
# 这意味着：
# 1. 当一个普通的健康检查请求进来时，app 会礼貌地处理，不会报错。
# 2. 当一个懂 MCP 协议的客户端（如 AstrBot）请求进来时，app 会把它无缝地转交给 mcp_app 来处理。
app.mount("/", mcp_app)

# --- 文件结束 ---
# 经过这样的改造，这个文件只负责“定义和配置”我们的服务。
# 它不再包含任何启动逻辑 (比如 uvicorn.run())。
# 启动的工作，完全交给了外部的 Gunicorn 服务器，由它来加载这个文件里定义的 `app`。
# 这实现了“逻辑”与“运行”的解耦，是更专业、更标准的做法。# 这叫做“挂载 (Mount)”，是解决这个问题的关键一步
app.mount("/", mcp_app)


# 5. 我们不再需要 main() 和 if __name__ == "__main__" 了
# 因为 Uvicorn 会直接加载上面创建的那个标准的 app 实例，
# 这样代码更简洁，也更符合云平台部署的标准。
