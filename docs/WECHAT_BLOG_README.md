# 博客 AI 发布助手

通过企业微信群机器人，在手机上发送主题即可自动生成博客文章并提交 PR。

## 功能特性

- 📱 **手机端创作**：在企业微信群发送主题，AI 自动生成文章
- 🤖 **AI 驱动**：调用 LLM API 生成符合 Hugo 格式的 Markdown 文章
- 🔄 **PR 审核流程**：自动创建 GitHub PR，支持移动端审核后发布
- ⚡ **自动化部署**：PR 合并后 GitHub Actions 自动构建并发布到博客

## 快速开始

### 1. 克隆并安装依赖

```bash
git clone https://gitee.com/chengxueqing/myblog.git
cd myblog
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入实际配置
```

必需配置项：

| 变量 | 说明 | 获取方式 |
|------|------|----------|
| `WECOM_BOT_WEBHOOK` | 企微机器人 webhook URL | 企微群机器人设置 |
| `LLM_API_KEY` | LLM API 密钥 | DeepSeek / 硅基流动控制台 |
| `GITHUB_TOKEN` | GitHub Personal Access Token | GitHub Settings → Developer settings |

### 3. 启动服务

```bash
python start_server.py
# 或直接运行
python wechat_blog_agent.py
```

服务启动后会监听 `http://0.0.0.0:7860`

### 4. 配置企业微信群机器人

#### 4.1 创建群机器人

1. 打开企业微信 → 进入任意群聊 → 点击右上角「...」
2. 群机器人 → 添加机器人 → 输入名称（如"博客助手"）
3. 复制机器人 Webhook URL 中的 `key=` 后面的值

#### 4.2 配置接收消息（关键步骤）

⚠️ **注意**：企微群机器人默认只有**发送**权限，要接收消息需要：

1. 在企微管理后台开启「接收消息」功能
2. 配置消息接收地址为你的服务地址（如 `https://your-domain.com/webhook/wechat`）
3. 设置「调用API」权限

**简化方案**：使用企业微信的**自建应用**模式：

1. 登录企业微信管理后台 → 应用管理 → 创建应用
2. 设置应用的「企业微信授权登录」或「API接收消息」
3. 获取 `corp_id` 和 `agent_id` 配置到应用

#### 4.3 测试 webhook

在 Cloud Studio 或服务器上启动服务后，用 curl 测试：

```bash
curl -X POST http://localhost:7860/webhook/wechat \
  -H "Content-Type: application/json" \
  -d '{"msg_type":"text","content":"博客: 测试文章主题"}'
```

## 使用方式

### 在企微群发送命令

```
写博客: Python异步编程实战指南
博客: Go语言并发模型解析
生成: Docker容器化最佳实践
```

### 可选参数

在命令后附加分类标签：

```
写博客: Python异步编程 @advanced
博客: Docker容器化 @engineering
```

支持的分类：`basic`、`advanced`、`interview`、`engineering`、`others`

## 自动化部署

### GitHub Actions（已有配置）

博客已配置 GitHub Actions 自动化部署：

- 触发条件：推送到 `master` 分支 或手动触发
- 构建命令：`hugo --minify`
- 部署地址：https://chengxueqing.github.io/

### Gitee Pages 同步（可选）

如果也需要同步部署到 Gitee Pages：

1. 在 Gitee 仓库设置中开启 Gitee Pages
2. 在 GitHub Actions 中添加 Gitee Pages 部署步骤

## 目录结构

```
myblog/
├── wechat_blog_agent.py    # 主服务（FastAPI）
├── start_server.py         # 启动脚本
├── requirements.txt         # Python 依赖
├── .env.example            # 环境变量模板
├── hugo.toml               # Hugo 配置
├── content/                # 博客文章
│   ├── basic/
│   ├── advanced/
│   ├── interview/
│   ├── engineering/
│   └── others/
├── .github/
│   └── workflows/
│       └── hugo.yml        # GitHub Actions 配置
└── static/                 # 静态资源
```

## 常见问题

### Q: 服务部署在哪里？

**推荐**：使用 Cloud Studio 的常驻任务功能，将 `start_server.py` 作为常驻服务运行。

### Q: 如何确保服务持续运行？

使用 `nohup` 或配置 systemd/supervisor：

```bash
nohup python start_server.py > app.log 2>&1 &
```

### Q: LLM 生成的内容不满意怎么办？

修改 `wechat_blog_agent.py` 中的 `generate_blog_content()` 函数的 prompt 提示词，调整生成风格。

### Q: 能否直接发布而不走 PR 审核？

将 `draft: true` 改为 `draft: false` 即可自动发布。但**不推荐**，建议保持 PR 审核流程以确保文章质量。

## API 参考

### POST /webhook/wechat

企业微信 webhook 接收端点

**请求体**：
```json
{
  "msg_type": "text",
  "content": "写博客: 你的主题"
}
```

### POST /api/generate

直接 API 调用

**请求体**：
```json
{
  "topic": "Python异步编程实战指南",
  "category": "basic",
  "tags": ["Python", "异步"],
  "auto_publish": false
}
```

**响应**：
```json
{
  "status": "success",
  "title": "Python异步编程实战指南",
  "filename": "python-yibu-biancheng-shizhan-zhinan.md",
  "category": "basic",
  "pr_url": "https://github.com/ChengXueqing/myblog/pull/123"
}
```
