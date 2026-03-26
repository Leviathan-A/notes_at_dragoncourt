---
title: C++ Primer 学习地图
type: knowledge
tags: [knowledge, cpp]
created: 2026-03-25
---

# C++ Primer 学习地图

## 一句话定义
- 这是一份把 C++ Primer 零散笔记整理成“主题索引 + 复习路径”的导航页。

## 主题索引
- 输入输出与字符串处理：`getline`、`istringstream`、`ostringstream`。
- STL 容器与迭代器：关联容器、无序容器、插入迭代器、IO 迭代器。
- 泛型与算法：去重、谓词、lambda、bind、命名规则。
- 动态内存与智能指针：`shared_ptr`、`unique_ptr`、`weak_ptr`、`allocator`。
- 拷贝控制与对象移动：值语义/指针语义、copy-and-swap、右值引用。
- 类设计细节与语法边界：初始化顺序、`explicit`、`decltype`、`const_cast`。

## 推荐复习顺序
1. 先复习“容器 + 算法”主线，建立日常编码骨架。
2. 再复习“智能指针 + 拷贝控制 + 移动语义”，理解资源管理。
3. 最后回看“类设计细节与语法边界”，巩固工程实践。

## 适用场景
- 面试前快速回顾 C++ 核心知识。
- 写项目代码前进行 API/语义查漏补缺。

## 常见误区
- 只记 API，不理解失效规则（迭代器/引用/指针）。
- 混淆值语义与所有权语义，导致拷贝/移动行为错误。
- 记住语法却忽略“何时用、为何用”。

## 参考来源
- [[05-Resources/C++Primer-原始笔记]]

## 关联项目
- [[02-Projects/知识库自动化]]

## 相关概念
- [[03-Knowledge/Git 冲突最小化策略]]
