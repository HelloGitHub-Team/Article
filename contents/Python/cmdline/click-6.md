# Python 命令行之旅：使用 click 实现 git 命令

## 一、前言

在前面五篇介绍 `click` 的文章中，我们全面了解了 `click` 的强大能力。按照惯例，我们要像使用 `argparse` 和 `docopt` 一样使用 `click` 来实现 git 命令。

本文的关注点并不在 `git` 的各种命令是如何实现的，而是怎么使用 `click` 去打造一个实用命令行程序，代码结构是怎样的。因此，和 `git` 相关的操作，将会使用 `gitpython` 库来简单实现。

为了让没读过 `使用 xxx 实现 git 命令`（`xxx` 指 `argparse` 和 `docopt`） 的小伙伴也能读明白本文，我们仍会对 `git` 常用命令和 `gitpython` 做一个简单介绍。

```plain
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、git 常用命令

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

我们将使用 `click` 和 `gitpython` 库来实现这 4 个子命令。

## 三、关于 gitpython

[gitpython](https://gitpython.readthedocs.io/en/stable/intro.html) 是一个和 `git` 仓库交互的 Python 第三方库。
我们将借用它的能力来实现真正的 `git` 逻辑。

安装：

```bash
pip install gitpython
```

## 四、思考

在实现前，我们不妨先思考下会用到 `click` 的哪些功能？整个程序的结构是怎样的？

**click**

`git` 的 4 个子命令的实现其实对应于四个函数，每个函数使用 `click` 的 `command` 来装饰。
而对于 `git add` 和 `git commit`，则分别需要表示参数的 `click.argument` 和表示选项的 `click.option` 来装饰。

**程序结构**

程序结构上：

- 实例化 `Git` 对象，供全局使用
- 定义 `cli` 函数作为命令组，也就是整个命令程序的入口
- 定义四个命令对应的实现函数 `status`、`add`、`commit`、`push`

则基本结构如下：

```python
import os
import click
from git.cmd import Git

git = Git(os.getcwd())


@click.group()
def cli():
    """
    git 命令行
    """
    pass


@cli.command()
def status():
    """
    处理 status 命令
    """
    pass


@cli.command()
@click.argument('pathspec', nargs=-1)
def add(pathspec):
    """
    处理 add 命令
    """
    pass


@cli.command()
@click.option('-m', 'msg')
def commit(msg):
    """
    处理 -m <msg> 命令
    """
    pass


@cli.command()
def push():
    """
    处理 push 命令
    """
    pass


if __name__ == '__main__':
    cli()
```

下面我们将一步步地实现我们的 `git` 程序。

## 五、实现

假定我们在 [click-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/click-git.py) 文件中实现我们的 `git` 程序。

### 5.1 status 子命令

`status` 子命令不接受任何参数和选项，因此其实现函数只需 `cli.command()` 装饰。

```python
@cli.command()
def status():
    """
    处理 status 命令
    """
    cmd = ['git', 'status']
    output = git.execute(cmd)
    click.echo(output)
```

不难看出，我们最后调用了真正的 `git status` 来实现，并打印了输出。

### 5.2 add 子命令

`add` 子命令相对于 `status` 子命令，需要接受任意个 pathspec 参数，因此增加一个 `click.argument` 装饰器，并且在 `add` 函数中需要增加同名的 `pathspec` 入参。
经 `click` 处理后的 `pathspec` 其实是个元组，和列表相加前，需要先转换为列表。

```python
@cli.command()
@click.argument('pathspec', nargs=-1)
def add(pathspec):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + list(pathspec)
    output = git.execute(cmd)
    click.echo(output)
```

当我们执行 `python3 click-git.py add --help` 时，结果如下：

```plain
Usage: click-git.py add [OPTIONS] [PATHSPEC]...

  处理 add 命令

Options:
  --help  Show this message and exit.
```

既然 `git add` 能接受任意多个 `pathspec`，那么 `add(pathspec)` 的参数其实改为复数形式更为合适，但我们又希望帮助信息中是单数形式，这就需要额外指定 `metavar`，则有：

```python
@cli.command()
@click.argument('pathspecs', nargs=-1, metavar='[PATHSPEC]...')
def add(pathspecs):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + list(pathspecs)
    output = git.execute(cmd)
    click.echo(output)
```

### 5.3 commit 子命令

`add` 子命令相对于 `status` 子命令，需要接受 `-m` 选项，因此增加一个 `click.option` 装饰器，指定选项名称 `msg`，并且在 `commit` 函数中增加同名入参。

```python
@cli.command()
@click.option('-m', 'msg')
def commit(msg):
    """
    处理 -m <msg> 命令
    """
    cmd = ['git', 'commit', '-m', msg]
    output = git.execute(cmd)
    click.echo(output)
```

### 5.4 push 子命令

`push` 子命令同 `status` 子命令一样，不接受任何参数和选项，因此其实现函数只需 `cli.command()` 装饰。

```python
@cli.command()
def push():
    """
    处理 push 命令
    """
    cmd = ['git', 'push']
    output = git.execute(cmd)
    click.echo(output)
```

至此，我们就实现了一个简单的 `git` 命令行，使用 `python click-git.py status` 便可查询项目状态。

非常方便的是，每个命令函数的 `docstring` 都将作为这个命令的帮助信息，因此，当我们执行 `python3 click-git.py --help` 会自动生成如下帮助内容：

```plain
Usage: click-git.py [OPTIONS] COMMAND [ARGS]...

  git 命令行

Options:
  --help  Show this message and exit.

Commands:
  add     处理 add 命令
  commit  处理 -m <msg> 命令
  push    处理 push 命令
  status  处理 status 命令
```

想看整个源码，请戳 [click-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/click-git.py) 。

## 六、小结

本文简单介绍了日常工作中常用的 `git` 命令，然后提出实现它的思路，最终一步步地使用 `click` 和 `gitpython` 实现了 `git` 程序。

对比 `argparse` 和 `click` 的实现版本，你会发现使用 `click` 来实现变得特定简单：

- 相较于 `argparse`，子解析器、参数类型什么的统统不需要关心
- 相较于 `docopt`，参数解析和命令调用处理也不需要关心

这无疑是 `click` 最大的优势了。

关于 `click` 的讲解将告一段落，回顾下 `click` 的至简之道，你会爱上它。

现在，你已学会了三个命令行解析库的使用了。但你以为这就够了吗？`click` 已经够简单了吧，够直接了吧？但它仍然不是最简单的。

在下篇文章中，将为大家介绍一个由谷歌出品的在 Python 界很火的命令行库 —— `fire`。
