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

### 第一步 - 安装最新版的 Nginx

在 Nginx 1.9.5 之后的版本中才支持 HTTP/2 协议，幸运的是 Ubuntu 16.04 自带的软件源里的 Nginx 版本已经比它高了，所以我们不用再去添加软件源。

首先我们更新下 apt 的软件包：

```sh
sudo apt-get update
```

然后安装 Nginx：

```sh
sudo apt-get install nginx
```

安装完后先检查一下 Nginx 的版本：

```sh
sudo nginx -v
```

输出应该是类似下面这样：

```
nginx version: nginx/1.10.0 (Ubuntu)
```

下面几步我们会修改 Nginx 的配置文件里的配置项，每一步配置后我们都会检查一下语法。最后我们会验证 Nginx 能否支持 HTTP/2，并做些性能优化。

### 第二步 - 修改监听端口并开启 HTTP/2

首先把监听端口从 80 改到 443。

打开配置文件：

```sh
sudo nano /etc/nginx/sites-available/default
```

默认情况下，Nginx 是监听 80 端口的，这是标准 HTTP 的端口：

```
listen 80 default_server;
listen [::]:80 default_server;
```

如你所见，这里有两个 `listen` 变量，第一个是 IPv4 连接用的，第二个是 IPv6 连接用的。我们两边都要加密。

把监听端口改成 `443`，这是 HTTPS 用的端口：

```
listen 443 ssl http2 default_server;
listen [::]:443 ssl http2 default_server;
```

注意我们加了 `ssl` 和 `http2`，这个变量会告诉 Nginx 为支持的浏览器提供 HTTP/2 服务。

### 第三步 - 改 server_name 配置

在 `listen` 后面的那行 `server_name`，表示这个配置文件所对应的服务器。`server_name` 默认是下划线 `_`，表示这个配置文件对所有请求都生效。把它改成你自己的域名，就像这样：

```
server_name example.com;
```

保存退出后，检查下有没有语法错误：

```sh
sudo nginx -t
```

如果方法没有错误，会看到类似这样的信息：

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 第四步 - 增加 SSL 证书

接下来，你要为你的 Nginx 配置 SSL 证书，如果你不知道 SSL 证书或者并没有 SSL 证书，请阅读「环境及条件」部分里面提到的教程。

在 Nginx 配置目录里创建一个文件夹用来保存你的 SSL 证书。

```sh
sudo mkdir /etc/nginx/ssl
```

把你的证书和私钥复制到这个目录里，然后把这些文件以域名命名。（这能让以后管理起来更方便，因为你以后可能会拥有多个域名。）把 `example.com` 改成你自己的域名：

```
sudo cp /path/to/your/certificate.crt /etc/nginx/ssl/example.com.crt
sudo cp /path/to/your/private.key /etc/nginx/ssl/example.com.key
```

现在再次打开你的配置文件：

```sh
sudo nano /etc/nginx/sites-available/default
```

在 `server` 块里加入几行，用来定义你的证书的位置：

```
ssl_certificate /etc/nginx/ssl/example.com.crt;
ssl_certificate_key /etc/nginx/ssl/example.com.key;
```

保存退出编辑器。

### 第五步 - 避免过时的不安全的加密套件组合

HTTP/2 有个[庞大的黑名单](https://http2.github.io/http2-spec/#BadCipherSuites)，里面列了很多过时的不安全的加密套件组合，我们应该尽量避免用到它们。加密套件组合(Cipher suits)是由几个加密算法组成的，用来描述传输的数据是怎么被加密的。

这里我们将使用一个比较流行的加密套件组合，它的安全性已经被类似 CloudFlare 这样的互联网大公司承认了。不要使用 MD5（因为它已经从 1995 年来就被认定为不安全了，不过即使这样还是有很多地方在使用它）。

打开下面这个配置文件：

```sh
sudo nano /etc/nginx/nginx.conf
```

在 `ssl_prefer_server_ciphers on;` 后面加上一行：

```
ssl_ciphers EECDH+CHACHA20:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
```

再次检查一下配置文件的语法：

```sh
sudo nginx -t
```

### 第六步 - 提高私钥交换的安全性

建立一个安全连接的第一步是服务端和客户端之前的私钥交换，如果这一步出现问题，这个连接将变得不安全，也就是说这里面的数据交换对会被第三方看到。因此我们使用 Diffie–Hellman–Merkle 算法，它的实现很复杂，不是三言两语能说清楚的，如果你有兴趣，可以看[这个 Youtube 视频](https://www.youtube.com/watch?v=M-0qt6tdHzk)。

Nginx 默认用一个 1028-bit DHE(Ephemeral Diffie-Hellman) 密钥，相对比较容易被解密。为了提供最高程度的安全性，我们要建立更安全的 DHE key。

首先，运行下面的命令：

```sh
sudo openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
```

**（记住我们要把 DH 参数生成到 SSL 证书同目录下，这里我们的证书在 `/etc/nginx/ssl/`，因此是 `-out /etc/nginx/ssl/dhparam.pem`。这是因为 Nginx 会先检查用户提供的证书的目录是否存在，在的话就用那个目录。）**

在命令最后的那个变量（这里是 2048）表示私钥的长度，2048 长度的私钥已经足够安全了，[Mozilla 基金会也建议用 2048](https://wiki.mozilla.org/Security/Server_Side_TLS#Pre-defined_DHE_groups)，不过如果你想要更加安全可以把它改到 `4096`。

生成过程大概会花 5 分钟。

生成完成后，打开 Nginx 的配置文件：

```sh
sudo nano /etc/nginx/sites-available/default
```

在 `server` 块增加一行，定义你的 DHE key 的目录：

```
ssl_dhparam  /etc/nginx/ssl/dhparam.pem;
```

### 第七步 - 把所有 HTTP 请求重定向到 HTTPS

由于我们感兴趣的是只通过 HTTPS 的服务，所以我们应该告诉 Nginx 如果服务器收到一个HTTP请求它应该怎么做。

在配置文件的最后面新增一个 `server` 块，将所有的 HTTP 请求重定向到 HTTPS（记得把 server name 改成你的域名）：

```
# /etc/nginx/sites-available/default
server {
       listen         80;
       listen    [::]:80;
       server_name    example.com;
       return         301 https://$server_name$request_uri;
}
```

再次检查一下配置文件的语法：

```sh
sudo nginx -t
```

### 第八步 - 更新加载 Nginx

这一步是为了让修改的 Nginx 配置生效。我们已经在每一步修改后都有进行语法错误检查，已经为重启 Nginx 并测试更改做好了准备。

总之，忽略注释和空行，你的配置文件现在应该跟这差不多：

```
# /etc/nginx/sites-available/default
server {
        listen 443 ssl http2 default_server;
        listen [::]:443 ssl http2 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name example.com;

        location / {
                try_files $uri $uri/ =404;
        }

        ssl_certificate /etc/nginx/ssl/example.com.crt;
        ssl_certificate_key /etc/nginx/ssl/example.com.key;
        ssl_dhparam /etc/nginx/ssl/dhparam.pem;
}


server {
       listen         80;
       listen    [::]:80;
       server_name    example.com;
       return         301 https://$server_name$request_uri;
}
```

重启 Nginx 让这些改动生效：

```sh
sudo systemctl restart nginx
```

### 第九步 - 验证

让我们检查下服务器是否正常运作。用浏览器打开你的网站：

```
example.com
```

如果一切都配置正确，你应该自动重定向到 HTTPS。现在检查一下 HTTP/2 是否正常工作：打开 Chrome 浏览器的开发者工具（View->Developer->Developer Tools）并刷新页面，选择里面的 Network tab，在 Name 那一列右击，选中 Protocol 选项。

现在你就能看到 `h2`（代表 HTTP/2）在新增的那一列里：

![](https://assets.digitalocean.com/articles/nginx_http2/http2_check.png)

这说明我们的服务器已经可以用 HTTP/2 协议提供服务了，不过为了在生产环境中使用还有一些东西要准备下。

### 第十步 - 优化 Nginx 性能

这一步我们会修改 Nginx 的配置文件，让 Nginx 提高性能与安全性。

首先打开 `nginx.conf` 文件：

```sh
sudo nano /etc/nginx/nginx.conf
```

#### 启用连接证书缓存

相比 HTTP，HTTPS 花费相对较长的时间来建立服务器和用户之间的初始连接。为了尽量减少这种差异对页面加载速度的影响，我们将启用连接证书缓存。这意味着，服务器将使用的证书的缓存版本而不是在每个页面上创建一个新的会话（session）。

在 `nginx.conf` 文件里的 `http` 块后面增加几行，来打开 session 缓存：

```
# /etc/nginx/nginx.conf
ssl_session_cache shared:SSL:5m;
ssl_session_timeout 1h;
```

`ssl_session_cache` 表示 session 会缓存的大小，1 MB 大概可以存 4000 个会话，默认的 5M 对大部分用户来说已经足够了，不过如果你有更大的流量，你可以自行修改这个修。

`ssl_session_timeout` 表示一个 session 在缓存中的时间，这个值不宜过大（超过一小时），不过如果太低了它的作用也就降低了。

#### 启用 HTTP 严格传输安全（HSTS, HTTP Strict Transport Security）

即使在 Nginx 配置文件里已经把所有常规的 HTTP 请求重定向到 HTTPS，我们也要启用 HSTS 来避免不安全的重定向。

如果浏览器发现一个 HSTS header，它在设定的时间内不会再尝试通过常规的 HTTP 重新连接到服务器，不管怎样，它都会用加过密的 HTTPS 连接的来交换数据。这个 header 也会保护我们免受协议降级的攻击。

在 `nginx.conf` 中增加一行：

```
# /etc/nginx/nginx.conf
add_header Strict-Transport-Security "max-age=15768000" always;
```

`max-age` 的单位是秒，15768000 秒就是 6 个月。

这个 header 默认不会加到子域名的请求中，所以如果你有子域也想用上 HSTS，你可以在最后一行增加 `includeSubDomains` 变量，就像这样：

```
# /etc/nginx/nginx.conf
add_header Strict-Transport-Security "max-age=15768000; includeSubDomains: always;";
```

最后还是检查下语法错误：

```sh
sudo nginx -t
```

最后重启 Nginx 让改动生效：

```sh
sudo systemctl restart nginx
```

### 总结

现在你的服务器已经是 HTTP/2 的了，如果你想测试 SSL 连接的强度，可以访问 [Qualys SSL Lab](https://www.ssllabs.com/ssltest/) 并测试下你的服务器。如果一切配置得当，你应该可以拿到 A+ 的安全评分。

(已完)

