# 使用 Caddy 三分钟搭建你的 Web 服务器

<p align="center">本文作者：HelloGitHub-<strong>Anthony</strong></p>

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，本期介绍基于 Go 的网络服务端应用——**Caddy**，一个可以让您快速部署 http(s) 站点或反向代理服务的开源项目

> 项目地址：https://github.com/caddyserver/caddy

## 一、为什么使用 Caddy ?

> Caddy 是一个强大的、可扩展的平台，可以为您的站点、服务和应用程序提供服

使用 Caddy 我们可以在 Linux、Mac、Windows 上快速部署 http(s) 站点或反向代理服务。与传统的  Nginx 或者 Apache 相比，Caddy 整体只有一个可执行文件安装便捷**不易出现奇怪的依赖问题**，**配置文件结构清晰语法简单易于上手**，依托于模块化架构**可以使用 Go 语言快速开发 Caddy 模块**。

## 二、安装

实验环境：Ubuntu 20.04 LTS

Caddy 不仅可以作为一个系统服务安装也可以只下载一个可执行文件作为开发测试时使用，在这里我们使用单独下载的方式进行配置

> 下载地址：https://caddyserver.com/download
>
> 在网页上方选择自己的 Platform 后点击右侧蓝色的 Download 按钮即可
>
> 如果您想将 Caddy 安装成一个系统服务请按照官方指南操作： https://caddyserver.com/docs/install

下载好后的 Caddy 不能够直接运行，我们需要为其添加权限

```shell
$ mv caddy_linux_amd64 caddy # 将下载后的文件重命名方便后面指令输入，根据系统不同文件名不一样
$ sudo chmod a+x caddy # 为 Caddy 添加可执行权限
$ mv caddy /bin/caddy # 将 Caddy 复制到 bin 目录这样可以在命令行随时使用
```

命令行运行 ``caddy version`` 出现版本信息即为安装成功

## 三、快速开始

### 1、Hello World

Caddy 的配置文件语法简洁明了，首先在当前目录（当前终端所在目录）下新建一个名为 ``Caddyfile``  的文件（没有拓展名）输入以下内容

```ini
:2015

respond "Hello, world!"
```

然后输入

```shell
$ caddy adapt # 让 caddy 读取配置文件
# 也可以使用 caddy adapt --config /path/to/cadyfile 手动选择配置文件路径
$ caddy run # 运行 caddy 服务
```

之后访问 ``localhost:2015`` 可以看到网页显示 ``Hello World!`` 

访问 ``localhost:2019/config`` 可以查看 Caddy 的配置信息（Json）格式

### 2、Caddyfile 结构

Caddy 的原生配置文件使用的是 Json 格式 ，但是为了用户编写方便， Caddy 提供了 Caddyfile 作为接口让用户可以快速配置站点信息，运行时 Caddy 会自动将 Caddyfile 的配置信息转为 Json 配置文件。

> Caddyfile 所能提供功能不如 Json 配置文件强大，但是对于不需要复杂配置的人群而言两者几乎没有区别，具体对比请看
>
> https://caddyserver.com/docs/getting-started#json-vs-caddyfile

一个 Caddyfile 的文件结构如图所示：

![Caddy文件结构](./images/1.png)

> 图片来自于：https://caddyserver.com/docs/caddyfile/concepts#structure

其中，全局配置块可以省略，这时文件的第一行必须有是要配置的站点地址，每个站点的配置信息必须写在每个站点的花括号之中，**如果只有一个站点**（比如  Hello World 所示）则花括号也可以省略

### 3、几个例子

Caddyfile 的指令格式如下：

```ini
directive [<matcher>] <args...> { # matcher 代表匹配器，如果提供则该指令将只对 matcher 描述的资源进行响应
	subdirective [<args...>]	# 子指令
}
```

> Caddyfile 支持的指令可以在此处查询：https://caddyserver.com/docs/caddyfile/directives
>
> 有关如何使用 macher 过滤请求的文档：https://caddyserver.com/docs/caddyfile/matchers

下面给出一个简单的站点例子：

首先根据给出目录新建文件：

```text
.
├── Caddyfile
├── index.html
└── public
    └── HG.html
```

其中，``index.html`` 和 ``HG.html`` 内容如下：

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello World!</title>
</head>
<body>
    你好，世界！
</body>
</html>
```

```html
<!-- HG.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HelloGitHub</title>
</head>
<body>
    HelloGitHub
</body>
</html>
```

``Caddyfile`` 内容如下：

```ini
{
	# 服务器全局配置，可以省略
	# 完整可配置信息请见 https://caddyserver.com/docs/caddyfile/options
	auto_https off # 关闭 http 到 https 的自动重定向
	email Anthony@HelloGitHub.com # 用于自动续订 CA 证书使用
}

# 如果本机没有 wordpress 则注释这一块儿的站点配置
#:80 { # 部署一个 wordpress 站点
#	root * /var/www/wordpress
#	php_fastcgi unix//run/php/php-version-fpm.sock # 配置一个 fastcig 服务
#	file_server	# 配置一个文件服务
#}

http://localhost:3000 {
	basicauth /public/* {
		# 匹配访问 localhost:3000/public/* 的请求，为其加上登陆保护
		HG JDJhJDE0JGEySk9janFMdHlBY2Y0aVdQZklQak9HcmwzNDZhNFg0N3V5Ny9EZkZMZHB1Nkt4ZE5BNGJt
		# 用户名 HG 密码 HelloGitHub，密码使用 caddy hash-passowrd 指令生成
	}

	root * ./ # 设置当前站点根目录为当前文件夹，* 表示匹配所有的 request
	templates
	file_server {
		# 配置当前站点为静态文件服务器，可用于博客系统的搭建
		hide .git # 隐藏所有的 .git 文件
	}
}

:4000 {
	reverse_proxy /public/* http://localhost:3000 # 配置反向代理
	# 只会匹配 locahost:4000/public 的请求，转发到 localhost:3000/public/
}

```

在当前文件夹打开命令行输入：

```shell
$ caddy adapt # 让 caddy 读取 Caddyfile 进行自动配置
$ caddy run # 启动 Caddy
```

之后我们分别访问

``http://localhost:3000``

即可看到我们配置的服务器效果

![localhost:3000](./images/2.png)

``http://localhost:3000/public/HG.html``

![image-20220124153434506](./images/3.png)

输入用户名 HG 密码 HelloGitHub 后即可访问页面

![image-20220124153636161](./images/4.png)

``http://localhost:4000/public/HG.html``

可以发现我们的访问的实际上还是 ``http://localhost:3000/public/HG.html``

![image-20220124153958149](./images/5.png)



### 4、使用 REST API 配置站点

默认情况下，Caddy 会使用 ``localhost:2019``  作为 REST API 默认地址（该功能可以通过配置被禁止），直接访问 ``localhost:2019/config`` 可以查看我们当前站点的配置信息：

![image-20220124154705368](./images/6.png)

可以看到 Caddy 将我们的之前所写的 Caddyfile 文件转为了 Json 格式。

现在，我们删除目录下的 Caddyfile 文件，再次运行 ``caddy run`` 后刷新页面可以看到由于我们没有进行任何配置，当前网页返回 ``null`` .

Caddy 的 REST API 提供了以下几种配置指令：

- **[POST /load](https://caddyserver.com/docs/api#post-load)** 设置或替换活动配置
- **[POST /stop](https://caddyserver.com/docs/api#post-stop)** 停止活动配置并退出进程
- **[GET /config/\[path\]](https://caddyserver.com/docs/api#get-configpath)** 导出指定路径的配置
- **[POST /config/\[path\]](https://caddyserver.com/docs/api#post-configpath)** 设置或替换对象；追加到数组
- **[PUT /config/\[path\]](https://caddyserver.com/docs/api#put-configpath)** 创建新对象；插入数组
- **[PATCH /config/\[path\]](https://caddyserver.com/docs/api#patch-configpath)** 替换现有对象或数组元素
- **[DELETE /config/\[path\]](https://caddyserver.com/docs/api#delete-configpath)** 删除指定路径的值
- **[在 JSON 中使用`@id`](https://caddyserver.com/docs/api#using-id-in-json)** 轻松遍历配置结构
- **[GET /reverse_proxy/upstreams](https://caddyserver.com/docs/api#get-reverse-proxyupstreams)** 返回配置的代理上游的当前状态

例如，我们新建一个名为 ``HelloGitHub.json`` 的文件，并在里面保存如下内容：

```json
{ "apps": {
		"http": {
			"servers": {
				"example": {
					"listen": [":3000"],
					"routes": [
						{
							"handle": [{
								"handler": "static_response",
								"body": "HelloGitHub!"
							}]}]}}}}}
```

然后新打开一个命令行执行

```shell
$ curl localhost:2019/load \
	-X POST \
	-H "Content-Type: application/json" \
	-d @HelloGitHub.json
```

之后再次访问 ``localhost:3000`` 

可以看到我们我们刚刚配置的 app：

![image-20220124160859515](./images/7.png)

访问 ``localhost:2019/config`` 可以看到我们刚刚上传的配置：

![image-20220124161011985](./images/8.png)

其他的指令同理，在命令行中运行

```shell
$ curl localhost:2019/stop -X POST
```

即可停止当前的 app ，可以在运行 Caddy 的命令行看到如下信息：

```shell
2022/01/24 08:11:09.201	INFO	admin.api	received request	{"method": "POST", "host": "localhost:2019", "uri": "/stop", "remote_addr": "127.0.0.1:57956", "headers": {"Accept":["*/*"],"User-Agent":["curl/7.68.0"]}}
2022/01/24 08:11:09.201	WARN	admin.api	exiting; byeee!! 👋
2022/01/24 08:11:09.203	INFO	tls.cache.maintenance	stopped background certificate maintenance	{"cache": "0xc0000c8a80"}
2022/01/24 08:11:09.204	INFO	admin	stopped previous server	{"address": "tcp/localhost:2019"}
2022/01/24 08:11:09.204	INFO	admin.api	shutdown complete	{"exit_code": 0}
```

相比于 Caddyfile ，使用 REST API  配合 Json 配置文件 可以实现更多复杂的功能，但是实现起来也相对更为复杂。

## 四、总结

本文介绍的 Caddy 使用方法对于初学者学习或者简单的搭建类似 Hugo 的静态博客网站来说已经绰绰有裕，但是 Caddy 能实现的功能远不只如此，通过 Json 文件的形式进行配置或者导入 Go 语言编写的 Caddy 插件 Caddy 能够实现更多复杂的服务端功能。如果您想深入了解可以阅读 Caddy 的官方文档。
