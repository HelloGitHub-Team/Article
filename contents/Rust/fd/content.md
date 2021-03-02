# 开源文件搜索神器

![](./images/1.jpeg)

这是 HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，今天给大家推荐一个Rust 开源的文件搜索工具 —— [fd](https://github.com/sharkdp/fd)

## 一、fd 简介

你还在为寻找文件而烦恼吗？你还在为记不住 `find` 一大堆参数而烦恼吗？那就赶快来看看我这次推荐的项目 fd 吧！

> 项目地址：[https://github.com/sharkdp/fd](https://github.com/sharkdp/fd) 
>
> 官方简介：A simple, fast and user-friendly alternative to 'find'

我这里先放一个图，让大家直观的感受下

![](./images/2.svg)

fd 是一个命令行工具，提供了多种方便的选项进行文件的搜索。项目本身是由 Rust 语言编写的，作为系统级编程语言 Rust 拥有媲美 C++ 的运行速度，那 fd 的速度自然也不在话下，更优秀的是，他提供了强大功能方便用户按照各种条件进行搜索。

这个优秀的项目是不是成功的引起了你的注意呢～

![](./images/3.png)

## 二、fd 如何安装

作为使用的第一步当然是要先安装啦～

fd 提供了各个操作系统平台的安装方式，再不济可以直接通过源码进行安装（前提是有 Rust 的环境噢）

### 2.1 一键安装

我这里以我本地的 Mac 使用 `brew` 为例

```
$ brew install fd
```

`brew` 也可以一键升级

```
$ brew upgrade fd
```

具体各个平台的你可以看这里 [安装](https://github.com/chinanf-boy/fd-zh#%E5%AE%89%E8%A3%85)

### 2.2 源码安装

```
$ git clone https://github.com/sharkdp/fd.git
$ cd fd
$ cargo install --path .
```

### 2.3 查看帮助

无论哪种方式安装完成后，就可以直接使用了 `-h` 或 `--help` 获取帮助了，`--help` 就不演示了，区别就是换成了详细的帮助说明

```
$ fd -h
fd 8.2.1

USAGE:
    fd [FLAGS/OPTIONS] [<pattern>] [<path>...]

FLAGS:
    -H, --hidden            Search hidden files and directories
    -I, --no-ignore         Do not respect .(git|fd)ignore files
...
```

## 三、fd 快速上手演示

为了能让之后的演示有一个统一的认识，我这里新建了一个目录作为 fd 的测试目录，我虚构了一些文件和目录来模拟实际情况，该目录大致是这样，包括一个隐藏目录，我之后的演示都会基于该根目录下，选项如果有短名称和长名称，示例中以短名称为例

```
.
├── .hg
│   ├── HelloDjango.md
│   ├── HelloRust.md
│   ├── HelloVue.md
│   ├── HelloZooKeeper.md
├── dir1
│   ├── Hello.java
│   ├── World.java
│   └── dir2
│       ├── demo.py
│       ├── demo1.py
│       ├── dir3
│       │   ├── fd_demo.rs
│       │   └── fd_help.rs
│       └── sss.py
├── hello_fd.md
├── hello_java.md
├── java
│   ├── Hello.java
│   └── World.java
├── my_java.txt
├── python
│   ├── demo.py
│   ├── demo1.py
│   └── sss.py
└── rust
│   ├── fd_demo.rs
│   └── fd_help.rs
├── softdir3 -> dir1/dir2/dir3
└── sss.py -> dir1/dir2/sss.py
```

### 3.1 简单搜索

`fd` 直接跟想要搜索的内容，会递归搜索当前目录下的所有文件，列出文件名中包含目标内容的结果（结果当前目录的相对路径）

```
$ fd Hello
dir1/Hello.java
java/Hello.java
```

### 3.2 包含隐藏目录

选项 `-H` 或 ` --hidden`

```
$ fd -H Hello
.hg/HelloDjango.md
.hg/HelloRust.md
.hg/HelloVue.md
.hg/HelloZooKeeper.md
dir1/Hello.java
java/Hello.java
```

### 3.3 大小写

默认 `fd` 是匹配智能大小写的，如果你指定的是大写会按照精确匹配，但如果你指定的是小写会忽略大小写匹配，所以 `fd` 提供了两种选项来严格控制大小写匹配

选项 `-i` 或 ` --ignore-case`，忽略大小写

```
$ fd -i Hello
dir1/Hello.java
hello_fd.md
hello_java.md
java/Hello.java
```

选项 `-s` 或 ` --case-sensitive`，严格匹配大小写

```
$ fd -s hello
hello_fd.md
hello_java.md
```

### 3.4 返回完整绝对路径

选项 `-a` 或 ` --absolute-path`

```
$ fd -a Hello
/Users/junjiexun/fd_test/dir1/Hello.java
/Users/junjiexun/fd_test/java/Hello.java
```

### 3.5 返回详细文件列表

选项 `-l` 或 ` --list-details`，获得类似 `ls -l` 的效果

```
$ fd -l hello
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:42 dir1/Hello.java
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:37 hello_fd.md
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:37 hello_java.md
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:38 java/Hello.java
```

### 3.6 搜索内容包含全路径

选项 `-p` 或 ` --full-path`

```
$ fd xun
Nothing return...
$ fd -p xun
dir1
dir1/Hello.java
dir1/World.java
dir1/dir2
dir1/dir2/demo.py
dir1/dir2/demo1.py
dir1/dir2/dir3
dir1/dir2/dir3/fd_demo.rs
dir1/dir2/dir3/fd_help.rs
dir1/dir2/sss.py
hello_fd.md
hello_java.md
java
java/Hello.java
java/World.java
my_java.txt
python
python/demo.py
python/demo1.py
python/sss.py
rust
rust/fd_demo.rs
rust/fd_help.rs
softdir3
sss.py
```

### 3.7 包括 .gitignore 里的文件

选项 `-I` 或 ` --no-ignore`，我这里新建了一个 `.gitignore` 文件内容只有一个 `*.java` 用来演示，并且需要把当前目录通过 `git init` 初始化成 git 的项目

```
$ fd java
hello_java.md
java
my_java.txt
```

加上了 `-I` 之后结果中又包括了 `.java` 结尾的文件了

```
$ fd -I java
dir1/Hello.java
dir1/World.java
hello_java.md
java
java/Hello.java
java/World.java
my_java.txt
```

`-I` 功能我演示完了，我就将 `.gitignore` 和 `.git` 目录给删除了。

这些简单的功能已经可以一半的日常搜索需求了，接下来我们看看 `fd` 提供的更高级的搜索选项吧

![](./images/4.gif)

## 四、高级搜索选项

### 4.1 按深度

选项 `-d` 或 ` --max-depth <depth>`，当前路径算深度 1，`dir3` 下面的 `rs` 文件就是深度 4 了

```rust
$ fd rs
dir1/dir2/dir3/fd_demo.rs
dir1/dir2/dir3/fd_help.rs
rust/fd_demo.rs
rust/fd_help.rs
```

```
$ fd -d 3 rs
rust/fd_demo.rs
rust/fd_help.rs
```

### 4.2 按文件类型

选项 `-t` 或 ` --type <filetype>`，一共有以下几种 `filetype` 选项

-  f：file
- d：directory
-  l：symlink
- x：executable
- e：empty
- s：socket
- p：pipe

```
$ fd -t l
softdir3
sss.py
```

```
$ fd -t d
dir1
dir1/dir2
dir1/dir2/dir3
java
python
rust
```

我给所有的 py 文件都加了可执行权限

```
$ fd -t x
python/demo.py
python/demo1.py
python/sss.py
```

### 4.3 按扩展名

选项 `-e` 或 ` --extension <ext>`

```
$ fd -e md
hello_fd.md
hello_java.md
```

### 4.4 排除

选项 `-E` 或 ` --exclude <pattern>`，支持通配符

排除所有包含字母 `s` 的结果

```
$ fd -E '*s*'
dir1
dir1/Hello.java
dir1/World.java
dir1/dir2
dir1/dir2/demo.py
dir1/dir2/demo1.py
dir1/dir2/dir3
hello_fd.md
hello_java.md
java
java/Hello.java
java/World.java
my_java.txt
python
python/demo.py
python/demo1.py
```

可以看到所有的 rust、rs、sss、soft 都没有出现在结果集中

### 4.5 按所有者

选项 `-o` 或 ` --owner <user:group>`

```
$ fd -l -o junjiexun
drwxr-xr-x  5 junjiexun  staff   160B  3  1 18:42 dir1
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:42 dir1/Hello.java
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:42 dir1/World.java
drwxr-xr-x  6 junjiexun  staff   192B  3  1 18:42 dir1/dir2
-rw-r--r--  1 junjiexun  staff     0B  3  1 18:42 dir1/dir2/demo.py
...(略)
```

或者 `fd -l -o junjiexun:staff` 也可以达到同样的效果，但是 `fd` 不支持单独搜索 group，也不支持通配符。

### 4.6 组合命令

`fd` 提供了 `-x` 或 `--exec <cmd>`、`-X` 或 `--exec-batch <cmd>` 来进行对搜索结果集的进一步处理

找到所有和 java 匹配的内容并且删除！（仅仅用做演示，`rm -rf` 慎用）

```
$ fd java -X rm -rf
```

找到所有的 py 并且通过 vim 打开

```
$ fd py -X vim
```

还可以使用诸如 `unzip`、`ls`、`convert` 等等其他常用的命令，也可以直接使用 `|` 管道符语法进一步处理。

### 4.7 正则表达式

对于文件的内容搜索，我之前演示的是诸如 Hello、java、py 这样的完整文本，实际 `fd` 默认就是支持正则表达式对内容进行搜索的，但是正则表达式需要使用单引号包裹起来，我下面演示下

所有 s 开头的文件都能被搜索出来

```
$ fd '^s.*'
dir1/dir2/sss.py
python/sss.py
softdir3
sss.py
```

如果你不想使用正则表达式，想换成更简单的通配符匹配的话就可以使用选项 `-g` 或 `--glob` 

可以达到同样的效果

```
$ fd -g 's*'
dir1/dir2/sss.py
python/sss.py
softdir3
sss.py
```

## 五、总结

`fd` 是一个简单友好的命令行文件搜索工具，而且其开源的属性作为 Rust 源码学习的对象也是非常优秀的，给项目点个 star 吧，赶快行动起来吧～

顺便文章转评赞一波，每一个点赞的人，将来都会大富大贵，一夜暴富！

![](./images/5.png)