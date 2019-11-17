# Python 命令行之旅：深入 click（二）

## 一、前言

在上一篇文章中，我们介绍了 `click` 中的“参数”，本文将继续深入了解 `click`，着重讲解它的“选项”。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、选项

通过 `click.option` 可以给命令增加选项，并通过配置函数的参数来配置不同功能的选项。

### 2.1 给选项命名

`click.option` 中的命令规则可参考[参数名称](https://click.palletsprojects.com/en/7.x/parameters/#parameter-names)。它接受的前两个参数为长、短选项（顺序随意），其中：

- 长选项以 “--” 开头，比如 “--string-to-echo”
- 短选项以 “-” 开头，比如 “-s”

第三个参数为选项参数的名称，如果不指定，将会使用长选项的下划线形式名称：

```python
@click.command()
@click.option('-s', '--string-to-echo')
def echo(string_to_echo):
    click.echo(string_to_echo)
```

显示指定为 string

```python
@click.command()
@click.option('-s', '--string-to-echo', 'string')
def echo(string):
    click.echo(string)
```

### 2.2 基本值选项

值选项是非常常用的选项，它接受一个值。如果在命令行中提供了值选项，则需要提供对应的值；反之则使用默认值。若没在 `click.option` 中指定默认值，则默认值为 `None`，且该选项的类型为 [STRING](https://click.palletsprojects.com/en/7.x/api/#click.STRING)；反之，则选项类型为默认值的类型。

比如，提供默认值为 1，则选项类型为 [INT](https://click.palletsprojects.com/en/7.x/api/#click.INT)：

```python
@click.command()
@click.option('--n', default=1)
def dots(n):
    click.echo('.' * n)
```

如果要求选项为必填，则可指定 `click.option` 的 `required=True`：

```python
@click.command()
@click.option('--n', required=True, type=int)
def dots(n):
    click.echo('.' * n)
```

如果选项名称和 Python 中的关键字冲突，则可以显式的指定选项名称。比如将 `--from` 的名称设置为 `from_`：

```python
@click.command()
@click.option('--from', '-f', 'from_')
@click.option('--to', '-t')
def reserved_param_name(from_, to):
    click.echo(f'from {from_} to {to}')
```

如果要在帮助中显式默认值，则可指定 `click.option` 的 `show_default=True`：

```python
@click.command()
@click.option('--n', default=1, show_default=True)
def dots(n):
    click.echo('.' * n)
```

在命令行中调用则有：

```bash
$ dots --help
Usage: dots [OPTIONS]

Options:
  --n INTEGER  [default: 1]
  --help       Show this message and exit.
```

### 2.3 多值选项

有时，我们会希望命令行中一个选项能接收多个值，通过指定 `click.option` 中的 `nargs` 参数（必须是大于等于 0）。这样，接收的多值选项就会变成一个元组。

比如，在下面的示例中，当通过 `--pos` 指定多个值时，`pos` 变量就是一个元组，里面的每个元素是一个 `float`：

```python
@click.command()
@click.option('--pos', nargs=2, type=float)
def findme(pos):
    click.echo(pos)
```

在命令行中调用则有：

```bash
$ findme --pos 2.0 3.0
(1.0, 2.0)
```

有时，通过同一选项指定的多个值得类型可能不同，这个时候可以指定 `click.option` 中的 `type=(类型1, 类型2, ...)` 来实现。而由于元组的长度同时表示了值的数量，所以就无须指定 `nargs` 参数。

```python
@click.command()
@click.option('--item', type=(str, int))
def putitem(item):
    click.echo('name=%s id=%d' % item)
```

在命令行中调用则有：

```bash
$ putitem --item peter 1338
name=peter id=1338
```

### 2.4 多选项

不同于多值选项是通过一个选项指定多个值，多选项则是使用多个相同选项分别指定值，通过 `click.option` 中的 `multiple=True` 来实现。

当我们定义如下多选项：

```python
@click.command()
@click.option('--message', '-m', multiple=True)
def commit(message):
    click.echo('\n'.join(message))
```

便可以指定任意数量个选项来指定值，获取到的 `message` 是一个元组：

```bash
$ commit -m foo -m bar --message baz
foo
bar
baz
```

### 2.5 计值选项

有时我们可能需要获得选项的数量，那么可以指定 `click.option` 中的 `count=True` 来实现。

最常见的使用场景就是指定多个 `--verbose` 或 `-v` 选项来表示输出内容的详细程度。

```python
@click.command()
@click.option('-v', '--verbose', count=True)
def log(verbose):
    click.echo(f'Verbosity: {verbose}')
```

在命令行中调用则有：

```bash
$ log -vvv
Verbosity: 3
```

通过上面的例子，`verbose` 就是数字，表示 `-v` 选项的数量，由此可以进一步使用该值来控制日志的详细程度。

### 2.6 布尔选项

布尔选项用来表示真或假，它有多种实现方式：

- 通过 `click.option` 的 `is_flag=True` 参数来实现：

```python
import sys

@click.command()
@click.option('--shout', is_flag=True)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

在命令行中调用则有：

```bash
$ info --shout
LINUX!!!!111
```

- 通过在 `click.option` 的选项定义中使用 `/` 分隔表示真假两个选项来实现：

```python
import sys

@click.command()
@click.option('--shout/--no-shout', default=False)
def info(shout):
    rv = sys.platform
    if shout:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)
```

在命令行中调用则有：

```bash
$ info --shout
LINUX!!!!111
$ info --no-shout
linux
```

在 Windows 中，一个选项可以以 `/` 开头，这样就会真假选项的分隔符冲突了，这个时候可以使用 `;` 进行分隔：

```python
@click.command()
@click.option('/debug;/no-debug')
def log(debug):
    click.echo(f'debug={debug}')

if __name__ == '__main__':
    log()
```

在 cmd 中调用则有：

```bash
> log /debug
debug=True
```

### 2.7 特性切换选项

所谓特性切换就是切换同一个操作对象的不同特性，比如指定 `--upper` 就让输出大写，指定 `--lower` 就让输出小写。这么来看，布尔值其实是特性切换的一个特例。

要实现特性切换选项，需要让多个选项都有相同的参数名称，并且定义它们的标记值 `flag_value`：

```python
import sys

@click.command()
@click.option('--upper', 'transformation', flag_value='upper',
              default=True)
@click.option('--lower', 'transformation', flag_value='lower')
def info(transformation):
    click.echo(getattr(sys.platform, transformation)())
```

在命令行中调用则有：

```bash
$ info --upper
LINUX
$ info --lower
linux
$ info
LINUX
```

在上面的示例中，`--upper` 和 `--lower` 都有相同的参数值 `transformation`：

- 当指定 `--upper` 时，`transformation` 就是 `--upper` 选项的标记值 `upper`
- 当指定 `--lower` 时，`transformation` 就是 `--lower` 选项的标记值 `lower`

进而就可以做进一步的业务逻辑处理。

### 2.8 选择项选项

`选择项选项` 和 上篇文章中介绍的 `选择项参数` 类似，只不过是限定选项内容，依旧是通过 `type=click.Choice` 实现。此外，`case_sensitive=False` 还可以忽略选项内容的大小写。

```python
@click.command()
@click.option('--hash-type',
              type=click.Choice(['MD5', 'SHA1'], case_sensitive=False))
def digest(hash_type):
    click.echo(hash_type)
```

在命令行中调用则有：

```bash
$ digest --hash-type=MD5
MD5

$ digest --hash-type=md5
MD5

$ digest --hash-type=foo
Usage: digest [OPTIONS]
Try "digest --help" for help.

Error: Invalid value for "--hash-type": invalid choice: foo. (choose from MD5, SHA1)

$ digest --help
Usage: digest [OPTIONS]

Options:
  --hash-type [MD5|SHA1]
  --help                  Show this message and exit.
```

### 2.9 提示选项

顾名思义，当提供了选项却没有提供对应的值时，会提示用户输入值。这种交互式的方式会让命令行变得更加友好。通过指定 `click.option` 中的 `prompt` 可以实现。

- 当 `prompt=True` 时，提示内容为选项的参数名称

```python
@click.command()
@click.option('--name', prompt=True)
def hello(name):
    click.echo(f'Hello {name}!')
```

在命令行调用则有：

```bash
$ hello --name=John
Hello John!
$ hello
Name: John
Hello John!
```

- 当 `prompt='Your name please'` 时，提示内容为指定内容

```python
@click.command()
@click.option('--name', prompt='Your name please')
def hello(name):
    click.echo(f'Hello {name}!')
```

在命令行中调用则有：

```bash
$ hello
Your name please: John
Hello John!
```

基于提示选项，我们还可以指定 `hide_input=True` 来隐藏输入，`confirmation_prompt=True` 来让用户进行二次输入，这非常适合输入密码的场景。

```python
@click.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
def encrypt(password):
    click.echo(f'Encrypting password to {password.encode("rot13")}')
```

当然，也可以直接使用 `click.password_option`：

```python
@click.command()
@click.password_option()
def encrypt(password):
    click.echo(f'Encrypting password to {password.encode("rot13")}')
```

我们还可以给提示选项设置默认值，通过 `default` 参数进行设置，如果被设置为函数，则可以实现动态默认值。

```python
@click.command()
@click.option('--username', prompt=True,
              default=lambda: os.environ.get('USER', ''))
def hello(username):
    print("Hello,", username)
```

详情请阅读 [Dynamic Defaults for Prompts](https://click.palletsprojects.com/en/7.x/options/#dynamic-defaults-for-prompts)。

### 2.10 范围选项

如果希望选项的值在某个范围内，就可以使用范围选项，通过指定 `type=click.IntRange` 来实现。它有两种模式：

- 默认模式（非强制模式），如果值不在区间范围内将会引发一个错误。如 `type=click.IntRange(0, 10)` 表示范围是 [0, 10]，超过该范围报错
- 强制模式，如果值不在区间范围内，将会强制选取一个区间临近值。如 `click.IntRange(0, None, clamp=True)` 表示范围是 [0, +∞)，小于 0 则取 0，大于 20 则取 20。其中 `None` 表示没有限制

```python
@click.command()
@click.option('--count', type=click.IntRange(0, None, clamp=True))
@click.option('--digit', type=click.IntRange(0, 10))
def repeat(count, digit):
    click.echo(str(digit) * count)

if __name__ == '__main__':
    repeat()
```

在命令行中调用则有：

```bash
$ repeat --count=1000 --digit=5
55555555555555555555
$ repeat --count=1000 --digit=12
Usage: repeat [OPTIONS]

Error: Invalid value for "--digit": 12 is not in the valid range of 0 to 10.
```

### 2.11 回调和优先

**回调**
通过 `click.option` 中的 `callback` 可以指定选项的回调，它会在该选项被解析后调用。回调函数的签名如下：

```python
def callback(ctx, param, value):
    pass
```

其中：

- ctx 是命令的上下文 [click.Context](https://click.palletsprojects.com/en/7.x/api/#click.Context)
- param 为选项变量 [click.Option](https://click.palletsprojects.com/en/7.x/api/#click.Option)
- value 为选项的值

使用回调函数可以完成额外的参数校验逻辑。比如，通过 --rolls 的选项来指定摇骰子的方式，内容为“{N}d{M}”，表示 M 面的骰子摇 N 次，N 和 M 都是数字。在真正的处理 rolls 前，我们需要通过回调函数来校验它的格式：

```python
def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@click.command()
@click.option('--rolls', callback=validate_rolls, default='1d6')
def roll(rolls):
    click.echo('Rolling a %d-sided dice %d time(s)' % rolls)
```

这样，当我们输入错误格式时，变会校验不通过：

```bash
$ roll --rolls=42
Usage: roll [OPTIONS]

Error: Invalid value for "--rolls": rolls need to be in format NdM
```

输入正确格式时，则正常输出信息：

```bash
$ roll --rolls=2d12
Rolling a 12-sided dice 2 time(s)
```

**优先**
通过 `click.option` 中的 `is_eager` 可以让该选项成为优先选项，这意味着它会先于所有选项处理。

利用回调和优先选项，我们就可以很好地实现 `--version` 选项。不论命令行中写了多少选项和参数，只要包含了 `--version`，我们就希望它打印版本就退出，而不执行其他选项的逻辑，那么就需要让它成为优先选项，并且在回调函数中打印版本。

此外，在 `click` 中每个选项都对应到命令处理函数的同名参数，如果不想把该选项传递到处理函数中，则需要指定 `expose_value=True`，于是有：

```python
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def hello():
    click.echo('Hello World!')
```

当然 `click` 提供了便捷的 `click.version_option` 来实现 `--version`：

```python
@click.command()
@click.version_option(version='0.1.0')
def hello():
    pass
```

### 2.12 Yes 选项

基于前面的学习，我们可以实现 Yes 选项，也就是对于某些操作，不提供 `--yes` 则进行二次确认，提供了则直接操作：

```python
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.command()
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')
```

当然 `click` 提供了便捷的 `click.confirmation_option` 来实现 Yes 选项：

```python
@click.command()
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def dropdb():
    click.echo('Dropped all tables!')
```

在命令行中调用则有：

```bash
$ dropdb
Are you sure you want to drop the db? [y/N]: n
Aborted!
$ dropdb --yes
Dropped all tables!
```

### 2.11 其他增强功能

`click` 支持从环境中读取选项的值，这是 `argparse` 所不支持的，可参阅官方文档的 [Values from Environment Variables](https://click.palletsprojects.com/en/7.x/options/#values-from-environment-variables) 和 [Multiple Values from Environment Values](https://click.palletsprojects.com/en/7.x/options/#multiple-values-from-environment-values)。

`click` 支持指定选项前缀，你可以不使用 `-` 作为选项前缀，还可使用 `+` 或 `/`，当然在一般情况下并不建议这么做。详情参阅官方文档的 [Other Prefix Characters](https://click.palletsprojects.com/en/7.x/options/#other-prefix-characters)

## 三、总结

可以看出，`click` 对命令行选项的支持非常丰富和强大，除了支持 `argarse` 所支持的所有选项类型外，还提供了诸如 `计值选项`、`特性切换选项`、`提示选项` 等更丰富的选项类型。此外，还提供了从环境中读变量等方便易用的增强功能。简直就是开发命令行程序的利器。

在下篇文章中，我们着重介绍下 `click` 的命令和组，这可是实现它的重要特性（任意嵌套命令）的方式。
