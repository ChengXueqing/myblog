---
name: dual-push-deploy
category: git-devops
description: >
  Hugo 博客双推部署 skill：自动执行 hugo 构建 → git commit → 同时 push 到 GitHub（Pages 生产环境）和 Gitee（国内镜像）两个远程仓库。
  user 说"发布"、"deploy"、"双推"、"推送"时触发。
---

# Dual Push Deploy（双推部署）

这个 skill 专为 `chengxueqing/myblog` Hugo 博客项目设计，
将内容构建并同时推送到 **GitHub（GitHub Pages 生产）** 和 **Gitee（国内镜像）** 两个远程仓库。

## 适用场景

- ✅ 博客文章写完后一键发布
- ✅ 修改配置/主题后同步双仓库
- ✅ 删除或更新文章后保持一致
- ✅ 用户说"发布"、"deploy"、"双推"、"推上去"

## 双仓库配置说明

| 远程名 | 地址 | 用途 |
|--------|------|------|
| `github` | `https://github.com/ChengXueqing/myblog.git` | GitHub Pages 生产环境 |
| `origin` | `https://gitee.com/chengxueqing/myblog.git` | 国内镜像（Gitee） |

> ⚠️ 每次部署必须 **同时 push 两个远程**，不能只推一个。

## 执行流程

### 第 1 步：构建验证

```bash
cd /workspace/myblog && hugo --minify
```

- 如果构建失败（有 Error），**必须先修复错误**，再继续
- 常见错误：`yaml: did not find expected key`（description 字段有未转义引号）
- 修复后再次构建，直到 `Total in XXX ms` 成功输出

### 第 2 步：提交变更

```bash
cd /workspace/myblog && git add -A && git commit -m "feat: <简洁的提交说明>"
```

- 提交说明用中文，格式：`feat: <内容简述>`
- 如果 `git status` 显示 `nothing to commit`，跳过此步

### 第 3 步：双推（必须两步都执行）

```bash
# 先推 GitHub
cd /workspace/myblog && git push github master

# 再推 Gitee
cd /workspace/myblog && git push origin master
```

- 两个 push **都必须执行**，不能省略 Gitee
- 如果某个 push 失败（网络问题），需要重试

### 第 4 步：向用户报告结果

推送完成后，告知用户：
- ✅ 构建是否成功（Pages 数量）
- ✅ GitHub push 结果
- ✅ Gitee push 结果
- 📊 新文章的访问链接（如适用）

## 注意事项

### 🔴 图片路径（容易出错！）

Hugo 的 `baseURL = "https://chengxueqing.github.io/myblog/"`，
所有 Markdown 里的图片路径 **必须带 `/myblog` 前缀**：

```markdown
✅ 正确：![图片](/myblog/images/finance/daily-chart/xxx.jpg)
❌ 错误：![图片](/images/finance/daily-chart/xxx.jpg)
```

**每次创建新文章时，必须检查图片路径是否包含 `/myblog` 前缀。**

### 🔴 YAML 引号转义

description 字段里如果出现中文引号（`"..."` 或 `'...'`），
会导致 YAML 解析失败。必须改成中文引号或删除引号：

```yaml
# ❌ 错误
description: "他说"你好"世界"

# ✅ 正确
description: "他说你好世界"
```

### 🔴 只操作 master 分支

这个项目只用 `master` 分支，不要切换到其他分支。

## 快速参考

| 命令 | 说明 |
|------|------|
| `hugo --minify` | 本地构建（输出在 `/workspace/myblog/public/`） |
| `git push github master` | 推送到 GitHub（触发 Pages 自动部署） |
| `git push origin master` | 推送到 Gitee |
| `git log --oneline -5` | 查看最近 5 条提交记录 |

## 示例对话

**用户**："帮我发布这篇文章"
**你**：执行构建 → 提交 → 双推 → 报告结果 + 文章链接

**用户**："双推一下"
**你**：直接执行第 2-3 步（假设构建已通过）

**用户**："图片显示 404"
**你**：检查图片路径是否带 `/myblog` 前缀，修复后重新双推
