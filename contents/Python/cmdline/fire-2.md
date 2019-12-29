# Python 命令行之旅：深入 fire（一）

## 一、前言

在第一篇“初探 fire”的文章中，我们初步掌握了使用 `fire` 的简单步骤，了解了它 Pythonic 的用法。

今天我们将深入了解 `fire` 的子命令、嵌套命令和属性访问功能。

```
本系列文章默认使用 Python 3 作为解释器进行讲解。
若你仍在使用 Python 2，请注意两者之间语法和库的使用差异哦~
```

## 二、功能

### 2.1 子命令

使用 `fire` 实现子命令有多种方式：

#### 2.1.1 定义若干函数，使用 fire.Fire()

实现子命令最简单的方式就是定义若干个函数，每个函数名隐式就是子命令名称，然后调用 `fire.Fire()` 变将当前模块所有的函数解析为对应的子命令的处理函数。

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire()
```

然后我们就可以在命令行中这么调用：

```bash
$ python example.py add 10 20
30
$ python example.py multiply 10 20
200
```

关于如何识别参数类型，比如上述 `add 10 20` 中 `10` 和 `20` 是作为数字而非字符串，我们会在下篇文章的参数解析章节中进行讲解。

#### 2.1.2 定义若干函数，使用 fire.Fire(<dict>)

在 `2.1.1` 的版本中，会把所有函数都当做是子命令。有时我们可能只想把部分函数当做子命令，或者是希望子命令名称和函数名称不一样。这个时候我们就可以通过字典对象显式地告诉 `fire`。

字典对象的形式为 `{'子命令名称': 函数}`，比如前面的示例中，我们希望最终的子命令为 `add` 和 `mul`，那么就可以这么写：

```python
fire.Fire({
  'add': add,
  'mul': multiply,
})
```

然后我们就可以在命令行中这么调用：

```bash
$ python example.py add 10 20
30
$ python example.py mul 10 20
200
```

#### 2.1.3 定义类和方法，使用 fire.Fire(<object>)

定义类和方法的这种方式我们在上一篇文章中介绍过，它和定义函数的方式基本相同，只不过是用类的方式来组织。

然后将类实例化，并把实例化的对象多为 `fire.Fire` 的入参：

```python
import fire

class Calculator(object):

  def add(self, x, y):
    return x + y

  def multiply(self, x, y):
    return x * y

if __name__ == '__main__':
  calculator = Calculator()
  fire.Fire(calculator)
```

#### 2.1.4 定义类和方法，使用 fire.Fire(<class>)

和 `2.1.3` 中的唯一不同点是把类而非实例对象作为 `fire.Fire` 的入参：

```python
fire.Fire(Calculator)
```

传递类和实例对象的基本作用是一样的，但传递类还有一个额外的特性：如果构造函数中定义了参数，那么这些参数都会作为整个命令行程序的选项参数。

```python
import fire

class BrokenCalculator(object):

  def __init__(self, offset=1):
      self._offset = offset

  def add(self, x, y):
    return x + y + self._offset

  def multiply(self, x, y):
    return x * y + self._offset

if __name__ == '__main__':
  fire.Fire(BrokenCalculator)
```

查看帮助命令有：

```bash
$ python example.py --help
INFO: Showing help with the command 'example.py -- --help'.

NAME
    example.py

SYNOPSIS
    example.py <flags>

FLAGS
    --offset=OFFSET
```

由此可见构造函数 `BrokenCalculator.__init__(self, offset=1)` 中的 `offset` 自动转换为了命令行中的全局选项参数 `--offset`，且默认值为 `1`。

我们可以在命令行中这么调用：

```bash
$ python example.py add 10 20
31
$ python example.py multiply 10 20
201
$ python example.py add 10 20 --offset=0
30
$ python example.py multiply 10 20 --offset=0
200
```

### 2.2 命令组/嵌套命令

想要实现嵌套命令，可将多个类组织起来，示例如下：

```python
class IngestionStage(object):

  def run(self):
    return 'Ingesting! Nom nom nom...'

class DigestionStage(object):

  def run(self, volume=1):
    return ' '.join(['Burp!'] * volume)

  def status(self):
    return 'Satiated.'

class Pipeline(object):

  def __init__(self):
    self.ingestion = IngestionStage()
    self.digestion = DigestionStage()

  def run(self):
    self.ingestion.run()
    self.digestion.run()

if __name__ == '__main__':
  fire.Fire(Pipeline)
```

在上面的示例中：

- `IngestionStage` 实现了子命令 `run`
- `DigestionStage` 实现了子命令 `run` 和 `status`
- `Pipeline` 的构造函数中将 `IngestionStage` 实例化为 `ingestion`，将 `DigestionStage` 实例化为 `digestion`，就将这两个放到一个命令组中，因而支持了：
  - `ingestion run`
  - `digestion run`
  - `digestion status`
- `Pipeline` 实现了子命令 `run`

因此整个命令行程序支持如下命令：

- `run`
- `ingestion run`
- `digestion run`
- `digestion status`

然后我们就可以在命令行中这么调用：

```bash
$ python example.py run
Ingesting! Nom nom nom...
Burp!
$ python example.py ingestion run
Ingesting! Nom nom nom...
$ python example.py digestion run
Burp!
$ python example.py digestion status
Satiated.
```

### 2.3 属性访问

`属性访问` 是 `fire` 相对于其他命令行库来说一个比较独特的功能。所谓访问属性是获取预置的属性所对应的值。

举个例子，在命令行中指定 `--code` 来告知程序要查询的程序编码，然后希望通过 `zipcode` 属性返回邮编，通过 `city` 属性返回城市名。那么属性可实现为实例成员属性：

```python
import fire

cities = {
  'hz': (310000, '杭州'),
  'bj': (100000, '北京'),
}


class City(object):

  def __init__(self, code):
    info = cities.get(code)
    self.zipcode = info[0] if info else None
    self.city = info[1] if info else None

if __name__ == '__main__':
  fire.Fire(City)
```

使用方式如下：

```bash
$ python example.py --code bj zipcode
100000
$ python example.py --code hz city
杭州
```

## 三、小结

使用 `fire` 实现子命令和嵌套命令相对于其他命令行库来说都更加简单清晰，不仅如此，`fire` 还提供了属性访问这种较为独特的能力。

在下篇文章中，我们将进一步深入了解 `fire`，介绍其链式函数调用、自定义序列化、参数解析、fire 选项等更加高阶的功能。
