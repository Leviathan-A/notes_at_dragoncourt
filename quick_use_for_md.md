<!-- 表格居中 -->
<style>
table
{
    margin: auto;
}
</style>

# 1. 总览
Markdown 速查表提供了所有 Markdown 语法元素的基本解释。如果你想了解某些语法元素的更多信息，请参阅更详细的 基本语法 和 扩展语法.
>参考网站:\
1.[markdown语法]

[markdown语法]:https://markdown.com.cn/cheat-sheet.html

## 1.1. 基本语法
|   操作   |               字符                |    快捷键    |             演示              |
| :------: | :-------------------------------: | :----------: | :---------------------------: |
|   加粗   |             \*\*B\*\*             |    ctrl+b    |           **Bold**            |
|   斜体   |               \*I\*               |    ctrl+i    |           *italic*            |
| 单行代码 |           \`underline\`           |    太麻烦    |          `underline`          |
|  代码块  |       \`\`\`underline\`\`\`       |    太麻烦    |        ```underline```        |
| 添加章节 |              太麻烦               | ctrl+shift+p |
|   目录   |              太麻烦               | ctrl+shift+p |
|   引用   |           \> blockquote           |    太麻烦    |         > blockquote          |
|  超链接  | \[百度\]\(https://www.baidu.com\) |    太麻烦    | [百度](https://www.baidu.com) |
|   图片   |     \!\[图片文字\](图片地址)      |    太麻烦    |                               |

---
代码块演示
```cpp
int main()
{
    return 0;
}
```
多彩显示\
<font face="黑体">我是黑体字</font>
<font face="微软雅黑">我是微软雅黑</font>
<font face="STCAIYUN">我是华文彩云</font>

<font color=red>我是红色</font>
<font color=#008000>我是绿色</font>
<font color=Blue>我是蓝色</font>

<font size=5>我是尺寸</font>

<font face="黑体" color=green size=5>我是黑体，绿色，尺寸为5</font>

#锚点制作

- [锚点1](#anchor-1)
- [锚点2](#anchor-2)
- [锚点3](#anchor-3)

这是一段正文。

<a name="anchor-1"></a>
## 标题一

这是标题一下的正文。

<a name="anchor-2"></a>
## 标题二

这是标题二下的正文。

<a name="anchor-3"></a>
## 标题三

这是标题三下的正文。
