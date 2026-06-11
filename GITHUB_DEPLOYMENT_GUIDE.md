# 博客部署到 GitHub Pages - 操作指南

## 概述
本指南将帮助你将 Hugo 博客从 Gitee 迁移部署到 GitHub Pages。

**前置条件**：
- ✅ 博客代码已准备就绪（位于 `/workspace/myblog/`）
- ✅ Hugo 配置文件已更新（`baseURL` 已改为 `https://chengxueqing.github.io/myblog/`）
- ✅ GitHub Actions 工作流已配置（`.github/workflows/hugo.yml`）
- ⚠️ 需要你的操作：在 GitHub 网页上创建仓库并开启 Pages

---

## 步骤 1：在 GitHub 创建仓库

1. 访问 [GitHub](https://github.com/) 并登录你的账号（chengxueqing）
2. 点击右上角 `+` → `New repository`
3. 填写仓库信息：
   - **Repository name**: `myblog`（必须叫这个名字，与 hugo.toml 中的 baseURL 对应）
   - **Description**: `清净心 - 个人技术博客 (Hugo + GitHub Pages)`
   - **Public/Private**: 选择 `Public`（GitHub Pages 需要公开仓库）
   - **⚠️ 重要**: **不要**勾选 `Initialize this repository with a README`（保持空仓库）
4. 点击 `Create repository`

创建成功后，GitHub 会显示一个快速设置页面，先不要关闭。

---

## 步骤 2：推送代码到 GitHub

在 CodeBuddy 终端中执行以下命令（我帮你准备好脚本了）：

```bash
cd /workspace/myblog

# 添加 GitHub 远程仓库（替换 <your-github-username> 为你的用户名）
git remote add github https://github.com/chengxueqing/myblog.git

# 或者使用 SSH（如果你配置了 SSH key）
# git remote add github git@github.com:chengxueqing/myblog.git

# 推送代码到 GitHub（首次推送）
git push -u github master
```

**如果遇到认证问题**：
- GitHub 会提示你输入用户名和密码
- **⚠️ 注意**：密码字段需要输入 [Personal Access Token](https://github.com/settings/tokens)，不是登录密码
- 推荐：创建一个有 `repo` 权限的 Token

---

## 步骤 3：开启 GitHub Pages

推送代码后，需要在 GitHub 仓库设置中启用 Pages：

1. 访问你的 GitHub 仓库：`https://github.com/chengxueqing/myblog`
2. 点击 `Settings`（设置）标签
3. 在左侧菜单找到 `Pages`
4. 在 `Build and deployment` 部分：
   - **Source**: 选择 `GitHub Actions`（我们已经配置好了工作流）
5. 保存设置

GitHub Actions 会自动触发第一次构建和部署。

---

## 步骤 4：验证部署

1. 访问 `https://chengxueqing.github.io/myblog/`
2. 等待 1-3 分钟让 GitHub Actions 完成首次构建
3. 如果页面显示正常，恭喜！部署成功 🎉

**查看部署进度**：
- 进入仓库的 `Actions` 标签
- 点击最新的 workflow run
- 查看构建日志

---

## 常见问题

### Q1: 推送代码时提示认证失败？
**A**: GitHub 已不支持密码认证，需要使用 Personal Access Token：
1. 访问 [GitHub Token 设置](https://github.com/settings/tokens)
2. 点击 `Generate new token` → `Generate new token (classic)`
3. 勾选 `repo` 权限
4. 生成后复制 token，在密码字段输入这个 token

### Q2: GitHub Pages 显示 404？
**A**: 可能原因：
1. Actions 工作流还没运行完，等待 1-3 分钟
2. 仓库是 Private 的，需要改为 Public
3. `baseURL` 配置错误，检查 `hugo.toml` 中的 URL 是否匹配

### Q3: 博客样式丢失/显示不正常？
**A**: 通常是 `baseURL` 配置问题，确保：
- `hugo.toml` 中的 `baseURL = "https://chengxueqing.github.io/myblog/"`
- `.github/workflows/hugo.yml` 中的 `--baseURL` 参数与上面一致

---

## 附加说明

### 双远程仓库配置（可选）
如果你还想保留 Gitee 仓库，可以配置多个远程仓库：

```bash
# 查看当前远程仓库
git remote -v

# 推送到 Gitee
git push origin master

# 推送到 GitHub
git push github master
```

### 自动部署流程
配置完成后，每次向 `master` 分支推送代码，GitHub Actions 会自动：
1. 拉取代码
2. 安装 Hugo
3. 构建静态站点
4. 部署到 GitHub Pages

无需手动操作！

---

## 下一步

部署成功后，你可以：
1. ✅ 测试博客 AI 发布系统（应该会自动推送到 GitHub）
2. ✅ 自定义域名（可选）
3. ✅ 配置 Disqus 评论系统（可选）
4. ✅ 开启 Google Analytics（可选）

---

**需要帮助？** 随时问我 🙌
