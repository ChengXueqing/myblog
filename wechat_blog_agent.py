"""
企业微信群机器人 webhook 接收服务
接收消息 → AI生成博客内容 → 自动创建 GitHub PR

依赖: pip install -r requirements.txt
运行: python wechat_blog_agent.py
"""

import os
import re
import base64
import hashlib
import hmac
import time
import json
from datetime import datetime
from typing import Optional

# 加载 .env 环境变量
from dotenv import load_dotenv
load_dotenv()

import requests
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx

# ============== 配置区 ==============

# 企业微信群机器人配置
WECOM_BOT_SECRET = os.getenv("WECOM_BOT_SECRET", "")  # 机器人密钥
WECOM_BOT_WEBHOOK = os.getenv("WECOM_BOT_WEBHOOK", "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY_HERE")

# LLM API 配置 (DeepSeek / 硅基流动)
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.deepseek.com/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "ChengXueqing/myblog")  # 博客仓库
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "master")

# Hugo 内容配置
CONTENT_CATEGORIES = ["basic", "advanced", "interview", "others", "engineering"]
DEFAULT_CATEGORY = "basic"

# ============== FastAPI 应用 ==============

app = FastAPI(title="博客AI发布助手", version="1.0.0")

# 挂载静态文件目录
import pathlib
STATIC_DIR = pathlib.Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ============== 企业微信验证 ==============

def verify_wecom_signature(signature: str, timestamp: str, nonce: str, token: str) -> bool:
    """验证企业微信消息签名"""
    if not signature or not timestamp or not nonce:
        return False
    sorted_list = sorted([token, timestamp, nonce])
    sha1 = hashlib.sha1("".join(sorted_list).encode()).hexdigest()
    return hmac.compare_digest(sha1, signature)

# ============== 数据模型 ==============

class WeComMessage(BaseModel):
    """企业微信消息格式"""
    msg_type: str = "text"
    content: str = ""

class BlogRequest(BaseModel):
    """博客生成请求"""
    topic: str
    category: str = DEFAULT_CATEGORY
    tags: list = []
    auto_publish: bool = False  # 是否自动发布（不走PR审核）

# ============== LLM 调用 ==============

def generate_blog_content(topic: str, category: str = DEFAULT_CATEGORY) -> dict:
    """
    调用 LLM API 生成博客文章内容
    返回: {"title": "...", "content": "...", "filename": "..."}
    """
    prompt = f"""你是一个技术博客作者，擅长写简洁实用、深入浅出的技术文章。

请根据以下主题写一篇 Hugo 博客文章：

主题：{topic}
分类：{category}

要求：
1. 使用 Markdown 格式
2. 文章标题用 h1 级别
3. 包含适当的代码示例（用 ``` 包裹）
4. 字数控制在 800-1500 字
5. 风格：简洁实用，适合技术读者
6. 内容要有深度，避免泛泛而谈

请直接输出文章内容，不需要任何前缀说明。"""

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    with httpx.Client(timeout=120.0) as client:
        response = client.post(LLM_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"LLM API 调用失败: {response.text}")

    result = response.json()
    content = result["choices"][0]["message"]["content"].strip()

    # 生成文件名（从标题提取slug）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else topic
    slug = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+', '-', title).strip('-').lower()
    filename = f"{slug}.md"

    # 生成 frontmatter
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    frontmatter = f"""---
title: "{title}"
date: {now}
lastmod: {now}
categories: [{category}]
tags: []
draft: true
---

"""

    # 去掉标题（因为已在frontmatter中）
    body = re.sub(r'^#\s+.+\n+', '', content, count=1)

    return {
        "title": title,
        "content": frontmatter + body,
        "filename": filename,
        "category": category
    }

# ============== GitHub API ==============

def create_github_pr(title: str, content: str, filename: str, category: str) -> dict:
    """
    创建 GitHub Pull Request:
    1. 从 master 创建新分支 ai/xxx
    2. 在新分支上提交文件
    3. 创建 PR: ai/xxx -> master
    """
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN 未配置")

    file_path = f"content/{category}/{filename}"
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 新分支名称（ai/slug-timestamp）
    slug = re.sub(r'[^\w-]', '-', filename.replace('.md', ''))[:40]
    branch_name = f"ai/{slug}-{int(time.time())}"

    with httpx.Client(timeout=30.0) as client:
        # 1. 获取 master 分支的最新 commit SHA
        master_resp = client.get(f"{repo_url}/git/ref/heads/{GITHUB_BRANCH}", headers=headers)
        if master_resp.status_code != 200:
            raise HTTPException(status_code=500, detail=f"获取分支失败: {master_resp.text}")
        master_sha = master_resp.json()["object"]["sha"]

        # 2. 创建新分支
        branch_resp = client.post(f"{repo_url}/git/refs", headers=headers, json={
            "ref": f"refs/heads/{branch_name}",
            "sha": master_sha
        })
        if branch_resp.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=f"创建分支失败: {branch_resp.text}")

        # 3. 在新分支上提交文件
        file_url = f"{repo_url}/contents/{file_path}"
        put_response = client.put(file_url, headers=headers, json={
            "message": f"AI生成文章: {title}",
            "content": base64.b64encode(content.encode('utf-8')).decode('ascii'),
            "branch": branch_name
        })
        if put_response.status_code not in (200, 201):
            raise HTTPException(status_code=500, detail=f"提交文件失败: {put_response.text}")

        # 4. 创建 PR
        pr_body = f"""## 📝 博客文章草稿（AI生成）

**主题**: {title}
**分类**: {category}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
> 🤖 此 PR 由 AI 自动生成，请审核内容后合并发布到博客。
"""
        pr_response = client.post(f"{repo_url}/pulls", headers=headers, json={
            "title": f"📝 {title}",
            "body": pr_body,
            "head": branch_name,
            "base": GITHUB_BRANCH
        })

    if pr_response.status_code == 201:
        pr_result = pr_response.json()
        return {
            "status": "success",
            "pr_url": pr_result.get("html_url"),
            "pr_number": pr_result.get("number"),
            "file_path": file_path,
            "branch": branch_name
        }
    else:
        return {
            "status": "pr_failed",
            "detail": pr_response.text
        }

# ============== 企业微信消息处理 ==============

def send_wecom_notification(message: str):
    """发送消息到企业微信群"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": message
        }
    }

    with httpx.Client(timeout=10.0) as client:
        response = client.post(WECOM_BOT_WEBHOOK, json=payload)

    return response.status_code == 200

# ============== API 路由 ==============

@app.get("/")
async def root():
    """根路径重定向到 Web 界面"""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"status": "ok", "service": "博客AI发布助手", "ui": "/static/index.html"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/webhook/wechat")
async def wechat_webhook(request: Request):
    """
    接收企业微信群机器人 webhook 推送的消息
    """
    # 获取请求体
    body = await request.json()

    # 解析消息内容（企业微信群消息格式）
    msg_type = body.get("msg_type", "")
    content = body.get("content", "")

    # 只处理文本消息
    if msg_type != "text" or not content:
        return JSONResponse(content={"status": "ignored", "reason": "非文本消息"})

    # 去掉 @ 提及（如果消息包含）
    content = content.strip()

    # 忽略空消息
    if not content or len(content) < 3:
        return JSONResponse(content={"status": "ignored", "reason": "消息内容太短"})

    # 判断是否为博客生成指令（以 "写博客:" 或 "博客:" 开头）
    is_blog_cmd = any(content.startswith(prefix) for prefix in ["写博客:", "博客:", "生成:"])

    if not is_blog_cmd:
        return JSONResponse(content={"status": "ignored", "reason": "非博客生成指令"})

    # 提取主题
    topic = content
    for prefix in ["写博客:", "博客:", "生成:"]:
        if content.startswith(prefix):
            topic = content[len(prefix):].strip()
            break

    # 发送处理中通知
    send_wecom_notification(f"🤖 正在生成文章：**{topic}**\n> 请稍候...")

    try:
        # 生成博客内容
        result = generate_blog_content(topic)

        # 创建 GitHub PR
        pr_result = create_github_pr(
            title=result["title"],
            content=result["content"],
            filename=result["filename"],
            category=result["category"]
        )

        if pr_result["status"] == "success":
            response_msg = f"""✅ 文章已生成并提交 PR！

**标题**: {result['title']}
**文件**: `content/{result['category']}/{result['filename']}`
**PR链接**: {pr_result['pr_url']}

请审核后合并到 master 分支，GitHub Actions 将自动构建发布到博客。"""
        else:
            response_msg = f"""⚠️ 文章生成完成但 PR 创建失败：

{json.dumps(pr_result, ensure_ascii=False, indent=2)}"""

        send_wecom_notification(response_msg)

        return JSONResponse(content={
            "status": "success",
            "title": result["title"],
            "filename": result["filename"],
            "pr_url": pr_result.get("pr_url")
        })

    except Exception as e:
        error_msg = f"""❌ 文章生成失败！

**错误**: {str(e)}

请检查配置或稍后重试。"""
        send_wecom_notification(error_msg)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_blog(req: BlogRequest):
    """
    直接 API 调用生成博客（不经过企微 webhook）
    """
    try:
        result = generate_blog_content(req.topic, req.category)

        if req.auto_publish:
            # 直接提交到 master（跳过 PR）
            pass  # 暂不实现自动发布

        pr_result = create_github_pr(
            title=result["title"],
            content=result["content"],
            filename=result["filename"],
            category=result["category"]
        )

        return JSONResponse(content={
            "status": "success",
            "title": result["title"],
            "filename": result["filename"],
            "category": result["category"],
            "pr_url": pr_result.get("pr_url")
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== 启动 ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
