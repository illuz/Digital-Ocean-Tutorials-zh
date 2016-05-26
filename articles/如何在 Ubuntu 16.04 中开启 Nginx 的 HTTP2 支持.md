# 如何在 Ubuntu 16.04 中开启 Nginx 的 HTTP2 支持

原文:[How To Set Up Nginx with HTTP/2 Support on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-16-04)

---

### 简介

Nginx 是一个高效可靠的开源 web 服务器，它因为低内存占用，高可扩展性，易于配置，以及支持绝大多数的协议而十分流行。

HTTP/2 也是它支持的一个协议，HTTP/2 发布于 2015，它主要的优势在于它对内容丰富的网站的高传输速度。

这个教程会教你在开启 HTTP2 支持，让 Nginx 更快更安全。

### 环境及条件

在开始前，我们要准备这些东西：

- Ubuntu 16.04
- 有 sudo 权限的普通用户（具体做法阅读[Ubuntu 16.04 服务器初始配置](./Ubuntu 16.04 服务器初始配置.md)）
- 注册好的域名。你可以从 [Namechieap](https://namecheap.com/) 上买一个，或者从 [Freenom](http://www.freenom.com/) 免费获取。
- 保证你的域名已经配置好指向你的服务器。如果有问题可以看看[这个教程](https://www.digitalocean.com/community/tutorials/how-to-set-up-a-host-name-with-digitalocean)（有关 DigitalOcean 上如何配域名）
- 一个 SSL 证书。你可以选择[生成自签名的证书](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04)，或者[获取一个免费的 Let's Encrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04)，或者[从其他供应商买一个](https://www.digitalocean.com/community/tutorials/how-to-install-an-ssl-certificate-from-a-commercial-certificate-authority)。

如果你已经准备好了上面列的这条件，那就开始正文吧。

### HTTP 1.1 和 HTTP/2 的区别

HTTP/2 是新版本的超文本协议（HTTP），HTTP 协议是用来让服务器把页面传输给浏览器的。HTTP/2 是近二十年来 HTTP 协议第一次大更新：HTTP 1.1 是在 1999 年公开的，时的网页通常是只是一个单一的 HTML 文件内嵌 CSS 样式。互联网自那时以来发生了巨大变化，现在我们正面临着 HTTP 1.1 的局限性 - 它限制了现代网站的潜在传输速度，因为它下载页面内容时是队列式的（后面的下载任务必须等前面的任务完成后才能开始），而现代网页每个页面平均需要大约 100 个下载请求（一个图象，JS文件，CSS文件等就是一个请求）。 

HTTP/2 能够解决这个问题，它带来了根本性的变化：

- 所有的请求都是平行的，并不是队列式的
- HTTP 头是压缩过的
- 页面是按二进制传输的而不是按文本，高效了不少
- 服务器可以推送（push）数据，甚至不需要用户请求，从而提高延迟高的用户的速度

虽然 HTTP/2 不强制要求加密，Google Chrome 和 Mozilla Firefox 这个最大的浏览器的开发者却指出，为了安全起见，他们将只支持开启了 HTTPS 连接的 HTTP/2 页面。因此，如果你决定要用 HTTP/2，还必须使用 HTTPS 来加密传输。



