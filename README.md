# 清净心 - 技术博客

基于 Hugo + PaperMod 主题的个人技术博客，支持 GitHub Pages 和 Gitee Pages 双平台部署。

## 快速开始

### 1. 安装 Hugo

**Windows (使用 Chocolatey):**
```powershell
choco install hugo -y
```

**macOS:**
```bash
brew install hugo
```

**Linux:**
```bash
apt install hugo
```

验证安装：`hugo version`

### 2. 下载 PaperMod 主题

由于网络原因，GitHub 访问受限。请选择以下方式之一：

**方式一：手动下载（推荐）**
1. 访问 https://github.com/adityatelange/hugo-PaperMod/releases
2. 下载最新的 `hugo-PaperMod.zip`
3. 解压到 `themes/PaperMod` 目录

**方式二：Gitee 镜像**
```bash
git clone https://gitee.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

### 3. 本地预览

```bash
hugo server
```

访问 http://localhost:1313 查看博客。

### 4. 构建静态文件

```bash
hugo --minify
```

生成的静态文件在 `public/` 目录。

## 目录结构

```
myblog/
├── content/           # 博客文章
│   ├── basic/        # 前端基础
│   ├── advanced/      # 进阶之路
│   ├── interview/     # 面试题合集
│   ├── others/        # 诗和远方
│   └── engineering/   # 工程化
├── static/images/    # 静态图片
├── themes/PaperMod/  # 主题
├── hugo.toml        # Hugo 配置
└── .github/workflows/hugo.yml  # GitHub Actions 配置
```

## 部署说明

### GitHub Pages

推送到 GitHub 后，GitHub Actions 会自动构建并部署。

1. 将仓库推送到 GitHub
2. 在仓库 Settings → Pages 中启用 Pages
3. Source 选择 "GitHub Actions"

### Gitee Pages

1. 在 Gitee 仓库中启用「流水线」功能
2. 添加以下环境变量：
   - `GITEE_PASSWORD`: 你的 Gitee 私人令牌

Gitee 流水线配置示例：
```yaml
workflow:
  build:
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3

      - name: Build
        run: hugo --minify --baseURL "https://chengxueqing.gitee.io/"

      - name: Deploy to Gitee Pages
        run: |
          cd public
          git init
          git config user.name "chengxueqing"
          git config user.email "your@email.com"
          git add .
          git commit -m "deploy"
          git push -f https://${{ secrets.GITEE_PASSWORD }}@gitee.com/chengxueqing/myblog.git master:gh-pages
```

## 获取 Gitee 私人令牌

1. 登录 Gitee → 右上角头像 → 设置
2. 左侧菜单 → 私人令牌
3. 生成新令牌，勾选 `projects` 权限
4. 复制令牌并添加到 Gitee 流水线的环境变量中

## 写作指南

### 新建文章

```bash
hugo new content/[category]/new-post.md
```

例如：
```bash
hugo new content/basic/how-to-learn-css.md
```

### 文章 Front Matter

```yaml
---
title: "文章标题"
date: 2024-01-01T10:00:00+08:00
lastmod: 2024-01-01T10:00:00+08:00
categories: [basic]
tags: [CSS, 前端]
---
```

## 常见问题

### Q: Hugo 构建失败
A: 确保已正确安装 Hugo 和 PaperMod 主题

### Q: 图片不显示
A: 检查图片路径是否正确，放在 `static/images/` 目录下

### Q: Gitee Pages 部署失败
A: 检查私人令牌是否有效，以及仓库名称是否正确

## License

MIT License
