# Apache vs Nginx: 使用须知

原文:[Apache vs Nginx: Practical Considerations](https://www.digitalocean.com/community/tutorials/apache-vs-nginx-practical-considerations)

---

### 简介

Apache 和 Nginx 是最流行的两款开源的 web 服务器，它们负责了网络上超过 50% 的网络流量，两都都能处理多种类型的负载模式，并与其它软件一同提供一套全栈的功能。

尽管 Apache 和 Nginx 有着许多共同的特质，但他们不应该被认为是可以完全相互代替的。它们都有自己的过人之处，重点是你要知道在不同的情况下如何重新评估所选择的 Web 服务器。本文将专门讨论它们在各个领域各自的长短。 

### 概述

在我们深入讨论 Apache 和 Nginx 的区别之前，先快速浏览下这两个项目的开发背景和扮演的角色。

#### Apache

Apache HTTP Server 是 Robert McCool 在 1995 年开发出来的，并且从 1999 年开始在 Apache 软件基金会（Apache Software Foundation）的指导下开发。因为这个项目是这个基金会原始项目，而且也是迄今为止里面最受欢迎的项目，所以它也被称为"Apache"。

从 1996 年来，Apache 成为了网上最受欢迎的网页服务器，也正因如此，Apache 获得了大量的文档以及其他软件项目的集成支持。

很多网站管理者会选择 Apache 是因为它的灵活、强大和广泛的支持。它可以通过一个可扩展的模块系统进行动态加载，并且无需单独安装其它软件就可以处理大量解释的语言。

#### Nginx

2002 年 Igor Sysoev 为了解决 C10K 问题而开始开发 Nginx，现代网络的发展要求服务器要能处理 10000 个并发连接，C10K 问题就是这样一个对 web 服务器的挑战。Nginx 最早的公开发行是在 2004 年，来依靠异步、事件驱动的架构实现 C10K 这一目标。

Nginx 自发布以来不断壮大，得益于其轻量级的资源利用和其对最低硬件要求的轻松扩展能力。 Nginx 擅长快速相应静态内容，并被设计用来把动态的请求转发到的其他软件上。

网站管理者选择 Nginx 因为它负载下优秀的资源利用效率和响应能力选择。Nginx 的支持者很喜欢它因为它专注于核心的 Web 服务器和代理服务器的功能。


### 连接处理架构

Apache 和 Nginx 之间最大的区别是它们处理连接和传输的方式。[Cannot translate: This provides perhaps the most significant difference in the way that they respond to different traffic conditions]

#### Apache

Apache 提供了多样化的多进程模块（称为 MPMs，multi-processing modules），这些模块描述了客户端的请求如何被处理。通常它允许管理员随意改变连接处理架构。有这几个模块：

- **mpm_prefork**：这个进程模块可以产生单线程的进程来分别处理请求，每个子进程一次只能处理一个连接。当请求的数量比进程数少时，这个 MPM 是非常快的，不过当请求数多起来后性能就会大打折扣，因此它在多很情景下不是个好选择。因为每个进程对内存消耗的影响很大，所以它也很难高效的进行扩展。不过当其它的组件没有考虑线程时，它可能是个很好的选择。例如，PHP 并不是线程安全的，这个 MPM 就可以配合 `mod_php` 来让 PHP 安全的工作。
- **mpm_worker**：这个模块产生的是多线程的进程，每个线程处理一个连接。线程比进程高效多了，这意味着这个 MPM 在扩展性方面比 `mpm_prefork` 好多了。因为线程比进程多多了，所以新的连接可以很快的获取到一个空闲的线程而不用等待进程。
- **mpm_event**：这个模块在很多方面都跟 `mpm_worker` 很像，不过它对处理长连接(keep-alive connections)进行了优化。当用这个

#### Nginx


### 静态内容 vs 动态内容

#### Apache

#### Nginx


### 分布式配置 vs 中心化配置

#### Apache

#### Nginx


### 基于文件的解释 vs 基于 URI 的解释

#### Apache

#### Nginx


### 模块

#### Apache

#### Nginx


### 支持，兼容性，生态系统和文档

#### Apache

#### Nginx


### Apache 和 Nginx 一起用


### 总结


(未完)
