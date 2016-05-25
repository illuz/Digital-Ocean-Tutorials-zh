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

"Else"，顾名思义，是 if 命令的另外一个选择分支。基本用法是这样的：

```sh
if [ 20 -lt 10 ]
then
  echo "What?"
else
  echo "No, 20 is greater than 10."
fi
```

除了上面说的数学表达试，你还可以在 if/else 里比较字符串，虽然符号有点不一样，不过都是用 test 命令或 `[]` 命令。比较字符串的符号有如下几种：

```
string = string     相等
string != string    不相等
string              string 是否非空
-n string           string 是否非空且存在
-z string           string 是否是空的且存在
```

还能在条件里对文件进行判断：

```
-s file     file 是否非空
-f file     file 是否存在且不是文件夹
-d folder   folder 是否是文件夹
-w file     file 是否可写
-r file     file 是否可读
-x file     file 是否可执行
```

### 嵌套 if

你可以在 if 里再嵌套 if，下面的例子中我们会用到[上一篇]讲的 read 命令，并用 if 处理用户的输入：

```sh
#!/bin/bash
echo "Input which file you want created"
read file
if [ -f $file ]
then
echo "The file already exists"
else
  touch $file
  if [ -w $file ]
  then
    echo "The file was created and is writable"
  else
    echo "The file was created but isn't writable"
  fi
fi
```

### 样例脚本

这里我们要继续对备份脚本进行修改，这个版本我们会先检查下备份文件夹是否存在，不存在再去检查是否有权限创建它。首先，我们还是先创建一个可执行文件：

```sh
touch ~/bin/filebackup3
chmod +x ~/bin/filebackup3
nano ~/bin/filebackup3
```

然后就是脚本：

```sh
#!/bin/bash
#Backup script 3.0
#Description: makes a copy of any given file at the backup folder
#Author: Your Name
#Date: 9/29/2013
#询问用户要存的目录:
echo -e "\e[47m\e[1m\e[32mFile Backup Utility\n\e[39m\e[0m\e[47mPlease input your backup folder:"
read BACKUPFOLDER
#脚本必须保证目录存在
if [ -d $BACKUPFOLDER ]
then
  echo "You backup folder exists and will be used."
else
  mkdir $BACKUPFOLDER
  if [ -d $BACKUPFOLDER ]
  then
    echo "Backup folder created successfully."
  else
    echo -e "I do not have the rights to create your backup folder.\nThis script will now exit."
    exit 1
#exit 1 命令让脚本退出并返回一个错误码
  fi
fi
#所给文件将被复制到备份目录
echo -e "\e[30mWhich files do you want backed up?\e[39m\e[49m"
read FILES
if [ -n $FILES ]
then
  cp -a $FILES $BACKUPFOLDER
else
  echo "File does not exist."
fi
```

这个脚本会告诉你输入的文件夹是否存在，是否创建了新文件夹。

### 总结

你学到越多，越能写出更实用新颖的脚本程序，在这部分教程中，我们就让用户友好的脚本变得更加友好了。

(已完)
