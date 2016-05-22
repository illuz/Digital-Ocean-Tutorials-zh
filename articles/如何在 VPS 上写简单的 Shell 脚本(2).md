# 如何在 VPS 上写简单的 Shell 脚本(2)

原文:[How To Write a Simple Shell Script on a VPS (Part 2)](https://www.digitalocean.com/community/tutorials/how-to-write-a-simple-shell-script-on-a-vps-part-2)


本文是[Shell Script 介绍](../series/Shell Script 介绍.md)系列的一部分。

---

### 简介

这个教程的第二部分会教你 VPS 上用的更多命令，用来显示及收集信息。这往篇文件假设你已经配置好了[第一部分](https://www.digitalocean.com/community/tutorials/how-to-write-a-simple-shell-script-on-a-vps)中的 Shell 脚本文件夹。

### echo 命令

这个命令让你可以把信息显示给用户，你可以显示简单的文本字符串及变量，它有两个参数：`-n`表示输出文字后不换行，`-e`表示若字符串中出现以下字符，则特别加以处理，而不会将它当成一般文字输出：

```
\a 发出警告声
\b 删除前一个字符
\c 最后不加上换行符号
\e Esc 字符
\n 换行
\r 光标移至行首，但不换行
\t 插入 tab
\0xx 插入 0xx （八进制）所代表的 ASCII 字符
\\ 插入 \ 字符
```

比如现在的两条命令的输出一样的：

```sh
echo -e "Text\c"
echo -n "Text"
```

要输出变量只要在字符串中写'$'再加上变量名就行了，就像：

```sh
string=World!
echo "Hello $string"
```

你可以在一个字符串里放进文本、命令和变量，你甚至可以用一行代码输出多行，使用 `\n` 你就可以输出一个回车了。


（未完）
