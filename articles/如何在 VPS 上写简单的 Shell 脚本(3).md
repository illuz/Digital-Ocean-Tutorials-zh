# 如何在 VPS 上写简单的 Shell 脚本(3)

原文:[How To Write a Simple Shell Script on a VPS (Part 3)](https://www.digitalocean.com/community/tutorials/how-to-write-a-simple-shell-script-on-a-vps-part-3)


本文是[Shell Script 介绍](../series/Shell Script 介绍.md)系列的一部分。

---

### 简介

条件控制语句都是任何脚本语言或者编程语言不可或缺的一部分。这系列的第三部分中你会学到 bash 里的 if 和 else，以及如何把它们用到你的脚本中。这篇文章也假设你已经配置好了[第一部分](https://www.digitalocean.com/community/tutorials/how-to-write-a-simple-shell-script-on-a-vps)中的 Shell 脚本文件夹。

### if

条件控制语句就是用一个条件的真(true)或假(flase)来决定是否要执行一个指定的动作，在 Shell 脚本里用的是 if 命令，if 后面跟的是一个用来检查真假的表达式。这个表达式也可以是执行一句命令后的退出状态码(exit code)，一个数学式，或是其它可变的事情。当用退出状态码来判断时，脚本是很简单的：

```sh
if ls folder
then
echo "Folder exists"
fi
```

如果 folder 文件夹存在，就会执行 echo 命令，因为 ls 如果成功执行会返回退出状态码 0；如果文件夹不存在，文本就不会被打印出来。所有的 'if' 命令都要跟着一个 'then'，并以 'fi' 结尾。如果你不是用退出状态码而是用数学公式，那你需要 'test' 命令。下面是 Shell 脚本用来比较数字的操作符：

```
-eq 相等
-ne 不相等
-lt 小于
-le 小于或等于
-gt 大于
-ge 大于或等于
```

test 命令可以有两种写法：

```
if test 4 -gt 3
# 或是
if [ 4 -gt 3]
```

这两种学法效果是一样的，都是需要 'then' 和 'fi' 的。例如：

```sh
if [ 20 -lt 10 ]
then
echo "What?"
fi
```

"What?" 永远不会被打印出来，因为 20 是大于 10 的。好了，现在你要怎么在 if 条件返回 false 时向用户显示一条消息呢？

### else




（未完）
