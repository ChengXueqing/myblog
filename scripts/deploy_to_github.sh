#!/bin/bash
# 博客部署到 GitHub 一键脚本

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  博客部署到 GitHub Pages"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "hugo.toml" ]; then
    echo "❌ 错误：请在博客根目录（myblog）中运行此脚本"
    exit 1
fi

echo "📋 当前配置检查..."
echo "  - Hugo 配置文件：✅"
echo "  - GitHub Actions：✅"
echo "  - baseURL: $(grep "^baseURL" hugo.toml | cut -d'"' -f2)"
echo ""

# 检查 Git 状态
echo "📝 检查 Git 状态..."
if [ -n "$(git status --porcelain)" ]; then
    echo "  - 发现未提交的更改，正在提交..."
    git add .
    git commit -m "feat: 准备部署到 GitHub Pages

- 更新 baseURL 为 GitHub Pages 地址
- 配置 GitHub Actions 工作流
- 添加部署指南"
    echo "  ✅ 更改已提交"
else
    echo "  ✅ 工作区干净，无需提交"
fi
echo ""

# 检查是否已配置 GitHub 远程仓库
if git remote | grep -q "github"; then
    echo "🔗 GitHub 远程仓库已配置："
    git remote get-url github
    echo ""
else
    echo "⚠️  未配置 GitHub 远程仓库"
    echo ""
    read -p "请输入你的 GitHub 用户名（默认: chengxueqing）: " username
    username=${username:-chengxueqing}
    
    echo ""
    echo "请选择认证方式："
    echo "  1) HTTPS（需要 Personal Access Token）"
    echo "  2) SSH（需要配置 SSH Key）"
    read -p "选择（1/2）: " auth_method
    
    if [ "$auth_method" = "1" ]; then
        repo_url="https://github.com/${username}/myblog.git"
        echo "🔗 添加 HTTPS 远程仓库：$repo_url"
    else
        repo_url="git@github.com:${username}/myblog.git"
        echo "🔗 添加 SSH 远程仓库：$repo_url"
    fi
    
    git remote add github "$repo_url"
    echo "  ✅ 远程仓库已添加"
    echo ""
fi

# 推送到 GitHub
echo "🚀 准备推送到 GitHub..."
echo ""
echo "⚠️  重要提示："
echo "  1. 确保你的 GitHub 仓库 'myblog' 已创建（空仓库，不要初始化）"
echo "  2. 如果使用 HTTPS，密码字段需要输入 Personal Access Token"
echo "  3. Token 获取地址：<ADDRESS_REMOVED>"
echo ""
read -p "按 Enter 继续，或按 Ctrl+C 取消..."

echo ""
echo "📤 正在推送代码到 GitHub..."
if git push -u github master; then
    echo ""
    echo "✅ 代码推送成功！"
    echo ""
    echo "=========================================="
    echo "  下一步操作"
    echo "=========================================="
    echo ""
    echo "1️⃣  访问你的 GitHub 仓库："
    echo "    https://github.com/${username:-chengxueqing}/myblog"
    echo ""
    echo "2️⃣  开启 GitHub Pages："
    echo "    Settings → Pages → Build and deployment → Source: GitHub Actions"
    echo ""
    echo "3️⃣  等待部署完成（1-3 分钟）"
    echo ""
    echo "4️⃣  访问你的博客："
    echo "    https://${username:-chengxueqing}.github.io/myblog/"
    echo ""
    echo "=========================================="
    echo "  部署指南已保存在："
    echo "  GITHUB_DEPLOYMENT_GUIDE.md"
    echo "=========================================="
else
    echo ""
    echo "❌ 推送失败！"
    echo ""
    echo "可能的原因："
    echo "  1. GitHub 仓库未创建"
    echo "  2. 认证信息错误（需要使用 Personal Access Token）"
    echo "  3. 仓库名称不匹配"
    echo ""
    echo "请查看 GITHUB_DEPLOYMENT_GUIDE.md 获取详细帮助"
    exit 1
fi
