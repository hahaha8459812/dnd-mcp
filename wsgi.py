# 文件名: wsgi.py
# 作用: 这个文件是专门为 Gunicorn、uWSGI 等行业标准的网络服务器准备的“启动入口”。
#       它的存在，让我们的项目能够被这些服务器以最标准、最默认的方式来运行。

# 步骤 1: 从我们项目的主文件 dnd_mcp_server.py 中，导入那个最终配置好的、
#         可以对外提供服务的 FastAPI 应用实例，它的名字是 `app`。
from dnd_mcp_server import app

# 步骤 2: Gunicorn 服务器在默认情况下，会主动寻找一个名为 `application` 的变量来运行。
#         为了迎合这个默认约定，我们把我们自己的 `app` 赋值给一个新变量 `application`。
#         这样，当 Gunicorn 启动时，它就能自动找到并运行我们的程序，无需任何额外配置。
application = app

# 这个文件通常只需要这两行代码，它就像一个清晰的路牌，
# 告诉所有标准的服务器：“嘿，要运行的程序在这里！”
