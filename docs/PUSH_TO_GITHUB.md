# 快速推送代码到 GitHub

## 方法 1：使用 gh CLI（推荐，最简单）

在 CodeBuddy 终端执行以下命令：

```bash
# 1. 认证 GitHub（会弹出浏览器窗口）
cd /workspace/myblog
gh auth login --web

# 按提示操作：
# - 选择 GitHub.com
# - 选择 HTTPS
# - 选择 Login with a web browser
# - 复制 one-time code
# - 在浏览器中粘贴 code 并授权

# 2. 推送代码
git push -u github master
```

---

## 方法 2：使用 Personal Access Token

如果你已经有 Token，直接执行：

```bash
cd /workspace/myblog

# 设置远程仓库 URL（包含 Token）
git remote set-url github https://chengxueqing:<EMAIL_REMOVED>/chengxueqing/myblog.git

# 推送代码
git push -u github master
```

**如何获取 Token**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成后复制 Token

---

## 方法 3：使用 SSH（如果你已配置 SSH Key）

```bash
cd /workspace/myblog

# 修改为 SSH URL
git remote set-url github <EMAIL_REMOVED>:chengxueqing/myblog.git

# 推送代码
git push -u github master
```

---

## 推送成功后

1. 访问：https://github.com/chengxueqing/myblog/settings/pages
2. Source 选择：**GitHub Actions**
3. 等待 1-3 分钟
4. 访问博客：**https://chengxueqing.github.io/myblog/**

---

## 最直接的方式（复制粘贴运行）

```bash
cd /workspace/myblog && gh auth login --web
# 完成浏览器认证后
git push -u github master
```

然后告诉我推送结果，我来帮你开启 GitHub Pages 并给你博客地址！
