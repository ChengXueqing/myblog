---

title: "vue router跳转传参"
date: 2018-03-13T14:07:36+08:00
lastmod: 2018-03-13T14:07:36+08:00
categories: [frontend]
tags: []

description: "Vue Router 中页面跳转传参的几种方式"

summary: "Vue Router 中页面跳转传参的几种方式"

slug: "vue-router-params"
---
http://blog.csdn.net/qq_15646957/article/details/78070862

发送页面this.$router
接收页面this.$route

```
this.$router.push({
path: '',
query: {
key: value
}
})

----or------

this.$router.push({
name: '', //routes中要配置name名称
params: { //有params时，不能用path,
key: value
}
})
```