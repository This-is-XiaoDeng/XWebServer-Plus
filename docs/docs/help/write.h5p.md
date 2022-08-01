# HTML with Python

- 文件后缀：`.h5p`
- 嵌入式：是

## 概述

当用户访问一个 `.h5p` 文件时，XWebServer+ 会作为Python文件执行 `<?py` `?>` 之间的内容（`exec()`），并将其替换为执行后输出

同时 XWebServer+ 会作为python文件执行 `<?pyeval` `>` 之间的内容（`eval()`）并将其替换为代码返回

XWebServer+ 会忽略文件内所有 `sdk.`

## HelloWorld

### 源代码

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charset="utf-8">
    </head>
    <body>
        <center>
            <h1>
                <?py
print("HelloWorld")
?>
            </h1>
        </center>
    </body>
</html>
```

### 访问返回

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charset="utf-8">
    </head>
    <body>
        <center>
            <h1>
                HelloWorld
            </h1>
        </center>
    </body>
</html>
```

## HelloWorld（pyeval）

### 源代码

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charset="utf-8">
    </head>
    <body>
        <center>
            <h1>
                <?pyeval "HelloWorld" >
            </h1>
        </center>
    </body>
</html>
```

### 访问返回

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charset="utf-8">
    </head>
    <body>
        <center>
            <h1>
                HelloWorld
            </h1>
        </center>
    </body>
</html>
```


## 注意事项

1. 自 1.3 起，后缀`.h2p`已被改为`.h5p`，但是`.h2p`文件仍然能被正常识别
2. XWebServer+ 目前并不能自动去除`<?py``>`代码的基础缩进