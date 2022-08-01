# 变量对照表
> 为了避免编辑器报错，建议配合 `sdk` 使用
> 具体参考 [SDK使用](./index.md)

## 总览

| 变量名   | 类型    |全局  | 描述            |
|----------|--------|------|----------------|
|recv_data |dict    |否    |请求数据         |
|pageData  |dict    |是    |可用于存放页面变量|

## RECV_DATA    

此变量为格式化后的请求报文

这是一个正常的 recv_data 变量

```python
{                                                 
    'mode': 'GET',
    'path':  '<=×××××××××××××=>',
    'protocol': 'HTTP/1.1',
    'args': {'aaa': ['bbb']},
    'header': {
        'Accept-Encoding': 'identity',
        'Host': '<=×××××××××=>',
        'User-Agent': 'Python-urllib/3.10',
        'Connection': 'close'
    }
}
```

| 键       | 类型    | 描述            |
|----------|--------|-----------------|
|`mode`    |str     |请求模式          |
|`path`    |str     |本地文件路径      |
|`protocol`|str     |请求协议          |
|`args`    |dict    |请求参数          |
|`header`  |dict    |请求头            |

## PAGEDATA

储存自身的变量以便其他代码段使用