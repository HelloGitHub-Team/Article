# 聊聊 Python 的单元测试框架（一）：unittest

## 前言

说到 Python 的单元测试框架，想必接触过 Python 的朋友脑袋里第一个想到的就是 [unittest](https://docs.python.org/3/library/unittest.html)。
的确，作为 Python 的标准库，它很优秀，并被广泛用于各个项目。但你知道吗？其实在 Python 众多项目中，主流的单元测试框架远不止这一个。

本系列文章将为大家介绍目前流行的 Python 的单元测试框架，讲讲它们的功能和特点并比较其异同，以让大家在面对不同场景、不同需求的时候，能够权衡利弊，选择最佳的单元测试框架。

```plaintext
本文默认以 Python 3 为例进行介绍，若某些特性在 Python 2 中没有或不同，会特别说明。
```

## 一、介绍

[unittest](https://docs.python.org/3/library/unittest.html) 单元测试框架最早受到 JUnit 的启发，和其他语言的主流单元测试框架有着相似的风格。

它支持测试自动化，多个测试用例共享前置（setUp）和清理（tearDown）代码，聚合多个测试用例到测试集中，并将测试和报告框架独立。

## 二、用例编写

下面这段简单的示例来自于[官方文档](https://docs.python.org/3/library/unittest.html#basic-example)，用来测试三种字符串方法：`upper`、`isupper`、`split`：

```python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```

上述示例中，通过继承 [unittest.TestCase](https://docs.python.org/3/library/unittest.html#unittest.TestCase) 来创建一个测试用例。
在这个类中，定义以 `test` 开头的方法，测试框架将把它作为独立的测试去执行。

每个用例都采用 `unittest` 内置的断言方法来判断被测对象的行为是否符合预期，比如：

- 在 `test_upper` 测试中，使用 [assertEqual](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual) 检查是否是预期值
- 在 `test_isupper` 测试中，使用 [assertTrue](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertTrue) 或 [assertFalse](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertFalse) 验证是否符合条件
- 在 `test_split` 测试中，使用 [assertRaises](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises) 验证是否抛出一个特定异常

可能有人会好奇，为什么不使用内置断言语句 `assert`，而要额外提供这么多断言方法并使用呢？原因是通过使用 `unittest` 提供的断言方法，测试框架在运行结束后，能够聚合所有的测试结果并产生信息丰富的测试报告。而直接使用 `assert` 虽然也可以达到验证被测对象是否符合预期的目的，但在用例出错时，报错信息不够丰富。

## 三、用例发现和执行

`unittest` 支持用例自动（递归）发现：

- 默认发现当前目录下所有符合 `test*.py` 测试用例
  - 使用 `python -m unittest` 或 `python -m unittest discover`
- 通过 `-s` 参数指定要自动发现的目录， `-p` 参数指定用例文件的名称模式
  - `python -m unittest discover -s project_directory -p "test_*.py"`
- 通过位置参数指定自动发现的目录和用例文件的名称模式
  - `python -m unittest discover project_directory "test_*.py"`

`unittest` 支持执行指定用例：

- 指定测试模块
  - `python -m unittest test_module1 test_module2`
- 指定测试类
  - `python -m unittest test_module.TestClass`
- 指定测试方法
  - `python -m unittest test_module.TestClass.test_method`
- 指定测试文件路径（仅 Python 3）
  - `python -m unittest tests/test_something.py`

## 四、测试夹具（Fixtures）

测试夹具也就是测试前置（setUp）和清理（tearDown）方法。

测试前置方法 [setUp()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) 用来做一些准备工作，比如建立数据库连接。它会在用例执行前被测试框架自动调用。

测试清理方法 [tearDown()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown) 用来做一些清理工作，比如断开数据库连接。它会在用例执行完成（包括失败的情况）后被测试框架自动调用。

测试前置和清理方法可以有不同的执行级别。

### 4.1 生效级别：测试方法

如果我们希望每个测试方法之前前后分别执行测试前置和清理方法，那么需要在测试类中定义好 [setUp()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) 和 [tearDown()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown)：

```python
class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
```

### 4.2 生效级别：测试类

如果我们希望单个测试类中只执行一次前置方法，再执行该测试类中的所有测试，最后执行一次清理方法，那么需要在测试类中定义好 [setUpClass()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUpClass) 和 [tearDownClass()](https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDownClass)：

```python
class MyTestCase(unittest.TestCase):
    def setUpClass(self):
        pass

    def tearDownClass(self):
        pass
```

### 4.3 生效级别：测试模块

如果我们希望单个测试模块中只执行一次前置方法，再执行该模块中所有测试类的所有测试，最后执行一次清理方法，那么需要在测试模块中定义好 [setUpModule()](https://docs.python.org/3/library/unittest.html#setupmodule-and-teardownmodule) 和 [tearDownModule()](https://docs.python.org/3/library/unittest.html#setupmodule-and-teardownmodule)：

```python
def setUpModule():
    pass

def tearDownModule():
    pass
```

## 五、跳过测试和预计失败

`unittest` 支持直接跳过或按条件跳过测试，也支持预计测试失败：

- 通过 [skip](https://docs.python.org/3/library/unittest.html#unittest.skip) 装饰器或 [SkipTest](https://docs.python.org/3/library/unittest.html#unittest.SkipTest) 直接跳过测试
- 通过 [skipIf](https://docs.python.org/3/library/unittest.html#unittest.skipIf) 或 [skipUnless](https://docs.python.org/3/library/unittest.html#unittest.skipUnless) 按条件跳过或不跳过测试
- 通过 [expectedFailure](https://docs.python.org/3/library/unittest.html#unittest.expectedFailure) 预计测试失败

```python
class MyTestCase(unittest.TestCase):

    @unittest.skip("直接跳过")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(mylib.__version__ < (1, 3),
                     "满足条件跳过")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "满足条件不跳过")
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_maybe_skipped(self):
        if not external_resource_available():
            self.skipTest("跳过")
        # test code that depends on the external resource
        pass

    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "这个目前是失败的")
```

## 六、子测试

有时候，你可能想编写这样的测试：在一个测试方法中传入不同的参数来测试同一段逻辑，但它将被视作一个测试，但是如果使用了[子测试](https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests)，就能被视作 N（即为参数的个数）个测试。下面是一个示例：

```python
class NumbersTest(unittest.TestCase):

    def test_even(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

示例中使用了 `with self.subTest(i=i)` 的方式定义子测试，这种情况下，即使单个子测试执行失败，也不会影响后续子测试的执行。这样，我们就能看到输出中有三个子测试不通过：

```bash
======================================================================
FAIL: test_even (__main__.NumbersTest) (i=1)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0

======================================================================
FAIL: test_even (__main__.NumbersTest) (i=5)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "subtests.py", line 32, in test_even
    self.assertEqual(i % 2, 0)
AssertionError: 1 != 0
```

## 六、测试结果输出

基于简单示例小节中提到的例子，来说明下 `unittest` 在运行完测试后的结果输出。

默认情况下的输出非常简单，展示运行了多少个用例，以及所花费的时间：

```bash
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

通过指定 `-v` 参数，可以得到详细输出，除了默认输出的内容，还额外显示了用例名称：

```bash
test_isupper (__main__.TestStringMethods) ... ok
test_split (__main__.TestStringMethods) ... ok
test_upper (__main__.TestStringMethods) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

假定 `test_upper` 测试失败，则在详细输出模式下，结果如下：

```bash
test_isupper (tests.test.TestStringMethods) ... ok
test_split (tests.test.TestStringMethods) ... ok
test_upper (tests.test.TestStringMethods) ... FAIL

======================================================================
FAIL: test_upper (tests.test.TestStringMethods)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Uvsers/prodesire/projects/tests/test.py", line 6, in test_upper
    self.assertEqual('foo'.upper(), 'FOO1')
AssertionError: 'FOO' != 'FOO1'
- FOO
+ FOO1
?    +


----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```

如果我们将 `test_upper` 测试方法中的 `self.assertEqual` 改为 `assert`，则测试结果输出中将会少了对排查错误很有帮助的上下文信息：

```bash
test_isupper (tests.test.TestStringMethods) ... ok
test_split (tests.test.TestStringMethods) ... ok
test_upper (tests.test.TestStringMethods) ... FAIL

======================================================================
FAIL: test_upper (tests.test.TestStringMethods)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/prodesire/projects/tests/test.py", line 6, in test_upper
    assert 'foo'.upper() == 'FOO1'
AssertionError

----------------------------------------------------------------------
Ran 3 tests in 0.001s

FAILED (failures=1)
```

如果想要生成 HTML 格式的报告，那么就需要额外借助第三方库（如 [HtmlTestRunner](https://github.com/oldani/HtmlTestRunner)）来操作。

在安装好第三方库后，你不能直接使用 `python -m unittest` 加上类似 `--html report.html` 的方式来生成 HTML 报告，而是需要自行编写少量代码来运行测试用例进而得到 HTML 报告。
详情请查看 [HtmlTestRunner 使用说明](https://github.com/oldani/HtmlTestRunner#usage)。

## 七、小结

[unittest](https://docs.python.org/3/library/unittest.html) 作为 Python 标准库提供的单元测试框架，使用简单、功能强大，日常测试需求均能得到很好的满足。在不引入第三方库的情况下，是单元测试的不二之选。

在下篇文章中，我们将介绍第三方单元测试框架 `nose` 和 `nose2`，讲讲它对比于 `unittest` 有哪些改进，以至于让很多开发人员优先选择了它。
