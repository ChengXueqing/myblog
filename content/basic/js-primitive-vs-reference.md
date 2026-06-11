---

title: "ECMAScript基本类型值和引用类型值的区别"
date: 2018-04-10T18:33:11+08:00
lastmod: 2018-04-10T18:33:11+08:00
categories: [basic]
tags: []

description: "深入理解 ECMAScript 中基本类型值和引用类型值在保存方式和复制方式上的区别"

slug: "js-primitive-vs-reference"

aliases: ["/basic/js-primitive-vs-reference/"]
---
ECMAScript中，变量分为**基本类型值**和**引用类型值**，两者的区别如下：

**一、 保存方式不同**
- 基础类型值，长度不可变，保存在“栈”中
- 引用类型值，长度可变，保存在“堆”中


**二、 复制方式不同**
 - 基础类型值：在“栈”中创建副本，再把新值分配到新的位置上，如下图所示，

![基础类型值的复制过程](/images/basic/primitive-vs-reference-1.jpg)
 - 引用类型值：在“栈”中创建副本，这个副本实际上是一个**指针**，指向“堆”中的一个对象，如下图所示，

![引用类型值的复制过程](/images/basic/primitive-vs-reference-2.jpg)