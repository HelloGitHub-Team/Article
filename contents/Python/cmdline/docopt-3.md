# Python 命令行之旅：使用 docopt 实现 git 命令

## 前言

在前面两篇介绍 `docopt` 的文章中，我们全面了解了 `docopt` 的能力。按照惯例，我们要像使用 `argparse` 一样使用 `docopt` 来实现 git 命令。

为了让没读过 `使用 argparse 实现 git 命令` 的小伙伴也能读明白本文，我们仍会对 git 常用命令和 gitpython 做一个简单介绍。

```plain
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## git 常用命令

当你写好一段代码或增删一些文件后，会用如下命令查看文件状态：

```bash
git status
```

确认文件状态后，会用如下命令将的一个或多个文件（夹）添加到暂存区：

```bash
git add [pathspec [pathspec ...]]
```

然后使用如下命令提交信息：

```bash
git commit -m "your commit message"
```

最后使用如下命令将提交推送到远程仓库：

```bash
git push
```

我们将使用 `docopt` 和 `gitpython` 库来实现这 4 个子命令。

## 关于 gitpython

[gitpython](https://gitpython.readthedocs.io/en/stable/intro.html) 是一个和 `git` 仓库交互的 Python 第三方库。
我们将借用它的能力来实现真正的 `git` 逻辑。

安装：

```bash
pip install gitpython
```

## 思考

在实现前，我们不妨先思考下会用到 `docopt` 的哪些功能？整个程序的结构是怎样的？

**docopt**

不同于使用 `argparse` 时需要考虑嵌套解析器、各类参数等问题，在使用 `docopt` 只需将我们要实现的 git 命令用接口描述先定义清楚即可。

**程序结构**

程序结构上，除了开头处定义接口描述外，其余和使用 `argparse` 实现 git 命令的结构是一样的：

- 命令行程序需要一个 `cli` 函数来作为统一的入口，它负责构建解析器，并解析命令行参数
- 我们还需要四个 `handle_xxx` 函数响应对应的子命令

则基本结构如下：

```python
import os
import docopt
from git.cmd import Git


def cli():
    """
    git 命名程序入口
    """
    pass


def handle_status(git):
    """
    处理 status 命令
    """
    pass

def handle_add(git, pathspec):
    """
    处理 add 命令
    """
    pass


def handle_commit(git, msg):
    """
    处理 -m <msg> 命令
    """
    pass


def handle_push(git):
    """
    处理 push 命令
    """
    pass


if __name__ == '__main__':
    cli()
```

下面我们将一步步地实现我们的 `git` 程序。

## 实现

假定我们在 [docopt-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/docopt-git.py) 文件中实现我们的 `git` 程序。

### 定义接口描述

根据我们的要求，可以很容易的定义出接口描述：

```bash
Usage:
    git status
    git add [<pathspec>...]
    git commit -m msg
    git push

Options:
  -h --help         Show help.
  -m --message msg  Commit with message.
```

进而就可以在 `cli()` 中解析命令行：

```python
def cli():
    """
    git 命名程序入口
    """
    args = docopt(__doc__)
    git = Git(os.getcwd())
```

### status 子命令

如果 `args['status']` 为 `True`，说明输入了 status 子命令，那么就调用 `handle_status` 函数进行处理。

```python
def cli():
    ...
    if args['status']:
        handle_status(git)


def handle_status(git):
    """
    处理 status 命令
    """
    cmd = ['git', 'status']
    output = git.execute(cmd)
    print(output)
```

不难看出，我们最后调用了真正的 `git status` 来实现，并打印了输出。

### add 子命令

如果 `args['add']` 为 `True`，说明输入了 add 子命令，那么就调用 `handle_add` 函数进行处理，需要传入 `args['<pathspec>']` 表示添加的路径。

```python
def cli():
    ...
    elif args['add']:
        handle_add(git, args['<pathspec>'])


def handle_add(git, pathspec):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + pathspec
    output = git.execute(cmd)
    print(output)
```

### commit 子命令

如果 `args['commit']` 为 `True`，说明输入了 commit 子命令，那么就调用 `handle_commit` 函数进行处理，需要传入 `args['--message']` 表示提交的信息。

```python
def cli():
    ...
    elif args['commit']:
        handle_commit(git, args['--message'])


def handle_commit(git, msg):
    """
    处理 -m <msg> 命令
    """
    cmd = ['git', 'commit', '-m', msg]
    output = git.execute(cmd)
    print(output)
```

### push 子命令

如果 `args['push']` 为 `True`，说明输入了 commit 子命令，那么就调用 `handle_push` 函数进行处理。

```python
def cli():
    ...
    elif args['push']:
        handle_push(git)


def handle_push(git):
    """
    处理 push 命令
    """
    cmd = ['git', 'push']
    output = git.execute(cmd)
    print(output)
```

至此，我们就实现了一个简单的 `git` 命令行，使用 `python docopt-git.py status` 便可查询项目状态。

想看整个源码，请戳 [docopt-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/docopt-git.py) 。

## 小结

本文简单介绍了日常工作中常用的 `git` 命令，然后提出实现它的思路，最终一步步地使用 `docopt` 和 `gitpython` 实现了 `git` 程序。

对比 `argparse` 的实现版本，你会发现使用 `docopt` 来实现变得非常简单，子解析器、参数类型什么的统统不需要关心！这可以说是 `docopt` 最大的优势了。

关于 `docopt` 的讲解将告一段落，回顾下 `docopt` 的三步曲，加上今天的内容，感觉它的使用方式还是比 `argparse` 简单不少的。

现在，你已学会了两个命令行解析库的使用了。但你以为这就够了吗？

但人类的智慧是多么璀璨呀，有些人并不喜欢这两个库的使用方式，于是他们有开辟了一个全新的思路。

在下篇文章中，将为大家介绍一个在 Python 界十分流行的命令行库 —— `click`。
