Title: Python - 装饰器使用过程中的误区
Date: 2015-04-27 14:07
Category: Python
Tags: Python, 装饰器
Slug: python-decorator-mistake
Authors: startover

## **装饰器基本概念**

大家都知道装饰器是一个很著名的设计模式，经常被用于AOP(面向切面编程)的场景，较为经典的有插入日志，性能测试，事务处理，Web权限校验，Cache等。

Python语言本身提供了装饰器语法（@），典型的装饰器实现如下：

```python
@function_wrapper
def function():
    pass
```

@实际上是python2.4才提出的语法糖，针对python2.4以前的版本有另一种等价的实现：

```python
def function():
    pass

function = function_wrapper(function)
```

## **装饰器的两种实现**

**函数包装器 - 经典实现**

```python
def function_wrapper(wrapped):
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

@function_wrapper
def function():
    pass
```

**类包装器 - 更易于理解**

```python
class function_wrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped
    def __call__(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

@function_wrapper
def function():
    pass
```

## **函数（function）自省**

当我们谈到一个函数时，通常希望这个函数的属性像其文档上描述的那样，是被明确定义的，例如`__name__`和`__doc__` 。

针对某个函数应用装饰器时，这个函数的属性就会发生变化，但这并不是我们所期望的。

```python
def function_wrapper(wrapped):
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

@function_wrapper
def function():
    pass

>>> print(function.__name__)
_wrapper
```

python标准库提供了`functools.wraps()`，来解决这个问题。

```python
import functools

def function_wrapper(wrapped):
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
    return _wrapper

@function_wrapper
def function():
    pass

>>> print(function.__name__)
function
```

然而，当我们想要获取被包装函数的参数（`argument`）或源代码（`source code`）时，同样不能得到我们想要的结果。

```python
import inspect

def function_wrapper(wrapped): ...

@function_wrapper
def function(arg1, arg2): pass

>>> print(inspect.getargspec(function))
ArgSpec(args=[], varargs='args', keywords='kwargs', defaults=None)

>>> print(inspect.getsource(function))
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        return wrapped(*args, **kwargs)
```

## **包装类方法（`@classmethod`）**

当包装器（`@function_wrapper`）被应用于`@classmethod`时，将会抛出如下异常：

```python
class Class(object):
    @function_wrapper
    @classmethod
    def cmethod(cls):
        pass

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in Class
  File "<stdin>", line 2, in wrapper
  File ".../functools.py", line 33, in update_wrapper
    setattr(wrapper, attr, getattr(wrapped, attr))
AttributeError: 'classmethod' object has no attribute '__module__'
```

因为`@classmethod`在实现时，缺少`functools.update_wrapper`需要的某些属性。这是`functools.update_wrapper`在python2中的bug，3.2版本已被修复，参考[http://bugs.python.org/issue3445](http://bugs.python.org/issue3445)。

然而，在python3下执行，另一个问题出现了：

```python
class Class(object):
    @function_wrapper
    @classmethod
    def cmethod(cls):
        pass

>>> Class.cmethod()
Traceback (most recent call last):
  File "classmethod.py", line 15, in <module>
    Class.cmethod()
  File "classmethod.py", line 6, in _wrapper
    return wrapped(*args, **kwargs)
TypeError: 'classmethod' object is not callable
```

这是因为包装器认定被包装的函数（`@classmethod`）是可以直接被调用的，但事实并不一定是这样的。被包装的函数实际上可能是描述符（`descriptor`），意味着为了使其可调用，该函数（描述符）必须被正确地绑定到某个实例上。关于描述符的定义，可以参考[https://docs.python.org/2/howto/descriptor.html](https://docs.python.org/2/howto/descriptor.html)。

## **总结 - 简单并不意味着正确**

尽管大家实现装饰器所用的方法通常都很简单，但这并不意味着它们一定是正确的并且始终能正常工作。

如同上面我们所看到的，`functools.wraps()`可以帮我们解决`__name__`和`__doc__` 的问题，但对于获取函数的参数（`argument`）或源代码（`source code`）则束手无策。

以上问题，[wrapt](https://github.com/GrahamDumpleton/wrapt)都可以帮忙解决，详细用法可参考其官方文档：[http://wrapt.readthedocs.org](http://wrapt.readthedocs.org)
