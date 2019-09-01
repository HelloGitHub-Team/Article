# Python 命令行之旅：使用 argparse 实现 git 命令

## 前言

在前面三篇介绍 `argparse` 的文章中，我们全面了解了 `argparse` 的能力，相信不少小伙伴们都已经摩拳擦掌，想要打造一个属于自己的命令行工具。

本文将以我们日常工作中最常见的 `git` 命令为例，讲解如何使用 `argparse` 库来实现一个真正可用的命令行程序。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## git 常用命令

大家不妨回忆一下，平时最常使用 `git` 子命令都有哪些？

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

我们将使用 `argparse` 和 `gitpython` 库来实现这 4 个子命令。

## 关于 gitpython

[gitpython](https://gitpython.readthedocs.io/en/stable/intro.html) 是一个和 `git` 仓库交互的 Python 第三方库。
我们将借用它的能力来实现真正的 `git` 逻辑。

安装：

```bash
pip install gitpython
```

## 思考

在实现前，我们不妨先思考下会用到 `argparse` 的哪些功能？整个程序的结构是怎样的？

**argparse**

- 要实现子命令，那么之前介绍到的 `嵌套解析器` 必不可少
- 当用户键入子命令时，子命令所对应的子解析器需要作出响应，那么需要用到子解析器的 `set_defaults` 功能
- 针对 `git add [pathspec [pathspec ...]]`，我们需要实现位置参数，而且数量是任意个
- 针对 `git commit --message msg` 或 `git commit -m msg`，我们需要实现选项参数，且即可长选项，又可短选项

**程序结构**

- 命令行程序需要一个 `cli` 函数来作为统一的入口，它负责构建解析器，并解析命令行参数
- 我们还需要四个 `handle_xxx` 函数响应对应的子命令

则基本结构如下：

```python
import os
import argparse
from git.cmd import Git


def cli():
    """
    git 命名程序入口
    """
    pass


def handle_status(git, args):
    """
    处理 status 命令
    """
    pass

def handle_add(git, args):
    """
    处理 add 命令
    """
    pass


def handle_commit(git, args):
    """
    处理 -m <msg> 命令
    """
    pass


def handle_push(git, args):
    """
    处理 push 命令
    """
    pass


if __name__ == '__main__':
    cli()
```

下面我们将一步步地实现我们的 `git` 程序。

## 实现

假定我们在 [argparse-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/argparse-git.py) 文件中实现我们的 `git` 程序。

### 构建解析器

我们需要构建一个父解析器，作为程序的根解析器，程序名称指定为 `git`。然后在上面添加子解析器，为后续的子命令的解析做准备：

```python
def cli():
    """
    git 命名程序入口
    """
    parser = argparse.ArgumentParser(prog='git')
    subparsers = parser.add_subparsers(
        title='These are common Git commands used in various situations',
        metavar='command')
```

`add_subparsers` 中的 `title` 和 `metavar` 参数主要用于命令行帮助信息，最终的效果如下：

```bash
usage: git [-h] command ...

optional arguments:
  -h, --help  show this help message and exit

These are common Git commands used in various situations:
  command
    ...
```

### status 子命令

我们需要在 `cli` 函数中添加一个用于解析 `status` 命令的子解析器 `status_parser`，并指定其对应的处理函数为 `handle_status`。

```python
def cli():
    ...
    # status
    status_parser = subparsers.add_parser(
        'status',
        help='Show the working tree status')
    status_parser.set_defaults(handle=handle_status)
```

需要说明的是，在 `status_parser.set_defaults` 函数中，能接收任意名称的关键字参数，这个参数值会存放于父解析器解析命令行参数后的变量中。

比如，在本文示例程序中，我们为每个子解析器定义了 `handle`，那么 `args = parser.parse_args()` 中的 `args` 将具有 `handle` 属性，我们传入不同的子命令，那么这个 `handle` 就是不同的响应函数。

定义了 `status` 的子解析器后，我们再实现下 `handle_status` 即可实现 `status` 命令的响应：

```python
def handle_status(git, args):
    """
    处理 status 命令
    """
    cmd = ['git', 'status']
    output = git.execute(cmd)
    print(output)
```

不难看出，我们最后调用了真正的 `git status` 来实现，并打印了输出。

你可能会对 `handle_status` 的函数签名感到困惑，这里的 `git` 和 `args` 是怎么传入的呢？这其实是由我们自己控制的，将在本文最后讲解。

### add 子命令

同样，我们需要在 `cli` 函数中添加一个用于解析 `add` 命令的子解析器 `add_parser`，并指定其对应的处理函数为 `handle_add`。

额外要做的是，要在子解析器 `add_parser` 上添加一个 `pathspec` 位置参数，且其数量是任意的：

```python
def cli():
    ...
    # add
    add_parser = subparsers.add_parser(
        'add',
        help='Add file contents to the index')
    add_parser.add_argument(
        'pathspec',
        help='Files to add content from',
        nargs='*')
    add_parser.set_defaults(handle=handle_add)
```

然后，就是实现 `handle_add` 函数，我们需要用到表示文件路径的 `args.pathspec`：

```python
def handle_add(git, args):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + args.pathspec
    output = git.execute(cmd)
    print(output)
```

### commit 子命令

同样，我们需要在 `cli` 函数中添加一个用于解析 `commit` 命令的子解析器 `commit_parser`，并指定其对应的处理函数为 `handle_commit`。

额外要做的是，要在子解析器 `commit_parser` 上添加一个 `-m`/`--message` 选项参数，且要求必填：

```python
def cli():
    ...
    # commit
    commit_parser = subparsers.add_parser(
        'commit',
        help='Record changes to the repository')
    commit_parser.add_argument(
        '--message', '-m',
        help='Use the given <msg> as the commit message',
        metavar='msg',
        required=True)
    commit_parser.set_defaults(handle=handle_commit)
```

然后，就是实现 `handle_commit` 函数，我们需要用到表示提交信息的 `args.message`：

```python
def handle_commit(git, args):
    """
    处理 -m <msg> 命令
    """
    cmd = ['git', 'commit', '-m', args.message]
    output = git.execute(cmd)
    print(output)
```

### push 子命令

同样，我们需要在 `cli` 函数中添加一个用于解析 `push` 命令的子解析器 `push_parser`，并指定其对应的处理函数为 `handle_push`。

它同 `status` 子命令的实现方式一致：

```python
def cli():
    ...
    # push
    push_parser = subparsers.add_parser('push', help='Update remote refs along with associated objects')
    push_parser.set_defaults(handle=handle_push)
```

然后，就是实现 `handle_push` 函数，和 `handle_status` 类似：

```python
def handle_push(git, args):
    cmd = ['git', 'push']
    output = git.execute(cmd)
    print(output)
```

### 解析参数

在定义完父子解析器，并添加参数后，我们就需要对参数做解析，这项工作也是实现在 `cli` 函数中：

```python
def cli():
    ...
    git = Git(os.getcwd())
    args = parser.parse_args()
    if hasattr(args, 'handle'):
        args.handle(git, args)
    else:
        parser.print_help()
```

- 通过 `git.cmd.Git` 实例化出 `git` 对象，用来和 `git` 仓库交互
- 通过 `parser.parse_args()` 解析命令行
- 通过 `hasattr(args, 'handle')` 判断是否输入了子命令。
  - 由于每个子解析器都定义了 `handle`，那么如果当用户在命令行不输入任何命令时，`args` 就没有 `handle` 属性，那么我们就输出帮助信息
  - 如果用户输入了子命令，那么就调用 `args.handle`，传入 `git` 和 `args` 对象，用以处理对应命令

至此，我们就实现了一个简单的 `git` 命令行，使用 `python argparse-git.py -h` 查看帮助如下：

```bash
usage: git [-h] command ...

optional arguments:
  -h, --help  show this help message and exit

These are common Git commands used in various situations:
  command
    status    Show the working tree status
    add       Add file contents to the index
    commit    Record changes to the repository
    push      Update remote refs along with associated objects
```

然后我们就可以愉快地使用亲手打造的 `git` 程序啦！

想看整个源码，请戳 [argparse-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/argparse-git.py) 。

## 小节

本文简单介绍了日常工作中常用的 `git` 命令，然后提出实现它的思路，最终一步步地使用 `argparse` 和 `gitpython` 实现了 `git` 程序。是不是很有成就感呢？

关于 `argparse` 的讲解将告一段落，回顾下 `argparse` 的四步曲，加上今天的内容，感觉它还是挺清晰、简单的。
不过，这还只是打开了命令行大门的一扇门。

你是否想过，`argparse` 的四步曲虽然理解简单，但略微麻烦。有没有更简单的方式？
如果我很熟悉命令行帮助语法，我能不能写个帮助字符串就把所有的命令行元信息给定义出来？然后就直接轻松愉快地获取解析后的参数信息呢？

在下篇文章中，将为大家讲解另一个站在一个全新的思路，又无比强大的库 `docopt`。
