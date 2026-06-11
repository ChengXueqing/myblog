---

title: "Python 列表推导式入门"
date: 2026-06-11T08:30:42+08:00
lastmod: 2026-06-11T08:30:42+08:00
categories: [basic]
tags: []
draft: true

description: "Python 列表推导式的基础用法和常见场景"

slug: "python-列表推导式入门"
---
列表推导式（List Comprehension）是 Python 中一种简洁高效的创建列表的方法。它可以用一行代码替代传统的多行循环语句，让你的代码更加 Pythonic。本文将深入介绍列表推导式的语法、常见用法以及一些高级技巧。

## 什么是列表推导式

列表推导式的基本语法如下：

```python
[expression for item in iterable if condition]
```

这相当于：

```python
result = []
for item in iterable:
    if condition:
        result.append(expression)
```

让我们看一个简单的例子：将 0-9 的数字平方后放入列表。

传统写法：
```python
squares = []
for i in range(10):
    squares.append(i**2)
```

列表推导式写法：
```python
squares = [i**2 for i in range(10)]
```

## 基础用法

### 1. 简单的数值转换

```python
# 将华氏度列表转换为摄氏度
fahrenheit = [32, 68, 86, 104]
celsius = [(f-32)*5/9 for f in fahrenheit]
print(celsius)  # [0.0, 20.0, 30.0, 40.0]
```

### 2. 带条件的筛选

```python
# 只保留偶数
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
evens = [n for n in numbers if n % 2 == 0]
print(evens)  # [2, 4, 6, 8]
```

### 3. 双重循环

```python
# 生成笛卡尔积
colors = ['red', 'green']
sizes = ['S', 'M', 'L']
products = [(color, size) for color in colors for size in sizes]
print(products)
# [('red', 'S'), ('red', 'M'), ('red', 'L'), 
#  ('green', 'S'), ('green', 'M'), ('green', 'L')]
```

## 进阶用法

### 1. 嵌套列表推导式

```python
# 展平二维列表
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(flattened)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 2. 条件表达式

可以在表达式部分使用 if-else：

```python
# 将负数替换为0
numbers = [-5, 3, -2, 7, 0]
non_negative = [n if n >= 0 else 0 for n in numbers]
print(non_negative)  # [0, 3, 0, 7, 0]
```

### 3. 字典和集合推导式

类似的语法也可以用于创建字典和集合：

```python
# 字典推导式
words = ['hello', 'world', 'python']
length_dict = {word: len(word) for word in words}
print(length_dict)  # {'hello': 5, 'world': 5, 'python': 6}

# 集合推导式
unique_lengths = {len(word) for word in words}
print(unique_lengths)  # {5, 6}
```

## 性能考虑

列表推导式通常比等价的循环更快，主要有两个原因：

1. Python 解释器对列表推导式有专门的优化
2. 避免了频繁的 `append()` 方法调用

让我们用一个简单的性能测试来验证：

```python
import timeit

# 传统循环
def loop_style():
    result = []
    for i in range(1000):
        result.append(i**2)
    return result

# 列表推导式
def comprehension_style():
    return [i**2 for i in range(1000)]

print(timeit.timeit(loop_style, number=10000))      # 约1.2秒
print(timeit.timeit(comprehension_style, number=10000))  # 约0.8秒
```

## 何时不使用列表推导式

虽然列表推导式很强大，但并不是所有情况都适用：

1. **可读性降低时**：如果逻辑过于复杂，使用普通循环可能更清晰
2. **需要副作用时**：如果循环内有其他操作（如打印、修改外部变量等）
3. **处理大数据时**：列表推导式会立即创建整个列表，可能占用大量内存

对于大数据集，考虑使用生成器表达式：

```python
# 生成器表达式（惰性求值）
large_data = (x**2 for x in range(1000000))
```

## 实践建议

1. 保持简洁：如果推导式超过两行，考虑使用传统循环
2. 避免多层嵌套：超过两层的嵌套会降低可读性
3. 合理使用条件：复杂的条件逻辑可以拆分成多步
4. 注意作用域：推导式中的变量会"泄漏"到当前作用域（Python 3中已修复）

## 总结

列表推导式是 Python 中强大而优雅的特性，合理使用可以：
- 使代码更简洁
- 提高执行效率
- 增强可读性（在适当的情况下）

掌握列表推导式是成为 Python 高手的必经之路。建议在实际项目中多加练习，但也要记住"可读性为王"的原则，在复杂场景下适时选择传统循环写法。