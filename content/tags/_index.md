---
title: "标签云"
layout: "taxonomy"
description: "所有文章标签，按文章数量显示"
---

<style>
.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem 1.2rem;
  justify-content: center;
  padding: 2rem 0;
}
.tags-cloud a {
  color: var(--primary);
  text-decoration: none;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  transition: all 0.2s;
}
.tags-cloud a:hover {
  background: var(--entry);
  color: var(--content);
}
.tags-cloud .tag-count {
  font-size: 0.75rem;
  color: var(--secondary);
  margin-left: 0.2rem;
}
</style>

<div class="tags-cloud" id="tags-cloud">
加载中...
</div>

<script>
// 从 index.json 读取标签数据，生成标签云
fetch('/myblog/index.json')
  .then(r => r.json())
  .then(data => {
    const tagCounts = {};
    data.forEach(item => {
      (item.tags || []).forEach(tag => {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      });
    });

    const container = document.getElementById('tags-cloud');
    container.innerHTML = '';

    // 按文章数量排序
    const sorted = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]);

    sorted.forEach(([tag, count]) => {
      const a = document.createElement('a');
      a.href = `/myblog/tags/${tag}/`;
      // 根据数量设置字体大小
      const size = Math.min(1 + count * 0.15, 2.2);
      a.style.fontSize = `${size}rem`;
      a.style.fontWeight = count >= 3 ? '600' : '400';

      const text = document.createTextNode(tag);
      a.appendChild(text);

      const countSpan = document.createElement('span');
      countSpan.className = 'tag-count';
      countSpan.textContent = count;
      a.appendChild(countSpan);

      container.appendChild(a);
    });
  })
  .catch(() => {
    document.getElementById('tags-cloud').innerHTML = '加载失败，请刷新页面重试。';
  });
</script>
