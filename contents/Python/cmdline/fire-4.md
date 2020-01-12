# Python 命令行之旅：使用 fire 实现 git 命令

## 一、前言

在前面三篇介绍 `fire` 的文章中，我们全面了解了 `fire` 强大而不失简洁的能力。按照惯例，我们要像使用 `argparse`、`docopt` 和 `click` 一样使用 `fire` 来实现 git 命令。

本文的关注点并不在 `git` 的各种命令是如何实现的，而是怎么使用 `fire` 去打造一个实用命令行程序，代码结构是怎样的。因此，和 `git` 相关的操作，将会使用 `gitpython` 库来简单实现。

为了让没读过 `使用 xxx 实现 git 命令`（`xxx` 指 `argparse`、`docopt` 和 `click`） 的小伙伴也能读明白本文，我们仍会对 `git` 常用命令和 `gitpython` 做一个简单介绍。

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

我们将使用 `fire` 和 `gitpython` 库来实现这 4 个子命令。

## 三、关于 gitpython

[gitpython](https://gitpython.readthedocs.io/en/stable/intro.html) 是一个和 `git` 仓库交互的 Python 第三方库。
我们将借用它的能力来实现真正的 `git` 逻辑。

安装：

```bash
pip install gitpython
```

## 四、思考

在实现前，我们不妨先思考下会用到 `fire` 的哪些功能？整个程序的结构是怎样的？

**fire**

`git` 的 4 个子命令的实现其实对应于四个函数，我们可以都放到一个类中，实现四个实例方法。
而对于 `git add` 命令，需要接受任意个参数，在实例方法中用 `*pathspecs` 参数来表达。
对于 `git commit` 命令，需要接受 `-m` 选项，在实例方法中用 `m` 参数来表达。

**程序结构**

程序结构上：

- 实例化 `Git` 对象，供全局使用
- 在 `GitCli` 类中定义四个命令对应的实例方法 `status`、`add`、`commit`、`push`

则基本结构如下：

```python
import os
import fire
from git.cmd import Git

git = Git(os.getcwd())

class GitCli:
    def status(self):
        """
        处理 status 命令
        """
        pass

    def add(self, *pathspecs):
        """
        处理 add 命令
        """
        pass

    def commit(self, m):
        """
        处理 -m <msg> 命令
        """
        pass

    def push(self):
        """
        处理 push 命令
        """
        pass


if __name__ == '__main__':
    fire.Fire(GitCli())
```

下面我们将一步步地实现我们的 `git` 程序。

## 五、实现

假定我们在 [fire-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/fire-git.py) 文件中实现我们的 `git` 程序。

### 5.1 status 子命令

`status` 子命令不接受任何参数和选项，因此 `status` 方法无需任何入参。

```python
class GitCli:
    def status(self):
        """
        处理 status 命令
        """
        cmd = ['git', 'status']
        output = git.execute(cmd)
        return output
```

不难看出，我们最后调用了真正的 `git status` 来实现，并打印了输出。

### 5.2 add 子命令

`add` 子命令相对于 `status` 子命令，需要接受任意个 pathspec 参数，因此 `add` 方法需要增加 `*pathspecs` 入参。
fire 最终传入的是一个元组，我们需要将其转换成 list 以便后续处理。

```python
class GitCli:
    def add(self, *pathspecs):
        """
        处理 add 命令
        """
        cmd = ['git', 'add'] + list(pathspecs)
        output = git.execute(cmd)
        return output
```

当我们执行 `python3 fire-git.py add --help` 时，结果如下：

```plain
INFO: Showing help with the command 'fire-git.py add -- --help'.

NAME
    fire-git.py add - 处理 add 命令

SYNOPSIS
    fire-git.py add [PATHSPECS]...

DESCRIPTION
    处理 add 命令

POSITIONAL ARGUMENTS
    PATHSPECS
```

### 5.3 commit 子命令

`commit` 子命令相对于 `status` 子命令，需要接受 `-m` 选项，因此 `commit` 方法需要增加 `m` 入参。

```python
class GitCli:
    def commit(self, m):
        """
        处理 -m <msg> 命令
        """
        cmd = ['git', 'commit', '-m', m]
        output = git.execute(cmd)
        return output
```

### 5.4 push 子命令

`push` 子命令同 `status` 子命令一样，不接受任何参数和选项，因此 `push` 方法无需任何入参。

```python
class GitCli:
    def push(self):
        """
        处理 push 命令
        """
        cmd = ['git', 'push']
        output = git.execute(cmd)
        return output
```

至此，我们就实现了一个简单的 `git` 命令行，使用 `python fire-git.py status` 便可查询项目状态。

非常方便的是，每个命令函数的 `docstring` 都将作为这个命令的帮助信息，因此，当我们执行 `python3 fire-git.py --help` 会自动生成如下帮助内容：

```plain
INFO: Showing help with the command 'fire-git.py -- --help'.

NAME
    fire-git.py

SYNOPSIS
    fire-git.py COMMAND

COMMANDS
    COMMAND is one of the following:

     add
       处理 add 命令

     commit
       处理 -m <msg> 命令

     push
       处理 push 命令

     status
       处理 status 命令
```

想看整个源码，请戳 [fire-git.py](https://github.com/HelloGitHub-Team/Article/blob/master/contents/Python/cmdline/fire-git.py) 。

## 六、小结

本文简单介绍了日常工作中常用的 `git` 命令，然后提出实现它的思路，最终一步步地使用 `fire` 和 `gitpython` 实现了 `git` 程序。

对比 `argparse`、`docopt` 和 `click` 的实现版本，你会发现使用 `fire` 来实现是最简单的：

- 相较于 `argparse`，子解析器、参数类型什么的统统不需要关心
- 相较于 `docopt`，参数解析和命令调用处理也不需要关心
- 相较于 `click`，装饰器所定义的命令行参数信息也必须要关心

无疑，`fire` 把能简化的都简化了，简直就是懒人福音。

关于 `fire` 的讲解将告一段落，回顾下 `fire` 的至简之道，你会深爱上它。这也体现出了 Python 之美。

现在，你已学会了四个特点各异的主流命令行解析库的使用了，再也不需要为命令行程序的实现而烦恼了。

什么，你为要使用哪一个库而发愁？在下一篇也是最后一篇文章中，我们将对这些库做一个横向对比，以对什么场景下使用什么样的命令行库了然于胸~
