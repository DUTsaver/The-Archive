---
title: "复几何与流形优化笔记测试"
date: 2026-09-07
author: "测试作者"
tags: ["数学", "Markdown测试"]
categories: ["测试笔记"]
---

# 这是一个测试文章（用于测试 GitHub Actions 格式检查）

本文用于测试仓库中的 **Markdown 自动格式化与检查工作流**（GitHub Actions）。

## 1. 基础语法测试

这是一段普通的测试文本。包含 **加粗**、*斜体* 以及 `行内代码`。

### 列表规范

- 列表项 1：光滑流形（Smooth Manifold）
- 列表项 2：黎曼度量（Riemannian Metric）
- 列表项 3：切空间与退撤（Tangent Space & Retraction）

> **提示**：引用块内的重要提醒事项。请确保引用块样式与网站主题一致。

---

## 2. 代码块高亮测试

```python
import numpy as np

def riemannian_gradient_descent(x, grad, step_size=0.01):
    """光滑流形上的简易梯度下降算法模拟"""
    # 映射回流形上的退撤 (Retraction)
    x_next = x - step_size * grad
    return x_next / np.linalg.norm(x_next)

print("流形优化算法组件测试成功！")
```

---

## 3. 数学公式与表格

### 常用流形优化符号表

| 符号 | 含义说明 | 所在空间 |
| :--- | :--- | :--- |
| $\mathcal{M}$ | 光滑流形 (Smooth Manifold) | - |
| $T_x\mathcal{M}$ | 点 $x$ 处的切空间 (Tangent Space) | 向量空间 |
| $\text{grad} f(x)$ | 黎曼梯度 (Riemannian Gradient) | $T_x\mathcal{M}$ |

---

## 4. 自动修复测试区（用于验证 markdownlint 能力）

*   列表中包含不规范的空格缩进
*   没有明确代码语言的块：
```
# 未声明语言的代码片段
val = 42
```
