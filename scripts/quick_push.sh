#!/bin/bash
# 快速推送脚本 - 只需要粘贴你的 GitHub Token

echo "=========================================="
echo "  推送博客到 GitHub"
echo "=========================================="
echo ""
echo "请先获取 GitHub Personal Access Token："
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限"
echo "4. 生成后复制 token"
echo ""
read -p "请粘贴你的 GitHub Token: " token

if [ -z "$token" ]; then
    echo "❌ Token 不能为空"
    exit 1
fi

echo ""
echo "🔗 配置远程仓库..."
cd /workspace/myblog
git remote set-url github https://chengxueqing:${token}@github.com/chengxueqing/myblog.git

echo "🚀 推送代码到 GitHub..."
if git push -u github master; then
    echo ""
    echo "✅ 代码推送成功！"
    echo ""
    echo "=========================================="
    echo "  下一步：开启 GitHub Pages"
    echo "=========================================="
    echo ""
    echo "1. 访问: https://github.com/chengxueqing/myblog/settings/pages"
    echo "2. Source 选择: GitHub Actions"
    echo "3. 等待 1-3 分钟"
    echo "4. 访问博客: https://chengxueqing.github.io/myblog/"
    echo ""
else
    echo ""
    echo "❌ 推送失败，请检查 Token 是否正确"
    exit 1
fi
