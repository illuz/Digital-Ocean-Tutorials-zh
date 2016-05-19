# 如何在 VPS 上写简单的 Shell 脚本(1)

链接：https://www.digitalocean.com/community/tutorials/how-to-write-a-simple-shell-script-on-a-vps

---

### 介绍

本系列教程的目的是教你如何编写最各种用途的 Shell 脚本，用 Shell 脚本运行多个命令，或是带着复杂参数的单条命令，或是交互友好的工作脚本。它能让本来要手动去做的事情自动化，提高你的生活质量。

### 配置一个文件夹

在你开始写 Shell 脚本前，最好先创建一个文件夹来放这些脚本，建议在把个人的脚本都放在`~/bin`文件夹里。先建文件夹：

```sh
mkdir ~/bin
```

接下来，为了让这些脚本在系统各个地方都用直接使用，编辑`/etc/profile`：

```sh
sudo nano /etc/profile
```

然后在文件后面加上：

```sh
PATH=$PATH:$HOME/bin
export PATH
```

记得 ctrl+o 保存文件 ctrl+x 关闭退出。你可以让这些改动马上生效：

```sh
source /etc/profile
```

如果你的 Linux 发行版不支持 `source` 命令，你可以让你的 VPS 重启来让改动生效：

```sh
sudo reboot
```

### 创建文件

先从创建一个可执行文件开始吧：

```sh
touch ~/bin/firstscript
chmod +x ~/bin/firstscript
```

然后用 nano 文本编辑器打开脚本：

```sh
nano ~/bin/firstscript
```

为了让脚本在加载时，系统能知道是用什么程序执行这个脚本的，你要在第一行加上这样一句：

```sh
#!/bin/sh
```

然后你就可以加上任何你想要的 Linux 语句，例如：

```sh
clear
echo "Hello World!"
```

保存并退出文本编辑器后（nano 用的 ctrl+o,ctrl+x），你就可以运行你的脚本了：

```sh
firstscript
```

现在从系统的任何位置都能运行这个脚本：

![](https://assets.digitalocean.com/tutorial_images/PPFoJ5f.png)


### 样例脚本

Shell 脚本的一个主要目的就是方便执行重复性任务。比如，如果你要把很多文件移动到 ~/backup 文件夹里，你可以写个脚本来处理你指定的任意文件，你只要敲入这样的命令：

```sh
filebackup file-name1 file-name2...
```

这样就帮你移动好了。

在开始写脚本前，你需要先了解一些东西。没有硬编码（hardcoded）的脚本才是好脚本，也就是说，在这个例子中，如果你想改变你的备份文件夹的位置，你仅需轻松地改变脚本前面的一行代码就行了。是的，这里对应的那个变量只会被用到一次，但如果现在慢慢养成习惯，以后你会受益匪浅的。你不需要跳进文本编辑器就可以测试一下，通过键入做直接在命令行： 

```sh
testvariable=teststring
```

用 `echo` 命令打印出变量：

```sh
echo $testvariable
```

你可以看到你刚才设置的那个值“teststring”。

现在你可以开始编程了，先创建可执行文件：

```sh
touch ~/bin/filebackup
chmod +x ~/bin/filebackup
nano ~/bin/filebackup
```

记住，用 `#` 开头的内容是被注释的，它们不会对你的程序产生影响，有个例外就是第一行的注释是用来标明。


(未完)







