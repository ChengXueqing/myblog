#!/bin/bash
# dual-push-deploy: Hugo 博客双推部署脚本
# 用法: bash deploy.sh "feat: 提交说明"

set -e

BLOG_DIR="/workspace/myblog"
COMMIT_MSG="${1:-feat: 博客内容更新}"

echo "==> 1. 构建 Hugo 站点..."
cd "$BLOG_DIR"
hugo --minify 2>&1 | tail -5

if [ $? -ne 0 ]; then
  echo "❌ Hugo 构建失败，请检查错误信息"
  exit 1
fi

echo ""
echo "==> 2. 提交变更..."
git add -A
if git diff --staged --quiet; then
  echo "   ℹ️  没有新的变更需要提交，跳过 commit"
else
  git commit -m "$COMMIT_MSG"
  echo "   ✅ 已提交: $COMMIT_MSG"
fi

echo ""
echo "==> 3. 推送到 GitHub (Pages)..."
git push github master
echo "   ✅ GitHub 推送完成"

echo ""
echo "==> 4. 推送到 Gitee (国内镜像)..."
git push origin master
echo "   ✅ Gitee 推送完成"

echo ""
echo "🎉 双推部署完成！"
echo "   访问: https://chengxueqing.github.io/myblog/"
