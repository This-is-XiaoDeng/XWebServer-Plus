# Python Page

- 文件后缀：`.py`
- 嵌入式：否

## 概述

当用户访问一个 `.py` 文件时，XWebServer+ 会将文件内容作为 Python 代码执行（`exec()`）并获取输出作为页面内容

XWebServer+ 会忽略文件内所有 `sdk.`

## HelloWorld

### 源代码

```python
print("HelloWorld!")
```

### 浏览器显示内容

```html
HelloWorld!
```
