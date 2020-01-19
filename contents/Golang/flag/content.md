# Go命令行工具:flag

`flag`是Go的内置库，主要是实现了命令行参数的解析，使得开发命令行工具更加简单。

## 一、前言

当我们开发命令行工具时，我们为了扩展功能，会添加命令行参数。下面我介绍一个大家都很熟悉的程序`Nginx`,虽然它不是`go`写的，但我们可以使用`go`来实现`Nginx`的命令行参数。

```
[root@kalifun ~]# nginx -h
nginx version: nginx/1.16.1
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

Options:
  -?,-h         : this help
  -v            : show version and exit
  -V            : show version and configure options then exit
  -t            : test configuration and exit
  -T            : test configuration, dump it and exit
  -q            : suppress non-error messages during configuration testing
  -s signal     : send signal to a master process: stop, quit, reopen, reload
  -p prefix     : set prefix path (default: /etc/nginx/)
  -c filename   : set configuration file (default: /etc/nginx/nginx.conf)
  -g directives : set global directives out of configuration file
```

这就是命令行的魅力，看似简单的程序，其实隐藏着更多惊人的秘密，下面我们会结合`falg`来实现`Nginx`一样的命令行参数。

## 二、参数解析

接下来我们就一起探究，`falg`是如何实现命令行参数解析的吧。

通过分析上面`nginx -h`得知，命令行有两大部分(`Usage`和`Options`)。接下来主要针对这两部分讲，我们是如何用`flag`实现`nginx -h`的。

### Options参数类型

`flag`支持的命令行参数类型有`bool`,`duration`,`float64`,`int`,`int64`,`string`,`uint`,`uint64`。根据我们需要传入的参数选定需要的类型。

```
import "flag"
var ip = flag.Int("flagname", 1234, "help message for flagname")
```

这将声明一个整数`flag`,`-flagname`它存储在指针`ip`中，类型为`*int`。

- 第一个参数：flag名
- 第二个参数：flag的默认值
- 第三个参数：flag的描述信息

如果你喜欢，你还可以将`flag`绑定到变量上。

```
var flagvar int
func init() {
	flag.IntVar(&flagvar, "flagname", 1234, "help message for flagname")
}
```

这时候出现了四个参数，而第一个参数就是我们绑定的变量。

小伙伴会疑惑了，我知道了如何设计参数，可是我还是不知道怎么讲参数信息打印到终端上，怎么对我们输入的参数解析啊。那我们继续去探索，看flag是如何使用的。

### 命令行解析Parse

`flag.Parse`对命令行参数进行解析，我们需要搞清楚Parse有哪些解析方式：

`--flag value (需要注意两个--，后接空格)`

`-flag value（需要注意一个-，后接空格）`

`--flag=value（需要注意两个--，且使用的是=）`

`-flag=value（需要注意一个--，且使用的是=）`



下面我们看看实例，它是如何使用的：

```
package main

import (
	"flag"
	"fmt"
)

func main() {
	var age = flag.Int("age", 18, "this is age")
	flag.Parse()
	// 我们使用flag.Type这种类型，flagname只是保存了它的指针地址
	fmt.Println(*age)
}
```

我们将通过四种方式获取参数：

```
$ go run main.go -h
Usage of xxxxxxx\main.go:
  -age int
        this is age (default 18)
exit status 2


$ go run main.go
18

$ go run main.go -age 19
19

$ go run main.go --age 20
20

$ go run main.go -age=21
21

$ go run main.go --age=21
21
```

### 命令行Usage

如果自己看了上面实例的小伙伴，可以发现默认的`Usage`记录的是程序绝对路径，这样我们就无法实现`nginx -h`一样的效果，所以我们要引用`flag.Usage`。

由于`flag.Usage`是函数类型，所以使用覆盖默认函数实现，下面我们使用例子来看是如何覆盖的。

```
package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	var age = flag.Int("age", 18, "this is age")
	// 将默认的Usage替换成自定义usage
	flag.Usage = usage
	flag.Parse()
	fmt.Println(*age)
}

// 我们自定义usage函数
func usage() {
	fmt.Fprintf(os.Stderr, `nginx version: nginx/1.16.1
	Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]
	
	Options:`)
	// 显示所有已定义的命令行标志的默认设置，直至出现标准错误，直到出现标准错误。
	flag.PrintDefaults()
}
```

下面是效果：

```
$ go run main.go -h
nginx version: nginx/1.16.1
        Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

        Options:  -age int
        this is age (default 18)
exit status 2
```

## 三、开发工具

下面我们将结合上面学习的知识实现`nginx -h`的效果。

```
package main

import (
	"flag"
	"fmt"
	"os"
)

var (
	h bool
	v bool
	V bool
	t bool
	T bool
	q bool
	s string
	p string
	c string
	g string
)

func init() {
	flag.BoolVar(&h, "h", false, "this help")
	flag.BoolVar(&v, "v", false, "show version and exit")
	flag.BoolVar(&V, "V", false, "show version and configure options then exit")
	flag.BoolVar(&t, "t", false, "test configuration and exit")
	flag.BoolVar(&T, "T", false, "test configuration, dump it and exit")
	flag.BoolVar(&q, "q", false, "suppress non-error messages during configuration testing")
	flag.StringVar(&s, "s", "", "send `signal` to a master process: stop, quit, reopen, reload")
	flag.StringVar(&p, "p", "/etc/nginx/", "set `prefix` path")
	flag.StringVar(&c, "c", "/etc/nginx/nginx.conf", "set configuration `file`")
	flag.StringVar(&g, "g", "", "set global `directives` out of configuration file")
	flag.Usage = usage
}

func usage() {
	fmt.Fprintf(os.Stderr, `nginx version: nginx/1.16.1
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]
	
Options:
`)
	flag.PrintDefaults()
}

func main() {
	flag.Parse()
	if h {
		flag.Usage()
	}
}

```

下面是效果：

```
$ go run main.go -h
nginx version: nginx/1.16.1
Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

Options:
  -T    test configuration, dump it and exit
  -V    show version and configure options then exit
  -c file
        set configuration file (default "/etc/nginx/nginx.conf")
  -g directives
        set global directives out of configuration file
  -h    this help
  -p prefix
        set prefix path (default "/etc/nginx/")
  -q    suppress non-error messages during configuration testing
  -s signal
        send signal to a master process: stop, quit, reopen, reload
  -t    test configuration and exit
  -v    show version and exit
```

## 四、总结 

本文介绍了`flag`的基本用法，并没有将它的所有函数列举完整，如果有刚兴趣的小伙伴，可以到官网进一步学习。

## 参考文献

[Package flag](https://golang.google.cn/pkg/flag/)

[golang flag包使用笔记](https://www.jianshu.com/p/f9cf46a4de0e)