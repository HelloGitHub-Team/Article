# 聊聊 Python 的单元测试框架（二）：nose 和它的继任者 nose2

## 一、nose

[nose](https://nose.readthedocs.io/en/latest/) 是一个第三方单元测试框架，它**完全兼容 `unittest`**，并且号称是一个更好用的测试框架。

那么 `nose` 除了具备 `unittest` 的所有功能外，还具有哪些优势呢？

### 1.1 用例编写

用例的编写方式除了编写继承于 [unittest.TestCase](https://docs.python.org/3/library/unittest.html#unittest.TestCase) 的测试类外，还可以编写成**没有继承的测试类**。比如，写成如下形式也会被 `nose` 视作一个测试类：

```python
from nose.tools import raises

class TestStringMethods:

    def test_upper(self):
        assert 'foo'.upper() == 'FOO'

    def test_isupper(self):
        assert 'FOO'.isupper()
        assert not 'Foo'.isupper()

    @raises(TypeError)
    def test_split(self):
        s = 'hello world'
        assert s.split() == ['hello', 'world']
        # check that s.split fails when the separator is not a string
        s.split(2)
```

当然，测试类并没有继承 `unittest.TestCase`，将不能使用其内置的各类 `assertXXX` 方法，进而导致用例出错时无法获得更加详细的上下文信息。

此外，`nose` 也支持**定义函数**来作为测试，这给许多简单的测试场景带来很大的便利：

```python
def test_upper():
    assert 'foo'.upper() == 'FOO'
```

### 1.2 用例发现和执行

`unittest` 所支持的用例发现和执行能力，`nose` 均支持。
`nose` 支持用例自动（递归）发现：

- 默认发现当前目录下所有包含 `test` 的测试用例，但不包括以 `_` 开头的用例
  - 使用 `nosetests` 命令
- 通过 `-w` 参数指定要自动发现的目录， `-m` 参数指定用例文件、目录、函数、类的名称模式（正则匹配）
  - `nosetests -w project_directory "test_.+"`

`nose` 也支持执行指定用例：

- 指定测试模块
  - `nosetests test.module`
- 指定测试类
  - `nosetests a.test:TestCase`
- 指定测试方法
  - `nosetests another.test:TestCase.test_method`
- 指定测试文件路径
  - `nosetests /path/to/test/file.py`
- 指定测试文件路径+测试类或测试函数（这是 `unittest` 所不支持的）
  - `nosetests /path/to/test/file.py:TestCase`
  - `nosetests /path/to/test/file.py:TestCase.test_method`
  - `nosetests /path/to/test/file.py:test_function`

### 1.3 测试夹具（Fixtures）

`nose` 除了支持 `unittest` 所支持的定义测试前置和清理方式，还支持一种更为简单的定义方式：

```python
def setup_func():
    "set up test fixtures"

def teardown_func():
    "tear down test fixtures"

@with_setup(setup_func, teardown_func)
def test():
    "test ..."
```

只需定义两个函数用来表示前置和清理方法，通过 [nose.tools.with_setup](https://nose.readthedocs.io/en/latest/testing_tools.html?highlight=with_setup#nose.tools.with_setup) 装饰器装饰测试函数，`nose` 便会在执行测试用例前后分别执行所定义的前置和清理函数。

### 1.4 子测试/测试生成器

`nose` 除了支持 `unittest` 中的 `TestCase.subTest`，还支持一种更为强大的子测试编写方式，也就是 `测试生成器（Test generators）`，通过 `yield` 实现。

在下面的示例中，定义一个 `test_evens` 测试函数，里面生成了 5 个子测试 `check_even`：

```python
def test_evens():
    for i in range(0, 5):
        yield check_even, i, i*3

def check_even(n, nn):
    assert n % 2 == 0 or nn % 2 == 0
```

此外，相较于 `unittest.TestCase.subTest` 多个子测试只能执行一次测试前置和清理，`nose` 的 `测试生成器` 可以支持每个子测试执行一次测试前置和清理，如：

```python
def test_generator():
    # ...
    yield func, arg, arg # ...

@with_setup(setup_func, teardown_func)
def func(arg):
    assert something_about(arg)
```

### 1.5 插件体系

`nose` 相较于 `unittest` 一个最大的优势就是插件体系，自带了很多有用的插件，也有丰富的第三方插件。这样就能做更多的事情。

其中，自带插件如下：

- [AllModules](https://nose.readthedocs.io/en/latest/plugins/allmodules.html)：在所有模块中收集用例
- [Attrib](https://nose.readthedocs.io/en/latest/plugins/attrib.html)：给用例打标签，并可运行含指定标签的用例
- [Capture](https://nose.readthedocs.io/en/latest/plugins/capture.html)：捕获用例的标准输出
- [Collect](https://nose.readthedocs.io/en/latest/plugins/collect.html)：快速收集用例
- [Cover](https://nose.readthedocs.io/en/latest/plugins/cover.html)：统计代码覆盖率
- [Debug](https://nose.readthedocs.io/en/latest/plugins/debug.html)：用例失败时进入 pdb 调试
- [Deprecated](https://nose.readthedocs.io/en/latest/plugins/deprecated.html)：标记用例为弃用
- [Doctests](https://nose.readthedocs.io/en/latest/plugins/deprecated.html)：运行文档用例
- [Failure Detail](https://nose.readthedocs.io/en/latest/plugins/failuredetail.html)：断言失败时提供上下文信息
- [Isolate](https://nose.readthedocs.io/en/latest/plugins/isolate.html)：保护用例避免受一些副作用的影响
- [Logcapture](https://nose.readthedocs.io/en/latest/plugins/logcapture.html)：捕捉 logging 输出
- [Multiprocess](https://nose.readthedocs.io/en/latest/plugins/multiprocess.html)：并行执行用例
- [Prof](https://nose.readthedocs.io/en/latest/plugins/prof.html)：使用热点分析器进行分析
- [Skip](https://nose.readthedocs.io/en/latest/plugins/skip.html)：标记用例为跳过
- [Testid](https://nose.readthedocs.io/en/latest/plugins/testid.html)：为输出的每个用例名称添加测试 ID
- [Xunit](https://nose.readthedocs.io/en/latest/plugins/xunit.html)：以 xunit 格式输出测试结果

而第三方库则多种多样，如用来生成 HTML 格式测试报告的 [nose-htmloutput](https://github.com/ionelmc/nose-htmloutput) 等，这里不再一一列出。

得益于 `nose` 丰富的插件生态，当 `nose` 本身不能够完全满足我们的测试需求时，可以通过安装插件，并在 `nosetests` 命令行指定该插件所提供的特定参数即可非常容易的使用插件。
相较于 `unittest`，就能省去很多自己开发额外测试逻辑的精力。

## 二、nose2

[nose2](https://github.com/nose-devs/nose2) 是 [nose](https://nose.readthedocs.io/en/latest/) 的继任者。
它们的理念都是让编写和运行测试用例变得更容易。

它们有很多相同点，比如都兼容 `unittest`，支持使用函数作为测试用例，支持子测试，拥有插件体系。但也有很多不同点，下面列出一些主要的不同点：

- 发现和载入测试
  - `nose` 自行实现了模块加载功能，使用惰性方式加载测试模块，加载一个执行一个。
  - `nose2` 则借助内建的 [**import**()](https://docs.python.org/3/library/functions.html#__import__) 导入模块，并且是先全部载入，再执行用例
  - `nose2` 并不支持 `nose` 所支持的所有测试用例项目结构，比如如下用例文件的结构在 `nose2` 中就不受支持：

```bash
.
`-- tests
    |-- more_tests
    |   `-- test.py
    `-- test.py
```

- 测试前置和清理函数级别
  - `nose` 支持方法、类、模块和包级别的测试前置和清理函数
  - `nose2` 则不支持包级别的测试前置和清理函数
- 子测试
  - `nose2` 除了支持使用测试生成器来实现子测试外，还支持使用[参数化测试（Parameterized tests）](https://docs.nose2.io/en/latest/params.html#parameterized-tests)来实现子测试
  - `nose2` 除了像 `nose` 一样支持在测试函数和测试类（不继承于 `unittest.TestCase`）中支持参数化测试和测试生成器外，还支持在继承于 `unittest.TestCase` 的测试类中使用
- 配置化
  - `nose` 期望所有插件的配置通过命令行参数进行配置
  - `nose2` 则通过配置文件进行控制，以最小化命令行参数让人读得更舒服

更多对比详见 [官方文档](https://docs.nose2.io/en/latest/differences.html)。

## 三、小结

`nose` 和 `nose2` 在做到兼容 `unittest` 上就足以看出它们的目标，那便是要吸引原来那些使用 `unittest` 的用户来使用它们。它们确实做到了！

`nose` 和 `nose2` 在用例编写、测试夹具、子测试上做出改进，已经能让日常用例编写工作变得更加容易和灵活。同时又引入插件体系，进一步将单元测试框架的能力提升了一个大大的台阶，这让很多在基础测试功能之上的高阶功能的实现和共享成为了可能。也难怪有众多开发者对它们情有独钟。
