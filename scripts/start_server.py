"""
企微博客助手 - 启动脚本
用于在 Cloud Studio 中一键启动 webhook 服务
"""

import subprocess
import sys
import os

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
    print("✅ 依赖安装完成")

def start_server():
    """启动服务"""
    print("🚀 正在启动博客AI发布助手...")
    print("   服务地址: http://0.0.0.0:7860")
    print("   Webhook 端点: POST /webhook/wechat")
    print("   API 端点: POST /api/generate")
    print("")
    import uvicorn
    uvicorn.run("wechat_blog_agent:app", host="0.0.0.0", port=7860, reload=False)

if __name__ == "__main__":
    # 检查依赖
    try:
        import fastapi
        import httpx
    except ImportError:
        install_dependencies()

    start_server()
