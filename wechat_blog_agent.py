"""
企业微信群机器人 webhook 接收服务
接收消息 → AI生成博客内容 → 自动创建 GitHub PR

依赖: pip install -r requirements.txt
运行: python wechat_blog_agent.py
"""

import os
import re
import hashlib
import hmac
import time
import json
from datetime import datetime
from typing import Optional

import requests
from fastapi import FastAPI, Request, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
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

    with httpx.Client(timeout=60.0) as client:
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
    创建 GitHub Pull Request
    """
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GITHUB_TOKEN 未配置")

    # 决定文件路径
    file_path = f"content/{category}/{filename}"

    # 获取仓库信息
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 检查文件是否已存在
    file_url = f"{repo_url}/contents/{file_path}"
    params = {"ref": GITHUB_BRANCH}

    with httpx.Client(timeout=30.0) as client:
        # 尝试获取现有文件（用于更新场景）
        existing = client.get(file_url, headers=headers, params=params)
        sha = existing.json().get("sha") if existing.status_code == 200 else None

        # 创建新文件或更新
        commit_message = f"AI生成文章: {title}"

        file_content = {
            "message": commit_message,
            "content": content.encode('utf-8').hex(),  # GitHub API 需要 hex 编码
            "branch": GITHUB_BRANCH
        }
        if sha:
            file_content["sha"] = sha

        put_response = client.put(file_url, headers=headers, json=file_content)

    if put_response.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail=f"GitHub API 调用失败: {put_response.text}")

    result = put_response.json()

    # 创建 PR（如果文件不存在或需要审核流程）
    pr_title = f"📝 {title}"
    pr_body = f"""## 博客文章草稿

**主题**: {title}
**分类**: {category}
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 文章预览
请在 [文件列表](https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/{file_path}) 中查看完整内容。

---
> 🤖 此 PR 由 AI 自动生成，请审核后合并发布。
"""

    pr_url = f"{repo_url}/pulls"
    pr_data = {
        "title": pr_title,
        "body": pr_body,
        "head": GITHUB_BRANCH,  # PR 从哪个分支
        "base": GITHUB_BRANCH   # PR 合并到哪个分支
    }

    with httpx.Client(timeout=30.0) as client:
        pr_response = client.post(pr_url, headers=headers, json=pr_data)

    if pr_response.status_code == 201:
        pr_result = pr_response.json()
        return {
            "status": "success",
            "pr_url": pr_result.get("html_url"),
            "pr_number": pr_result.get("number"),
            "file_path": file_path
        }
    elif pr_response.status_code == 422:  # PR 已存在
        return {
            "status": "already_exists",
            "message": "该文章已存在，请先删除或修改后再试"
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
    return {"status": "ok", "service": "博客AI发布助手"}

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
