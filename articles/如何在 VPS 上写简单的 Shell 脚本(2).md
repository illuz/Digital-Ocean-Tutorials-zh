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

### 用 echo 打印格式化过的字符

echo 可以打印出包含多种颜色和样式的文本。不过下面说的东西可能不能适用所有终端，所以其它人看到和你终端上不同的结果时请不要感到奇怪和担心，只是看起来不同并不是个问题。

每个要定制字符（用来让字符变粗、变色等）都会先用一个 escape 字符（`\e`）先标志，比如：

```sh
echo -e "This is \e[1mBold"
```

下面是比较常用的样式和对应的编码：

```
加粗:         \e[1m
暗色:         \e[2m
下划线:        \e[4m
反色:         \e[7m
```

你可以混着使用它们，比如可以创建一个下划线加粗的文本，然后你可以用 "\e[0m" 把样式重置：

```sh
echo -e "\e[4mThis \e[1mis\e[0m \e[7man example \e[0mstring"
```

到你的终端试试它的输出吧。

加颜色也一样，每个颜色都有一个编码，用法和前面的样式一样。下面是一些大部分终端都有效的颜色和编码：

```
黑:          \e[30m (文本) and \e[40m (背景)
红:          \e[31m (文本) and \e[41m (背景)
绿:          \e[32m (文本) and \e[42m (背景)
黄:          \e[33m (文本) and \e[43m (背景)
蓝:          \e[34m (文本) and \e[44m (背景)
紫红:         \e[35m (文本) and \e[45m (背景)
蓝绿:         \e[36m (文本) and \e[46m (背景)
浅灰:         \e[37m (文本) and \e[47m (背景)
默认:         \e[39m (文本) and \e[49m (背景)
```

同样你可以混用颜色让文本和背景颜色不同，也可以把之前说的正常的样式也加进来。

### read 命令

用 read 命令可以从使用者获取信息，它会把用户按下回车前输入的所有字符都存到变量里，里面唯一的参数就是那个变量。比如，下面是一个创建用户想要名字文件夹的脚本：

```sh
#!/bin/bash
read foldername
mkdir foldername
```

不过这个脚本并没有任何用户界面，那么如何让用户知道我们希望他输入什么呢？

### 样例脚本

在这个例子中我们将用上前面学的格式化文字及输入输出。前一篇文章已经写了个基于参数传递的备份文件脚本，现在我们要重写一下让它能够询问用户要保存到哪个目录里。

首先我们创建个可执行文件：

```sh
touch ~/bin/filebackup2
chmod +x ~/bin/filebackup2
nano ~/bin/filebackup2
```

重写并让它有用户界面：

```sh
#!/bin/bash
#Backup script 2.0
#Description: makes a copy of any given file at the backup folder
#Author: Your Name
#Date: 9/19/2013
#询问用户要存的目录:
echo -e "\e[1m\e[32mFile Backup Utility\n\e[39m\e[0mPlease input your backup folder:"
read BACKUPFOLDER
#脚本必须保证目录存在
mkdir -p $BACKUPFOLDER
#所给文件将被复制到备份目录
echo -e "\e[47m\e[30mWhich files do you want backed up?\e[39m\e[49m"
read FILES
cp -a $FILES $BACKUPFOLDER
```

### 总结

这篇文章让你能写出一个适当的用户界面，让别人都能知道这个脚本是干啥的，要输入什么数据。不过并不是所有脚本都要用户界面的，不过在命令行中你最好为你的脚本写一个"help"界面，这里你就要用上"echo"命令了。

（已完）
