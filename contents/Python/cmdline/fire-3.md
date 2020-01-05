# Python 命令行之旅：深入 fire（二）

## 一、前言

在上一篇文章中我们介绍了 `fire` 的子命令、嵌套命令和属性访问等内容，今天我们将继续深入了解 `fire` 的其他功能。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、功能

### 2.1 最简命令实现

在上一节中，我们介绍了只要定义一个函数就可以实现命令行程序。比如：

```python
import fire

def english():
  return 'Hello, fire!'

def chinese():
  return '你好，fire！'

if __name__ == '__main__':
  fire.Fire()
```

但这还不是最简单的实现方式，`fire` 甚至允许你通过定义变量的方式来实现命令行！
上面的例子可以写成下面这种形式：

```python
import fire

english = 'Hello, fire!'
chinese = '你好，fire！'

if __name__ == '__main__':
  fire.Fire()
```

### 2.2 链式调用

在 `Fire CLI` 中，你可以通过链式调用不断地对上一个结果进行处理。

想做到这一点也很简单，就是在实例方法中返回 `self` 即可。

在下面的示例中，我们实现了一个简单的四则运算命令，可链式调用 `add`、`sub`、`mul` 和 `div`。

```python
import fire

class Calculator:

  def __init__(self):
    self.result = 0
    self.express = '0'

  def __str__(self):
    return f'{self.express} = {self.result}'

  def add(self, x):
    self.result += x
    self.express = f'{self.express}+{x}'
    return self

  def sub(self, x):
    self.result -= x
    self.express = f'{self.express}-{x}'
    return self

  def mul(self, x):
    self.result *= x
    self.express = f'({self.express})*{x}'
    return self

  def div(self, x):
    self.result /= x
    self.express = f'({self.express})/{x}'
    return self

if __name__ == '__main__':
  fire.Fire(Calculator)
```

上述代码中的 `add`、`sub`、`mul`、`div` 分别对应加、减、乘、除的逻辑，每个方法都接受 `x` 参数作为参与运算的数字，返回值均为 `self`，这样就可以无限次地链式调用。在命令行中链式调用结束后，会最终调用到 `__str__` 方法将结果打印出来。

其中，`__str__` 在 `fire` 中用来完成自定义序列化。如果不提供这个方法，在链式调用完成后将会打印帮助内容。

比如，我们可以这么调用：

```bash
$ python calculator.py add 1 sub 2 mul 3 div 4
((+1-2)*3)/4 = -0.75

$ python calculator.py add 1 sub 2 mul 3 div 4 add 4 sub 3 mul 2 div 1
((((0+1-2)*3)/4+4-3)*2)/1 = 0.5
```

### 2.3 位置参数和选项参数

通过前面的介绍我们也都清楚了在 `fire` 中不必显式的定义位置参数或选项参数。

通过下面的例子，我们将细化两类参数的使用：

```python
import fire

class Building(object):

  def __init__(self, name, stories=1):
    self.name = name
    self.stories = stories

  def __str__(self):
    return f'name: {self.name}, stories: {self.stories}'

  def climb_stairs(self, stairs_per_story=10):
    yield self.name
    for story in range(self.stories):
      for stair in range(1, stairs_per_story):
        yield stair
      yield 'Phew!'
    yield 'Done!'

if __name__ == '__main__':
  fire.Fire(Building)
```

- 构造函数中定义的参数（如 `name` 和 `stories`）在命令行中仅为选项参数（如 `--name` 和 `--stories`）。我们可以这么调用：

```bash
$ python example.py --name="Sherrerd Hall" --stories=3
```

- 构造函数中定义的参数可在命令中放于任意位置。比如下面两个调用都是可以的：

```bash
$ python example.py --name="Sherrerd Hall" climb-stairs --stairs-per-story 10
$ python example.py climb-stairs --stairs-per-story 10 --name="Sherrerd Hall"
```

- 构造函数和普通方法中定义的默认参数（如 `stories`），在命令行中是可选的。我们可以这么调用：

```bash
$ python example.py --name="Sherrerd Hall"
```

- 普通方法中定义的参数（如 `stairs_per_story`）在命令行中即可以是位置参数，也可以是选项参数。我们可以这么调用：

```bash
# 作为位置参数
$ python example.py --name="Sherrerd Hall" climb_stairs 10
# 作为选项参数
$ python example.py --name="Sherrerd Hall" climb_stairs --stairs_per_story=10
```

- 选项参数中的横杠（`-`）和下划线（`_`）是等价的。因此也可以这么调用：

```bash
# 作为选项参数
$ python example.py --name="Sherrerd Hall" climb_stairs --stairs-per-story=10
```

此外，`fire` 还支持在函数中定义 `*args` 和 `**kwargs`。

```python
import fire

def fargs(*args):
  return str(args)


def fkwargs(**kwargs):
  return str(kwargs)

if __name__ == '__main__':
  fire.Fire()
```

- 函数中的 `*args` 在命令行中为位置参数。我们可以这么调用：

```bash
$ python example.py fargs a b c
```

- 函数中的 `**kwargs` 在命令行中为选项参数。我们可以这么调用：

```bash
$ python example.py fargs --a a1 --b b1 --c c1
```

- 通过分隔符 `-` 可显式告知分隔符后的为子命令，而非命令的参数。且看下面的示例：

```bash
# 没有使用分隔符，upper 被作为位置参数
$ python example.py fargs a b c upper
('a', 'b', 'c', 'upper')

# 使用了分隔符，upper 被作为子命令
$ python example.py fargs a b c - upper
('A', 'B', 'C')
```

- 通过 `fire` 内置的 `--separator` 可以自定义分隔符，此选项参数需要跟在单独的 `--` 后面：

```bash
$ python example.py a b c X upper -- --separator=X
('A', 'B', 'C')
```

### 2.4 参数类型

在 `fire` 中，参数的类型由其值决定，通过下面的简单代码，我们可以看到给不同的值时，`fire`会解析为什么类型：

```python
import fire
fire.Fire(lambda obj: type(obj).__name__)
```

```bash
$ python example.py 10
int
$ python example.py 10.0
float
$ python example.py hello
str
$ python example.py '(1,2)'
tuple
$ python example.py [1,2]
list
$ python example.py True
bool
$ python example.py {name: David}
dict
```

如果想传递字符串形式的数字，那就需要小心引号了，要么把引号引起来，要么转义引号：

```bash
# 数字 10
$ python example.py 10
int
# 没有对引号处理，仍然是数字10
$ python example.py "10"
int
# 把引号引起来，所以是字符串“10”
$ python example.py '"10"'
str
# 另一种把引号引起来的形式
$ python example.py "'10'"
str
# 转义引号
$ python example.py \"10\"
str
```

考虑下更复杂的场景，如果传递的是字典，在字典中有字符串，那么也是要小心引号的：

```bash
# 推荐做法
$ python example.py '{"name": "David Bieber"}'
dict
# 也是可以的
$ python example.py {"name":'"David Bieber"'}
dict
# 错误，会被解析为字符串
$ python example.py {"name":"David Bieber"}
str
# 错误，不会作为单个参数（因为中间有空格），报错
$ python example.py {"name": "David Bieber"}
<error>
```

如果值为 `True` 或 `False` 将为视为布尔值，`fire` 还支持通过 `--name` 将 `name` 设为 `True`，或通过 `--noname` 将 `name` 设为 `False`：

```bash
$ python example.py --obj=True
bool
$ python example.py --obj=False
bool
$ python example.py --obj
bool
$ python example.py --noobj
bool
```

### 2.5 Fire 内置选项参数

Fire 内置了一些选项参数，以帮助我们更容易地使用命令行程序。若想使用内置的选项功能，需要将选项参数跟在 `--` 后，在上文中，我们介绍了 `--separator` 参数，除了它，`fire` 还支持以下选项参数：

- `command -- --help` 列出详细的帮助信息
- `command -- --interactive` 进入交互式模式
- `command -- --completion [shell]` 生成 CLI 程序的自动补全脚本，以支持自动补全
- `command -- --trace` 获取命令的 Fire 追踪以了解调用 Fire 后究竟发生了什么
- `command -- --verbose` 获取包含私有成员在内的详情

## 三、小结

`fire` 让命令行程序的实现变得特别简单，本文着重介绍了它的链式调用、选项参数、位置参数、参数类型以及内置选项参数。`fire` 的概念并不多，真正践行了“把简单留给他人，把复杂留给自己”的理念。

`fire` 的介绍就告一段落，它绝对会是你编写命令行程序的一大利器。在下一篇文章中，我们依然会通过实现一个简单的 `git` 程序来进行 `fire` 的实战。
