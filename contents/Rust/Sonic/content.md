# 开源轻便且无架构的搜索后端，跑起来就能搜！

![](images/1.jpg)

<p align="center">本文作者：HelloGitHub-<strong>kalifun</strong></p>
这是 HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，今天给大家推荐一个Rust 开源的搜索服务项目——Sonic

*When one builds a product, a good measure of success would not be how much time users spend on the product, but how much time users save by using it. Let search be at the core of any product for that purpose.*



## 一、Sonic简介

> Sonic是一种快速，轻量级且无模式的搜索后端。它提取搜索文本和标识符元组，然后可以在几微秒的时间内对其进行查询。

![](images/2.gif)



在某些用例中， Sonic 可以用作超繁重和功能齐全的搜索后端（例如 Elasticsearch ）的简单替代方案。下面我们介绍我们是如何放弃功能强大的搜索后端而选择 sonic 的。

## 二、特点

- `部署简单`：支持 Docker ，可以抛弃那些复杂的部署流程。
- `轻量`：1,000,000条动态长度的消息，占用磁盘为20MB（KV）+ 1.4MB（FST）。
- `入手简单`：支持多语言连接库。简单的协议( TCP )让它拥有主流语言的 Client ，这样使用操作门槛就降低了。

## 三、5分钟上手Sonic

>配置Sonic实例不需要花费很多时间。我鼓励您遵循此快速入门指南，以了解Sonic如何为您工作。您只需要Docker，NodeJS和一点点JavaScript知识（无需成为开发人员！）。

### 3.1 前提

- Docker（建议最新版本）
- Go（建议最新版本）

假设您正在运行MacOS。此测试的所有路径均为MacOS路径。如果您正在运行Linux，则可以将/ home /用作测试路径。对于永久部署，您将使用正确的UNIX / etc /配置和/ var / lib /数据路径。

如果您不愿意使用Docker运行Sonic，则可以尝试从Rust的Cargo上安装它，也可以自己编译。本指南没有详细说明如何执行此操作，因此，如果您打算以自己的方式进行操作，请参阅自述文件。

### 3.2 下载程序

```
docker pull valeriansaliou/sonic:v1.2.3
```

通过 Docker 运行 Sonic 很方便。您可以在 Docker Hub 上以 valeriansaliou / sonic 的形式找到预构建的 Sonic 映像。

### 3.3 配置文件

```
wget https://raw.githubusercontent.com/valeriansaliou/sonic/master/config.cfg
```

使用样本 [config.cfg](https://github.com/valeriansaliou/sonic/blob/master/config.cfg) 配置文件，并将其调整到您自己的环境。如果您希望微调配置，则可以阅读[详细配置文档](https://github.com/valeriansaliou/sonic/blob/master/CONFIGURATION.md)。

由于是快速入手，所以我在这篇文章中不会对配置文件进行详细的解释。

```
# Sonic
# Fast, lightweight and schema-less search backend
# Configuration file
# Example: https://github.com/valeriansaliou/sonic/blob/master/config.cfg
[server]
log_level = "debug"  # type: string, allowed: debug, info, warn, error, default: error

[channel]
inet = "[::1]:1491"  # 监听端口
tcp_timeout = 300  # 客户端连接超时时间
auth_password = "SecretPassword"    # 连接到通道所需的身份验证密码(可选)

[channel.search]
query_limit_default = 10     # 搜索结果限制
query_limit_maximum = 100	 # 最大搜索结果限制
query_alternates_try = 4	 # 替代词的数量
suggest_limit_default = 5    # 建议字数限制
suggest_limit_maximum = 20   # 最大建议字数限制


[store]

[store.kv]
path = "./data/store/kv/"     # 键值数据库存储的路径(建议绝对路径)
retain_word_objects = 1000    # 索引中给定单词可链接的最大对象数

[store.kv.pool]
inactive_after = 1800  # 将缓存的数据库视为非活动状态并且可以关闭（如果未使用，即重新激活）

[store.kv.database]
flush_after = 900		# 将等待的数据库更新从内存刷新到磁盘的时间
compress = true			# 是否压缩数据库
parallelism = 2			# 限制可以同时运行的压缩线程和刷新线程的数量
max_files = 100			# 每个数据库在同一时间保持打开状态的最大数据库文件数
max_compactions = 1		# 限制并发数据库压缩作业的数量
max_flushes = 1			# 限制并发数据库刷新作业的数量
write_buffer = 16384	# 数据库写缓冲区的最大大小
write_ahead_log = true	# 是否启用预写日志

[store.fst]
path = "./data/store/fst/"		# 有限状态传感器数据库存储的路径(建议绝对路径)

[store.fst.pool]
inactive_after = 300 	# 将缓存的图形视为非活动状态并且可以关闭

[store.fst.graph]		
consolidate_after = 180		# 合并具有待处理更新的图形之后的时间
max_size = 2048				# 磁盘上图形文件的最大大小
max_words = 250000			# 图形中可以同时保留的最大单词数，之后将不再插入其他单词
```

将其保存为.cfg文件，尽可能不要放入中文命名的文件夹内。

### 3.4 启动Sonci

```
docker run -p 1491:1491 -v /path/to/your/sonic/config.cfg:/etc/sonic.cfg -v /path/to/your/sonic/store/:/var/lib/sonic/store/ valeriansaliou/sonic:v1.2.3
```

- 此`/path/to/your/sonic/config.cfg`文件路径不能错。
- `/path/to/your/sonic/store/`这是本地存储数据库路径。

这样我们就完成了 Sonic 的服务端啦，想要将内容写入数据库，还需要借助 Sonic-Client。下面我将使用 [go-sonic](https://github.com/expectedsh/go-sonic)进行演示。

## 四、Sonic 插入数据

### 4.1 安装

```
go get github.com/expectedsh/go-sonic
```

### 4.2 示例

```
package main

import (
	"fmt"
	"github.com/expectedsh/go-sonic/sonic"
)

func main() {

	ingester, err := sonic.NewIngester("localhost", 1491, "SecretPassword")
	if err != nil {
		panic(err)
	}

	// I will ignore all errors for demonstration purposes
	// 将下面数据写入数据库中
	_ = ingester.BulkPush("movies", "general", 3, []sonic.IngestBulkRecord{
		{"id:6ab56b4kk3", "Star wars"},
		{"id:5hg67f8dg5", "Spider man"},
		{"id:1m2n3b4vf6", "Batman"},
		{"id:68d96h5h9d0", "This is another movie"},
	})

	search, err := sonic.NewSearch("localhost", 1491, "SecretPassword")
	if err != nil {
		panic(err)
	}
	// 查看关键字man
	results, _ := search.Query("movies", "general", "man", 10, 0)

	fmt.Println(results)
}
```

### 4.3 结果

```
["id:5hg67f8dg5","id:1m2n3b4vf6"]
```

这样我们就完成了简单的搜索系统啦，我们可以利用的返回结果快速定位到数据库具体位置。

## 五、总结

在将其作为开源软件发布给广大公众时，我们希望为社区提供“构建自己的SaaS业务”生态系统中缺失的部分：Redis 搜索。它解决了一个古老的瘙痒；我等不及要看看人们将如何使用Sonic来构建！      --Valerian Saliou

这是 Sonic 作者的说的话，我在想开源的意义大概也是如此吧。技术共享！

## 六、参考文献

[Sonic项目地址](https://github.com/valeriansaliou/sonic)

[Sonic作者博客](https://journal.valeriansaliou.name/announcing-sonic-a-super-light-alternative-to-elasticsearch/)