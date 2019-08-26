# Python 命令行之旅：深入 argparse（二）

## 前言

在上一篇“深入 argparse（一）”的文章中，我们深入了解了 `argparse` 的包括参数动作和参数类别在内的基本功能，具备了编写一个简单命令行程序的能力。本文将继续深入了解 `argparse` 的进阶玩法，一窥探其全貌，助力我们拥有实现复杂命令行程序的能力。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 帮助
### 自动生成帮助
当你在命令行程序中指定 `-h` 或 `--help` 参数时，都会输出帮助信息。而 `argparse` 可通过指定 `add_help` 入参为 `True` 或不指定，以达到自动输出帮助信息的目的。

```bash
>>> import argparse
>>> parser = argparse.ArgumentParser(add_help=True)
>>> parser.add_argument('--foo')
>>> parser.parse_args(['-h'])
usage: [-h] [--foo FOO]

optional arguments:
  -h, --help  show this help message and exit
  --foo FOO
```

如果 `add_help=False`，那么在命令行中指定 `-h` 则会报错：

```bash
>>> import argparse
>>> parser = argparse.ArgumentParser(add_help=False)
>>> parser.add_argument('--foo')
>>> parser.parse_args(['-h'])
usage: [--foo FOO]
: error: unrecognized arguments: -h
```

### 自定义帮助
`ArgumentParser` 使用 `formatter_class` 入参来控制所输出的帮助格式。
比如，通过指定 `formatter_class=argparse.RawTextHelpFormatter`，我们可以让帮助内容遵循原始格式：

```bash
>>> import argparse
>>> parser = argparse.ArgumentParser(
...     add_help=True,
...     formatter_class=argparse.RawTextHelpFormatter,
...     description="""
...     description
...         raw
...            formatted"""
... )
>>> parser.add_argument(
...     '-a', action="store_true",
...     help="""argument
...         raw
...             formatted
...     """
... )
>>>
>>> parser.parse_args(['-h'])
usage: [-h] [-a]

    description
        raw
           formatted

optional arguments:
  -h, --help  show this help message and exit
  -a          argument
                      raw
                          formatted
```

对比下不指定 `formatter_class` 的帮助输出，就可以发现 descirption 和 -a 两个帮助内容上的差异：

```bash
>>> import argparse
>>> parser = argparse.ArgumentParser(
...     add_help=True,
...     description="""
...     description
...         notraw
...            formatted"""
... )
>>> parser.add_argument(
...     '-a', action="store_true",
...     help="""argument
...         notraw
...             formatted
...     """
... )
>>> parser.parse_args(['-h'])
usage: [-h] [-a]

description notraw formatted

optional arguments:
  -h, --help  show this help message and exit
  -a          argument notraw formatted
```

## 参数组
有时候，我们需要给参数分组，以使得在显示帮助信息时能够显示到一起。

比如某命令行支持三个参数选项 `--user`、`--password`和`--push`，前两者需要放在一个名为 `authentication` 的分组中以表示它们是身份认证信息。那么我们可以用 `ArgumentParser.add_argument_group` 来满足：

```bash
>>> import argparse
>>> parser = argparse.ArgumentParser()
>>> group = parser.add_argument_group('authentication')
>>> group.add_argument('--user', action="store")
>>> group.add_argument('--password', action="store")
>>> parser.add_argument('--push', action='store')
>>> parser.parse_args(['-h'])
usage: [-h] [--user USER] [--password PASSWORD] [--push PUSH]

optional arguments:
  -h, --help           show this help message and exit
  --push PUSH

authentication:
  --user USER
  --password PASSWORD
```

可以看到，当我们输出帮助信息时，`--user` 和 `--password` 选项都出现在 `authentication` 分组中。


## 选项参数前缀
不知你是否注意到，在不同平台上命令行程序的选项参数前缀可能是不同的。比如在 Unix 上，其前缀是 `-`；而在 Windows 上，大多数命令行程序（比如 `findstr`）的选项参数前缀是 `/`。

在 `argparse` 中，选项参数前缀默认采用 Unix 命令行约定，也就是 `-`。但它也支持自定义前缀，下面是一个例子：

```bash
>>> import argparse
>>> 
>>> parser = argparse.ArgumentParser(
...     description='Option prefix',
...     prefix_chars='-+/',
... )
>>> 
>>> parser.add_argument('-power', action="store_false",
...                     default=None,
...                     help='Set power off',
...                     )
>>> parser.add_argument('+power', action="store_true",
...                     default=None,
...                     help='Set power on',
...                     )
>>> parser.add_argument('/win',
...                     action="store_true",
...                     default=False)
>>> parser.parse_args(['-power'])
Namespace(power=False, win=False)
>>> parser.parse_args(['+power', '/win'])
Namespace(power=True, win=True)
```

在这个例子中，我们指定了三个选项参数前缀 `-`、`+`和`/`，从而：
- 通过指定选项参数 `-power`，使得 `power=False`
- 通过指定选项参数 `+power`，使得 `power=True`
- 通过指定选项参数 `/win`，使得 `win=True`


## 共享解析器
有些时候我们需要共享解析器，以共享里面的参数配置。比如，我们的命令行工具需要支持对阿里云和 AWS 进行操作，两类操作都需要指定 `AccessKeyId` 和 `AccessKeySecret` 来表明用户身份和权限。那么共享解析器就显得尤为必要，这样就可以少去重复代码。

我们可以这样做，在 `base.py` 中定义一个父解析器，存放 `AccessKey` 相关参数配置，作为公用的解析器。由于后续的子解析器会自动生成帮助信息，这里的父解析器指定 `add_help=False` 以不自动生成帮助信息：
```python
# bash.py
import argparse

parser = argparse.ArgumentParser(add_help=False)

parser.add_argument('--ak-id', action="store")
parser.add_argument('--ak-secret', action="store")
```

然后就可以分别在 `ali.py` 和 `aws.py` 中分别定义子解析器，通过 `parents` 入参指定上述父解析器，从而继承公共的参数，并实现各自的参数：

```python
# ali.py
import argparse
import base

parser = argparse.ArgumentParser(
    parents=[base.parser],
)

parser.add_argument('--ros',
                    action="store_true",
                    default=False,
                    help='Using ROS service to orchestrate cloud resources')

print(parser.parse_args())
```

```python
# aws.py
import argparse
import base

parser = argparse.ArgumentParser(
    parents=[base.parser],
)

parser.add_argument('--cloudformation',
                    action="store_true",
                    default=False,
                    help='Using CloudFormation service to orchestrate cloud resources')

print(parser.parse_args())
```

最终通过 `-h` 参数分别看 `ali.py` 和 `aws.py` 所支持的参数，其中共同参数为 `--ak-id` 和 `--ak-secret`，特定参数分别为 `--ros` 和 `--cloudformation`：

```bash
$ python3 ali.py -h

usage: ali.py [-h] [--ak-id AK_ID] [--ak-secret AK_SECRET] [--ros]

optional arguments:
  -h, --help            show this help message and exit
  --ak-id AK_ID
  --ak-secret AK_SECRET
  --ros                 Using ROS service to orchestrate cloud resources
```

```bash
$ python3 aws.py -h

usage: aws.py [-h] [--ak-id AK_ID] [--ak-secret AK_SECRET] [--cloudformation]

optional arguments:
  -h, --help            show this help message and exit
  --ak-id AK_ID
  --ak-secret AK_SECRET
  --cloudformation      Using CloudFormation service to orchestrate cloud
                        resources
```

## 嵌套解析器
我们之前介绍的命令行中，使用形式通常是 `cli --a --b xxx`。但还有一种极为常见的命令行使用方式是 `cli subcmd --a --b xxx`。比如当我们要通过 `git` 推送标签时，会用到 `git push --tags`。

通过实现嵌套解析器，我们可以很容易地对这种子命令的形式进行解析。

在嵌套解析器中，我们定义一个父解析器来作为整个命令行的入口，再分别定义N个子解析器来对应N个子命令，由此即可实现整个功能。

在下面这个例子中，我们支持 `create` 和 `delete` 两个子命令，用来创建或删除指定路径。而 `delete` 命令支持 `--recursive` 参数来表明是否递归删除指定路径：

```python
# cli.py
import argparse

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')

# Create
create_parser = subparsers.add_parser(
    'create', help='Create a directory')
create_parser.add_argument(
    'dirname', action='store',
    help='New directory to create')

# Delete
delete_parser = subparsers.add_parser(
    'delete', help='Remove a directory')
delete_parser.add_argument(
    'dirname', action='store', help='The directory to remove')
delete_parser.add_argument(
    '--recursive', '-r', default=False, action='store_true',
    help='Recursively remove the directory',
)

print(parser.parse_args())
```

直接指定 `-h` 来查看所支持的子命令和参数选项：
```bash
$ python3 cli.py -h

usage: cli.py [-h] {create,delete} ...

positional arguments:
  {create,delete}  commands
    create         Create a directory
    delete         Remove a directory

optional arguments:
  -h, --help       show this help message and exit
```

直接指定 `delete -h` 来查看 `delete` 子命令支持的参数选项：
```bash
$ python3 cli.py delete -h

usage: cli.py delete [-h] [--recursive] dirname

positional arguments:
  dirname          The directory to remove

optional arguments:
  -h, --help       show this help message and exit
  --recursive, -r  Recursively remove the directory
```

## 自定义动作
在上一篇“深入 argparse （一）”的文章中介绍过8种参数动作，可以说是覆盖了绝大部分场景。但是也会有一些特定需求无法被满足，比如希望获取到的参数值都是大写。在这种情况下，自定义动作就派上了用场。

实现一个自定义动作类，需继承自 `argparse.Action`，这个自定义动作类要传入到 `ArgumentParser.add_argument` 的 `action` 入参。当解析器解析参数时，会调用该类的 `__call__` 方法，该方法的签名为 `__call__(self, parser, namespace, values, option_string=None) `，其中：
- parser 为解析器实例
- namespace 存放解析结果
- values 即命令行中传入的参数值
- option_string 为参数选项

在下面的例子中，我们通过 `--words` 传入单词，并在自定义动作类中将其值转换为大写：

```python
# cli.py
import argparse

class WordsAction(argparse.Action):

    def __call__(self, parser, namespace, values,
                 option_string=None):
        print(f'parser = {parser}')
        print(f'values = {values!r}')
        print(f'option_string = {option_string!r}')

        values = [v.upper() for v in values]
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument('--words', nargs='*', action=WordsAction)

results = parser.parse_args()
print(results)
```

```bash
$ python3 cli.py --words foo bar

parser = ArgumentParser(prog='cli.py', usage=None, description=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)
values = ['foo', 'bar']
option_string = '--words'
Namespace(words=['FOO', 'BAR'])
```

## 小节
通过对 `argparse`由浅入深的介绍，相信你已经全面了解了 `argparse` 的威力，也具备了开发命令行工具的能力。但“纸上得来终觉浅，绝知此事要躬行”。

在下篇文章中，将带大家一起用 `argparse` 实现日常工作中常见的 `git` 命令，想想是不是有些兴奋呢？
