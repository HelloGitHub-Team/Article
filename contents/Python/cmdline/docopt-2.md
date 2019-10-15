# Python 命令行之旅：深入 docopt

## 一、前言

在第一篇“初探 docopt”的文章中，我们初步掌握了使用 `docopt` 的三个步骤，了解了它不同于 `argparse` 的设计思路。
那么 `docopt` 的使用模式都有哪些呢？其接口描述中都支持哪些语法规则呢？本文将带你深入了解 `docopt`。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、使用模式

在上一篇文章中我们提到 `docopt` 是通过定义一个包含特定内容的字符串，也就是接口描述，来达到描述命令行功能的目的。
那么接口描述的总体规则是这样的：

- 位于关键字 `usage:` （大小写不敏感）和一个可见的空行之间的文本内容会被解释为一个个使用模式。
- `useage:` 后的第一个词会被解释为程序的名称，比如下面就是一个没有命令行参数的示例程序：

```
Usage: cli
```

- 接口描述中可以包含很多有各种元素的模式，以描述命令行用法，比如：

```
Usage:
  cli command --option <argument>
  cli [<optional-argument>]
  cli --another-option=<with-argument>
  cli (--either-that-option | <or-this-argument>)
  cli <repeating-argument> <repeating-argument>...
```

### 2.1 位置参数： <argument>

使用 `<` 和 `>` 包裹的参数会被解释为位置参数。

比如，我们可以指定两个位置参数 `x` 和 `y` ，先添加的 `x` 位于第一个位置，后加入的 `y` 位于第二个位置。那么在命令行中输入 `1 2`的时候，分别对应到的就是 `x` 和 `y`：

```python
"""
Usage: cli <x> <y>
"""
from docopt import docopt

arguments = docopt(__doc__, argv=['1', '2'])
print(arguments)
```

其输出为：

```python
{'<x>': '1',
 '<y>': '2'}
```

### 2.2 选项参数： -o --option

以单个破折号（`-`）开头的的参数为短选项，以双破折号（`--`）开头的参数为长选项。

- 短选项支持集中表达多个短选项，比如 `-abc` 等价于 `-a`、`-b` 和 `-c`
- 长选项后可跟参数，通过 `空格` 或 `=` 指定，比如 `--input ARG` 等价于 `--input=ARG`
- 短选项后可跟参数，通可选的 `空格` 指定，比如 `-f FILE` 等价于 `-fFILE`

在下面这个例子中，我们希望通过 `-n` h 或 `--name` 来指定名字：

```python
"""
Usage:
  cli [options]

Options:
  -n, --name NAME   Set name.
"""
from docopt import docopt

arguments = docopt(__doc__, argv=['-n', 'Eric'])
print(arguments)

arguments = docopt(__doc__, argv=['-nEric'])
print(arguments)

arguments = docopt(__doc__, argv=['--name', 'Eric'])
print(arguments)

arguments = docopt(__doc__, argv=['--name=Eric'])
print(arguments)
```

上面的示例中，我们通过 4 种方式（2 个短选项参数方式和 2 个长选项参数方式）来指定命令行输入，其输出均为：

```python
{'--name': 'Eric'}
```

需要注意的是：

`--input ARG`（而不是 `--input=ARG`）的含义是模糊不清的，因为这不能看出 `ARG` 究竟是选项参数，
还是位置参数。在 `docopt` 的使用模式中，只有在接口描述中定义了对应选项才会被解释为一个带参数的选项，
否则就会被解释为一个选项和一个独立的位置参数。

`-f FILE` 和 `-fFILE` 这种写法也有同样的模糊点。后者无法说明这究竟是一系列短选项的集合，
还是一个带参数的选项。只有在接口描述中定义了对应选项才会被解释为一个带参数的选项。

### 2.3 命令

这里的命令也就是 `argparse` 中嵌套解析器所要完成的事情，准确的说，对整个命令行程序来说，实现的是子命令。

在 `docopt` 中，凡是不符合 `--options` 或 `<arguments>` 约定的词，均会被解释为子命令。

在下面这个例子中，我们支持 `create` 和 `delete` 两个子命令，用来创建或删除指定路径。而 `delete` 命令支持 `--recursive` 参数来表明是否递归删除指定路径：

```python
"""
Usage:
  cli create
  cli delete [--recursive]

Options:
  -r, --recursive   Recursively remove the directory.
"""
from docopt import docopt

arguments = docopt(__doc__)
print(arguments)
```

直接指定 `delete -r`，输出如下：

```bash
$ python3 cli.py delete -r

{'--recursive': True,
 'create': False,
 'delete': True}
```

### 2.4 可选元素： [optional elements]

以中括号“[]”包裹的元素（选项、参数和命令）均会被标记为可选。多个元素放在一对中括号中或各自放在中括号中是等价的。比如：

```bash
Usage: cli [command --option <argument>]
```

等价于：

```bash
Usage: cli [command] [--option] [<argument>]
```

### 2.5 必填元素： (required elements)

没被中括号“[]”包裹的所有元素默认都是必填的。但有时候使用小括号“()”将元素包裹住，用以标记必填是有必要的。
比如，要将多个互斥元素进行分组：

```bash
Usage: my_program (--either-this <and-that> | <or-this>)
```

另一个例子是，当出现一个参数时，也要求提供另一个参数，那么就可以这么写：

```bash
Usage: my_program [(<one-argument> <another-argument>)]
```

这个例子中，`<one-argument>` 和 `<another-argument>` 要么都出现，要么都不出现。

### 2.6 互斥参数： element|another

在 `argparse` 中要想实现互斥参数，还需要先调用 `parser.add_mutually_exclusive_group()` 添加互斥组，
再在组里添加参数。而在 `docopt` 中就特别简单，直接使用 `|` 进行分隔：

```bash
Usage: my_program go (--up | --down | --left | --right)
```

在上面的示例中，使用小括号“()”来对四个互斥选项分组，要求必填其中一个选项。
在下面的示例中，使用中括号“()”来对四个互斥选项分组，可以不填，或填其中一个选项：

```bash
Usage: my_program go [--up | --down | --left | --right]
```

我们还可以发散一下思路，子命令天然需要互斥，那么除了这种写法：

```bash
Usage: my_program run [--fast]
       my_program jump [--high]
```

使用如下 `|` 的写法，也是等价的：

```bash
Usage: my_program (run [--fast] | jump [--high])
```

### 2.7 可变参数列表： element...

可变参数列表也就是定义参数可以有多个值。在 `argparse` 中，我们通过 `parser.add_argument('--foo', nargs='?')` 来指定，其中 `nargs` 可以是数字、`?`、`+`、`*`来表示参数个数。

在 `docopt` 中，自然也有相同的能力，使用省略号 `...` 来实现：

```bash
Usage: my_program open <file>...
       my_program move (<from> <to>)...
```

若要参数提供 N 个，则写 N 个参数即可，比如下面的示例中要求提供 2 个：

```
Usage: my_program <file> <file>
```

若要参数提供 0 个或多个，则配合中括号“[]”进行定义，如下 3 中定义方式等价：

```bash
Usage: my_program [<file>...]
       my_program [<file>]...
       my_program [<file> [<file> ...]]
```

若要参数提供 1 个或多个，则可以这么写：

```bash
Usage: my_program <file>...
```

在下面完整示例中，所获得的 `arguments` 是 `{'<file>': ['f1', 'f2']}`：

```python
"""
Usage:
  cli <file>...
"""
from docopt import docopt

arguments = docopt(__doc__, argv=['f1', 'f2'])
print(arguments)
```

### 2.8 选项简写： [options]

“[options]”用于简写选项，比如下面的示例中定义了 3 个选项：

```bash
Usage: my_program [--all --long --human-readable] <path>

--all             List everything.
--long            Long output.
--human-readable  Display in human-readable format.
```

可以简写为：

```bash
Usage: my_program [options] <path>

--all             List everything.
--long            Long output.
--human-readable  Display in human-readable format.
```

如果一个模式中有多个选项，那么这会很有用。

另外，如果选项包含长短选项，那么也可以用它们中的任意一个写在模式中，比如下面的示例的模式中均使用短选项：

```bash
Usage: my_program [-alh] <path>

-a, --all             List everything.
-l, --long            Long output.
-h, --human-readable  Display in human-readable format.
```

### 2.9 [--]

当双破折号“--”不是选项时，通常用于分隔选项和位置参数，以便处理例如将文件名误认为选项的情况。
为了支持此约定，需要在位置参数前添加 `[--]`。

```bash
Usage: my_program [options] [--] <file>...
```

### 2.10 [-]

当单破折号“-”不是选项时，通常用于表示程序应处理 `stdin`，而非文件。为了支持此约定，需要在使用模式中加入 `[-]`。

### 2.11 选项描述

选项描述就是描述一系列选项参数的模式。如果使用模式中的选项定义是清晰的，那么选项描述就是可选的。

选项描述可以定义如下内容：

- 短选项和长选项代表相同含义
- 带参数的选项
- 有默认值的选项参数

选项描述的每一行需要以 `-` 或 `--` 开头（不算空格），比如：

```bash
Options:
  --verbose   # 好
  -o FILE     # 好
Other: --bad  # 坏, 没有以 "-" 开头
```

选项描述中，使用空格或“=”来连接选项和参数，以定义带选项的参数。参数可以使用`<Arg>`的形式，
或是使用`ARG`大写字母的形式。可用逗号“,”来分隔长短选项。比如：

```bash
-o FILE --output=FILE       # 没有逗号 长选项使用 "=" 分隔
-i <file>, --input <file>   # 有逗号, 长选项使用空格分隔
```

选项描述中每个选项定义和说明之间要有两个空格，比如：

```bash
--verbose MORE text.    # 坏, 会被认为是带参数 MORE 的选项
                        # --version 和 MORE text. 之间应该有2个空格
-q        Quit.         # 好
-o FILE   Output file.  # 好
--stdout  Use stdout.   # 好，2个空格
```

选项描述中在说明中使用 `[default: <default-value>]` 来给带参数的选项赋以默认值，比如：

```bash
--coefficient=K  The K coefficient [default: 2.95]
--output=FILE    Output file [default: test.txt]
--directory=DIR  Some directory [default: ./]
```

## 三、小节

关于 `docopt` 的方方面面我们都了解的差不多了，回过头来看，对于命令行元信息的定义，它比 `argparse` 要来的更加简洁。
`argparse` 像是命令式编程，调用一个个的函数逐步将命令行元信息定义清楚；而 `docopt` 则像是声明式编程，通过声明定义命令行元信息。
两者站在的维度不同，编程的套路也不尽相同，甚是有趣。

了解了这么多，也该练练手了。在下篇文章中，我们仍然会以 `git` 命令作为实战项目，看看如何使用 `docopt` 来实现 `git` 命令。
