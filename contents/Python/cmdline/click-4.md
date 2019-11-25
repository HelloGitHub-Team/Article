# Python 命令行之旅：深入 click（三）

## 一、前言

在上两篇文章中，我们介绍了 `click` 中的”参数“和“选项”，本文将继续深入了解 `click`，着重讲解它的“命令”和”组“。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、命令和组

`Click` 中非常重要的特性就是任意嵌套命令行工具的概念，通过 [Command](https://click.palletsprojects.com/en/7.x/api/#click.Command) 和 [Group](https://click.palletsprojects.com/en/7.x/api/#click.Group) （实际上是 [MultiCommand](https://click.palletsprojects.com/en/7.x/api/#click.MultiCommand)）来实现。

所谓命令组就是若干个命令（或叫子命令）的集合，也成为多命令。

### 2.1 回调调用

对于一个普通的命令来说，回调发生在命令被执行的时候。如果这个程序的实现中只有命令，那么回调总是会被触发，就像我们在上一篇文章中举出的所有示例一样。不过像 `--help` 这类选项则会阻止进入回调。

对于组和多个子命令来说，情况略有不同。回调通常发生在子命令被执行的时候：

```python
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()  # @cli, not @click!
def sync():
    click.echo('Syncing')
```

执行效果如下：

```bash
Usage: tool.py [OPTIONS] COMMAND [ARGS]...

Options:
  --debug / --no-debug
  --help                Show this message and exit.

Commands:
  sync

$ tool.py --debug sync
Debug mode is on
Syncing
```

在上面的示例中，我们将函数 `cli` 定义为一个组，把函数 `sync` 定义为这个组内的子命令。当我们调用 `tool.py --debug sync` 命令时，会依次触发 `cli` 和 `sync` 的处理逻辑（也就是命令的回调）。

### 2.2 嵌套处理和上下文

从上面的例子可以看到，命令组 `cli` 接收的参数和子命令 `sync` 彼此独立。但是有时我们希望在子命令中能获取到命令组的参数，这就可以用 [Context](https://click.palletsprojects.com/en/7.x/api/#click.Context) 来实现。

每当命令被调用时，`click` 会创建新的上下文，并链接到父上下文。通常，我们是看不到上下文信息的。但我们可以通过 [pass_context](https://click.palletsprojects.com/en/7.x/api/#click.pass_context) 装饰器来显式让 `click` 传递上下文，此变量会作为第一个参数进行传递。

```python
@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # 确保 ctx.obj 存在并且是个 dict。 (以防 `cli()` 指定 obj 为其他类型
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))

if __name__ == '__main__':
    cli(obj={})
```

在上面的示例中：

- 通过为命令组 `cli` 和子命令 `sync` 指定装饰器 `click.pass_context`，两个函数的第一个参数都是 `ctx` 上下文
- 在命令组 `cli` 中，给上下文的 `obj` 变量（字典）赋值
- 在子命令 `sync` 中通过 `ctx.obj['DEBUG']` 获得上一步的参数
- 通过这种方式完成了从命令组到子命令的参数传递

### 2.3 不使用命令来调用命令组

默认情况下，调用子命令的时候才会调用命令组。而有时你可能想直接调用命令组，通过指定 `click.group` 的 `invoke_without_command=True` 来实现：

```python
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('I was invoked without subcommand')
    else:
        click.echo('I am about to invoke %s' % ctx.invoked_subcommand)

@cli.command()
def sync():
    click.echo('The subcommand')
```

调用命令有：

```bash
$ tool
I was invoked without subcommand
$ tool sync
I am about to invoke sync
The subcommand
```

在上面的示例中，通过 `ctx.invoked_subcommand` 来判断是否由子命令触发，针对两种情况打印日志。

### 2.4 自定义命令组/多命令

除了使用 [click.group](https://click.palletsprojects.com/en/7.x/api/#click.group) 来定义命令组外，你还可以自定义命令组（也就是多命令），这样你就可以延迟加载子命令，这会很有用。

自定义多命令需要实现 `list_commands` 和 `get_command` 方法：

```python
import click
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'commands')

class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []  # 命令名称列表
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py'):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name + '.py')  # 命令对应的 Python 文件
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

cli = MyCLI(help='This tool\'s subcommands are loaded from a '
            'plugin folder dynamically.')

# 等价方式是通过 click.command 装饰器，指定 cls=MyCLI
# @click.command(cls=MyCLI)
# def cli():
#     pass

if __name__ == '__main__':
    cli()
```

### 2.5 合并命令组/多命令

当有多个命令组，每个命令组中有一些命令，你想把所有的命令合并在一个集合中时，`click.CommandCollection` 就派上了用场：

```python

@click.group()
def cli1():
    pass

@cli1.command()
def cmd1():
    """Command on cli1"""

@click.group()
def cli2():
    pass

@cli2.command()
def cmd2():
    """Command on cli2"""

cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
```

调用命令有：

```bash
$ cli --help
Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  cmd1  Command on cli1
  cmd2  Command on cli2
```

从上面的示例可以看出，`cmd1` 和 `cmd2` 分别属于 `cli1` 和 `cli2`，通过 `click.CommandCollection` 可以将这些子命令合并在一起，将其能力提供个同一个命令程序。

Tips：如果多个命令组中定义了同样的子命令，那么取第一个命令组中的子命令。

### 2.6 链式命令组/多命令

有时单级子命令可能满足不了你的需求，你甚至希望能有多级子命令。典型地，`setuptools` 包中就支持多级/链式子命令： `setup.py sdist bdist_wheel upload`。在 click 3.0 之后，实现链式命令组变得非常简单，只需在 `click.group` 中指定 `chain=True`：

```python
@click.group(chain=True)
def cli():
    pass


@cli.command('sdist')
def sdist():
    click.echo('sdist called')


@cli.command('bdist_wheel')
def bdist_wheel():
    click.echo('bdist_wheel called')
```

调用命令则有：

```bash
$ setup.py sdist bdist_wheel
sdist called
bdist_wheel called
```

### 2.7 命令组/多命令管道

链式命令组中一个常见的场景就是实现管道，这样在上一个命令处理好后，可将结果传给下一个命令处理。

实现命令组管道的要点是让每个命令返回一个处理函数，然后编写一个总的管道调度函数（并由 `MultiCommand.resultcallback()` 装饰）：

```python
@click.group(chain=True, invoke_without_command=True)
@click.option('-i', '--input', type=click.File('r'))
def cli(input):
    pass

@cli.resultcallback()
def process_pipeline(processors, input):
    iterator = (x.rstrip('\r\n') for x in input)
    for processor in processors:
        iterator = processor(iterator)
    for item in iterator:
        click.echo(item)

@cli.command('uppercase')
def make_uppercase():
    def processor(iterator):
        for line in iterator:
            yield line.upper()
    return processor

@cli.command('lowercase')
def make_lowercase():
    def processor(iterator):
        for line in iterator:
            yield line.lower()
    return processor

@cli.command('strip')
def make_strip():
    def processor(iterator):
        for line in iterator:
            yield line.strip()
    return processor
```

在上面的示例中：

- 将 `cli` 定义为了链式命令组，并且指定 invoke_without_command=True，也就意味着可以不传子命令来触发命令组
- 定义了三个命令处理函数，分别对应 `uppercase`、`lowercase` 和 `strip` 命令
- 在管道调度函数 `process_pipeline` 中，将输入 `input` 变成生成器，然后调用处理函数（实际输入几个命令，就有几个处理函数）进行处理

### 2.8 覆盖默认值

默认情况下，参数的默认值是从通过装饰器参数 `default` 定义。我们还可以通过 `Context.default_map` 上下文字典来覆盖默认值：

```python
@click.group()
def cli():
    pass

@cli.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

if __name__ == '__main__':
    cli(default_map={
        'runserver': {
            'port': 5000
        }
    })
```

在上面的示例中，通过在 `cli` 中指定 `default_map` 变可覆盖命令（一级键）的选项（二级键）默认值（二级键的值）。

我们还可以在 `click.group` 中指定 `context_settings` 来达到同样的目的：

```python

CONTEXT_SETTINGS = dict(
    default_map={'runserver': {'port': 5000}}
)

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('--port', default=8000)
def runserver(port):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

if __name__ == '__main__':
    cli()
```

调用命令则有：

```bash
$ cli runserver
Serving on http://127.0.0.1:5000/
```

## 三、总结

本文首先介绍了命令的回调调用、上下文，再进一步介绍命令组的自定义、合并、链接、管道等功能，了解到了 `click` 的强大。而命令组中更加高阶的能力（[如命令返回值](https://click.palletsprojects.com/en/7.x/commands/#command-return-values)）则可看官方文档进一步了解。

我们通过介绍 `click` 的参数、选项和命令已经能够完全实现命令行程序的所有功能。而 `click` 还为我们提供了许多锦上添花的功能，比如实用工具、参数自动补全等，我们将在下节详细介绍。
