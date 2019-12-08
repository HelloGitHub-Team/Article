# Python 命令行之旅：深入 click（四）

## 一、前言

在前面三篇文章中，我们介绍了 `click` 中的参数、选项和命令，本文将介绍 `click` 锦上添花的功能，以帮助我们更加轻松地打造一个更加强大的命令行程序。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、增强功能

### 2.1 Bash 补全

Bash 补全是 `click` 提供的一个非常便捷和强大的功能，这是它比 `argpase` 和 `docopt` 强大的一个表现。

在命令行程序正确安装后，Bash 补全才可以使用。而如何安装可以参考 [setup 集成](https://click.palletsprojects.com/en/7.x/setuptools/#setuptools-integration)。Click 目前仅支持 Bash 和 Zsh 的补全。

#### 2.1.1 补全能力

通常来说，Bash 补全支持对子命令、选项、以及选项或参数值得补全。比如：

```plain
$ repo <TAB><TAB>
clone    commit   copy     delete   setuser
$ repo clone -<TAB><TAB>
--deep     --help     --rev      --shallow  -r
```

此外，`click` 还支持自定义补全，这在动态生成补全场景中很有用，使用 `autocompletion` 参数。`autocompletion` 需要指定为一个回调函数，并且返回字符串的列表。此函数接受三个参数：

- `ctx` —— 当前的 click 上下文
- `args` 传入的参数列表
- `incomplete` 正在补全的词

这里有一个根据环境变量动态生成补全的示例：

```python
import os

def get_env_vars(ctx, args, incomplete):
    return [k for k in os.environ.keys() if incomplete in k]

@click.command()
@click.argument("envvar", type=click.STRING, autocompletion=get_env_vars)
def cmd1(envvar):
    click.echo('Environment variable: %s' % envvar)
    click.echo('Value: %s' % os.environ[envvar])
```

在 `ZSH` 中，还支持补全帮助信息。只需将 `autocompletion` 回调函数中返回的字符串列表中的字符串改为二元元组，第一个元素是补全内容，第二个元素是帮助信息。

这里有一个颜色补全的示例：

```python
import os

def get_colors(ctx, args, incomplete):
    colors = [('red', 'help string for the color red'),
              ('blue', 'help string for the color blue'),
              ('green', 'help string for the color green')]
    return [c for c in colors if incomplete in c[0]]

@click.command()
@click.argument("color", type=click.STRING, autocompletion=get_colors)
def cmd1(color):
    click.echo('Chosen color is %s' % color)
```

#### 2.1.2 激活补全

要激活 Bash 的补全功能，就需要告诉它你的命令行程序有补全的能力。通常通过一个神奇的环境变量 `_<PROG_NAME>_COMPLETE` 来告知，其中 `<PROG_NAME>` 是大写下划线形式的程序名称。

比如有一个命令行程序叫做 `foo-bar`，那么对应的环境变量名称为 `_FOO_BAR_COMPLETE`，然后在 `.bashrc` 中使用 `source` 导出即可：

````bash
eval "$(_FOO_BAR_COMPLETE=source foo-bar)"
···

或者在 `.zshrc` 中使用：
```bash
eval "$(_FOO_BAR_COMPLETE=source_zsh foo-bar)"
````

不过上面的方式总是在命令行程序启动时调用，这可能在有多个程序时减慢 shell 激活的速度。另一种方式是把命令放在文件中，就像这样：

```bash
# 针对 Bash
_FOO_BAR_COMPLETE=source foo-bar > foo-bar-complete.sh

# 针对 ZSH
_FOO_BAR_COMPLETE=source_zsh foo-bar > foo-bar-complete.sh
```

然后把脚本文件路径加到 `.bashrc` 或 `.zshrc` 中：

```bash
. /path/to/foo-bar-complete.sh
```

### 2.2 实用工具

#### 2.2.1 打印到标准输出

[echo()](https://click.palletsprojects.com/en/7.x/api/#click.echo) 函数可以说是最有用的实用工具了。它和 Python 的 `print` 类似，主要的区别在于它同时在 Python 2 和 3 中生效，能够智能地检测未配置正确的输出流，且几乎不会失败（除了 Python 3 中的[少数限制](https://click.palletsprojects.com/en/7.x/python3/#python3-limitations)。）

`echo` 即支持 unicode，也支持二级制数据，如：

```python
import click

click.echo('Hello World!')

click.echo(b'\xe2\x98\x83', nl=False) # nl=False 表示不输出换行符
```

#### 2.2.2 ANSI 颜色

有些时候你可能希望输出是有颜色的，这尤其在输出错误信息时有用，而 `click` 在这方面支持的很好。

首先，你需要安装 `colorama`：

```bash
pip install colorama
```

然后，就可以使用 [style()](https://click.palletsprojects.com/en/7.x/api/#click.style) 函数来指定颜色：

```python
import click

click.echo(click.style('Hello World!', fg='green'))
click.echo(click.style('Some more text', bg='blue', fg='white'))
click.echo(click.style('ATTENTION', blink=True, bold=True))
```

`click` 还提供了更加简便的函数 [secho](https://click.palletsprojects.com/en/7.x/api/#click.secho)，它就是 `echo` 和 `style` 的组合：

```python
click.secho('Hello World!', fg='green')
click.secho('Some more text', bg='blue', fg='white')
click.secho('ATTENTION', blink=True, bold=True)
```

#### 2.2.3 分页支持

有些时候，命令行程序会输出长文本，但你希望能让用户盘也浏览。使用 [echo_via_pager()](https://click.palletsprojects.com/en/7.x/api/#click.echo_via_pager) 函数就可以轻松做到。

例如：

```python
def less():
    click.echo_via_pager('\n'.join('Line %d' % idx
                                   for idx in range(200)))
```

如果输出的文本特别大，处于性能的考虑，希望翻页时生成对应内容，那么就可以使用生成器：

```python
def _generate_output():
    for idx in range(50000):
        yield "Line %d\n" % idx

@click.command()
def less():
    click.echo_via_pager(_generate_output())
```

#### 2.2.4 清除屏幕

使用 [clear()](https://click.palletsprojects.com/en/7.x/api/#click.clear) 可以轻松清除屏幕内容：

```python
import click
click.clear()
```

#### 2.2.5 从终端获取字符

通常情况下，使用内建函数 `input` 或 `raw_input` 获得的输入是用户输出一段字符然后回车得到的。但在有些场景下，你可能想在用户输入单个字符时就能获取到并且做一定的处理，这个时候 [getchar()](https://click.palletsprojects.com/en/7.x/api/#click.getchar) 就派上了用场。

比如，根据输入的 `y` 或 `n` 做特定处理：

```python
import click

click.echo('Continue? [yn] ', nl=False)
c = click.getchar()
click.echo()
if c == 'y':
    click.echo('We will go on')
elif c == 'n':
    click.echo('Abort!')
else:
    click.echo('Invalid input :(')
```

#### 2.2.6 等待按键

在 Windows 的 cmd 中我们经常看到当执行完一个命令后，提示按下任意键退出。通过使用 [pause()](https://click.palletsprojects.com/en/7.x/api/#click.pause) 可以实现暂停直至用户按下任意键：

```python
import click
click.pause()
```

#### 2.2.7 启动编辑器

通过 [edit()](https://click.palletsprojects.com/en/7.x/api/#click.edit) 可以自动启动编辑器。这在需要用户输入多行内容时十分有用。

在下面的示例中，会启动默认的文本编辑器，并在里面输入一段话：

```python
import click

def get_commit_message():
    MARKER = '# Everything below is ignored\n'
    message = click.edit('\n\n' + MARKER)
    if message is not None:
        return message.split(MARKER, 1)[0].rstrip('\n')
```

`edit()` 函数还支持打开特定文件，比如：

```python
import click
click.edit(filename='/etc/passwd')
```

#### 2.2.8 启动应用程序

通过 [launch](https://click.palletsprojects.com/en/7.x/api/#click.launch) 可以打开 URL 或文件类型所关联的默认应用程序。如果设置 `locate=True`，则可以启动文件管理器并自动选中特定文件。

示例：

```python
# 打开浏览器，访问 URL
click.launch("https://click.palletsprojects.com/")

# 使用默认应用程序打开 txt 文件
click.launch("/my/downloaded/file.txt")

# 打开文件管理器，并自动选中 file.txt
click.launch("/my/downloaded/file.txt", locate=True)
```

#### 2.2.9 显示进度条

`click` 内置了 [progressbar()](https://click.palletsprojects.com/en/7.x/api/#click.progressbar) 函数来方便地显示进度条。

它的用法也很简单，假定你有一个要处理的可迭代对象，处理完每一项就要输出一下进度，那么就有两种用法。

用法一：使用 `progressbar` 构造出 `bar` 对象，迭代 `bar` 对象来自动告知进度：

```python
import time
import click

all_the_users_to_process = ['a', 'b', 'c']

def modify_the_user(user):
    time.sleep(0.5)

with click.progressbar(all_the_users_to_process) as bar:
    for user in bar:
        modify_the_user(user)
```

用法二：使用 `progressbar` 构造出 `bar` 对象，迭代原始可迭代对象，并不断向 `bar` 更新进度：

```python
import time
import click

all_the_users_to_process = ['a', 'b', 'c']

def modify_the_user(user):
    time.sleep(0.5)

with click.progressbar(all_the_users_to_process) as bar:
    for user in enumerate(all_the_users_to_process):
        modify_the_user(user)
        bar.update(1)
```

#### 2.2.10 更多实用工具

- [打印文件名](https://click.palletsprojects.com/en/7.x/utils/#printing-filenames)
- [标准流](https://click.palletsprojects.com/en/7.x/utils/#standard-streams)
- [智能打开文件](https://click.palletsprojects.com/en/7.x/utils/#intelligent-file-opening)
- [查找应用程序文件夹](https://click.palletsprojects.com/en/7.x/utils/#finding-application-folders)

## 三、总结

`click` 提供了非常多的增强型功能，本文着重介绍了它的 Bash 补全和十多个实用工具，这会让你在实现命令行的过程中如虎添翼。此外，`click` 还提供了诸如命令别名、参数修改、标准化令牌、调用其他命令、回调顺序等诸多[高级模式](https://click.palletsprojects.com/en/7.x/advanced/) 以应对更加复杂或特定的场景，我们就不再深入介绍。

`click` 的介绍就告一段落，它将会是你编写命令行程序的一大利器。在下一篇文章中，我们依然会通过实现一个简单的 `git` 程序来进行 `click` 的实战。
