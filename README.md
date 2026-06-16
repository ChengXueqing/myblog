# 清净心

> 一个简单的技术博客

个人技术积累与生活思考的记录站，基于 **Hugo** + **PaperMod** 主题，部署在 GitHub Pages。

## 访问入口

- **线上地址**：https://chengxueqing.github.io/myblog/
- **源码仓库（GitHub）**：https://github.com/ChengXueqing/myblog
- **镜像仓库（Gitee）**：https://gitee.com/chengxueqing/myblog

---

## 目录结构

```
content/
├── tech/              # 技术升级主线
│   ├── basics/       # 通用基础（JS、工具等）
│   ├── frontend/     # 前端开发（Vue、React、CSS）
│   ├── engineering/  # 工程化（构建、规范、Git）
│   ├── interview/    # 面试准备
│   └── ai/           # AI 全栈
└── mind/             # 个人发展
    ├── dao/          # 道法自然（道家、中医、易经）
    ├── poetry/       # 诗词欣赏（古文、唐诗宋词）
    ├── yijing/       # 易经六十四卦
    ├── misc/         # 杂项（影视台词、观念言论）
    └── reflection/   # 反思总结
```

---

## 本地开发

### 前置条件

- [Hugo v0.146.0+](https://gohugo.io/installation/)
- [Git](https://git-scm.com/)

### 本地预览

```bash
git clone https://github.com/ChengXueqing/myblog.git
cd myblog
hugo server --buildFuture
```

访问 http://localhost:1313/myblog/ 查看效果。

### 构建静态文件

```bash
hugo --minify
```

生成的静态文件在 `public/` 目录。

---

## 自动部署

推送到 `master` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages：

```
git push github master   # 推送到 GitHub（触发部署）
git push origin master  # 推送到 Gitee（镜像备份）
```

---

## 写作

在 `content/` 对应目录下新建 `.md` 文件，Front Matter 格式：

```yaml
---
title: "文章标题"
date: 2026-06-16T12:00:00+08:00
description: "文章摘要"
tags: ["标签1", "标签2"]
categories: ["分类"]
slug: "url-slug"
---
```

---

## License

MIT License
