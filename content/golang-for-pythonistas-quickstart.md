Title: Python 程序员的 Golang 学习指南（III）: 入门篇
Date: 2016-08-30 13:44
Category: Golang
Tags: Golang, Python
Slug: golang-for-pythonistas-quickstart
Authors: startover

## 基础语法

#### 类型和关键字

* 类型

```
// 基础类型
布尔类型: bool
整型: int8，uint8，int16，uint16，int32，uint32，int64，uint64，int，rune，byte，complex128， complex64，其中，byte 是 int8 的别名
浮点类型: float32 、 float64
复数类型: complex64 、 complex128
字符串: string
字符类型: rune（int32的别名）
错误类型: error

// 复合类型
指针（pointer）
数组（array）
切片（slice）
字典（map）
通道（chan）
结构体（struct）
接口（interface）
```

* 关键字

```
break        default      func         interface    select
case         defer        go           map          struct
chan         else         goto         package      switch
const        fallthrough  if           range        type
continue     for          import       return       var

```

#### 变量

Go 同其他语言不同的地方在于变量的类型在变量名的后面，不是 `int a`，而是 `a int`。至于为什么这么定义，Go 的[官方博客](https://blog.golang.org/gos-declaration-syntax)有给出解释，有兴趣的可以参考下。

变量定义语法如下：

```go
var a int
a = 2

// 或者
a := 2

// 同时定义多个变量
var (
    a int
    b bool
)

// 同时给多个变量赋值
a, b := 2, true
```

#### 操作符

```
+    &     +=    &=     &&    ==    !=    (    )
-    |     -=    |=     ||    <     <=    [    ]
*    ^     *=    ^=     <-    >     >=    {    }
/    <<    /=    <<=    ++    =     :=    ,    ;
%    >>    %=    >>=    --    !     ...   .    :
     &^          &^=

```

#### 控制结构

Go 语言支持如下的几种流程控制语句:

* 条件语句，对应的关键字为 if、else 和 else if；
* 选择语句，对应的关键字为 switch、case 和 select；
* 循环语句，对应的关键字为 for 和 range；
* 跳转语句，对应的关键字为 goto。

值得一提的是，Go 语言并不支持 do 或者 while 关键字，而是对 for 关键字做了增强，以实现类似的效果，如下：

```go
for {
    // 实现无限循环，慎用！
}
```

#### 常用内置函数

* len：计算（字符串，数组或者切片，map）长度
* cap：计算（数组或者切片，map）容量
* close：关闭通道
* append：追加内容到切片
* copy：拷贝数组/切片内容到另一个数组/切片
* delete：用于删除 map 的元素

#### array, slice 和 map

```go
// array
a := [3]int{ 1, 2, 3 } // 等价于 a := [...]int{ 1, 2, 3 }

// slice
s := make([]int , 3) // 创建一个长度为 3 的 slice
s := append(s, 1) // 向 slice 追加元素
s := append(s, 2)

// map
m := make(map[string]int) // 使用前必须先初始化
m["golang"] = 7
```

关于 array, slice 和 map 的更多惯用法，有一篇[文章](https://se77en.cc/2014/06/30/array-slice-map-and-set-in-golang/)介绍的挺详细，有兴趣的可以看看。

#### 函数

Go 语言的函数有如下特性：

* 不定参数

由于 Go 语言不支持函数重载（具体原因见 [Go Language FAQ](https://golang.org/doc/faq#overloading)），但我们可以通过不定参数实现类似的效果。

```go
func myfunc(args ...int) {
    // TODO
}

// 可通过如下方式调用
myfunc(2)
myfunc(1, 3, 5)
```

* 多返回值

与 C、C++ 和 Java 等开发语言的一个极大不同在于，Go 语言的函数或者成员的方法可以有多
个返回值，这个特性能够使我们写出比其他语言更优雅、更简洁的代码。

```go
func (file *File) Read(b []byte) (n int, err error)

// 我们可以通过下划线（_）来忽略某个返回值
n, _ := f.Read(buf)
```

* 匿名函数

匿名函数是指不需要定义函数名的一种函数实现方式，它并不是一个新概念，最早可以回溯
到 1958 年的 Lisp 语言。但是由于各种原因，C 和 C++ 一直都没有对匿名函数给以支持，其他的各
种语言，比如 JavaScript、C# 和 Objective-C 等语言都提供了匿名函数特性，当然也包含Go语言。

匿名函数由一个不带函数名的函数声明和函数体组成，如下：

```go
func(a, b int) bool {
    return a < b
}
```

匿名函数可以直接赋值给一个变量或者直接执行：

```go
f := func(a, b int) bool {
    return a < b
}

func(a, b int) bool {
    return a < b
}(3, 4) // 花括号后直接跟参数列表表示函数调用
```

* 闭包

闭包是可以包含自由(未绑定到特定对象)变量的代码块，这些变量不在这个代码块内或者
任何全局上下文中定义，而是在定义代码块的环境中定义。要执行的代码块(由于自由变量包含
在代码块中，所以这些自由变量以及它们引用的对象没有被释放)为自由变量提供绑定的计算环
境(作用域)。

Go 的匿名函数就是一个闭包。我们来看一个例子：

```go
package main

import "fmt"

func main() {
    j := 5
    a := func() func() {
        i := 10
        return func() {
            fmt.Printf("i, j: %d, %d\n", i, j)
        }
    }()
    a()
    j *= 2
    a()
}
```

程序输出如下：

```
i, j: 10, 5
i, j: 10, 10
```

#### 错误处理

Go 语言追求简洁优雅，所以，Go 语言不支持传统的 `try...catch...finally` 这种异常，因为 Go 语言的设计者们认为，将异常与控制结构混在一起会很容易使得代码变得混乱。因为开发者很容易滥用异常，甚至一个小小的错误都抛出一个异常。在 Go 语言中，使用多值返回来返回错误。不要用异常代替错误，更不要用来控制流程。在极个别的情况下，也就是说，遇到真正的异常的情况下（比如除数为0了），才使用 Go 中引入的Exception处理：defer, panic, recover。

用法如下：

```go
package main

import "fmt"

func main() {
    defer func() {
        fmt.Println("recovered:", recover())
    }()
    panic("not good")
}
```

关于 Go 语言的错误处理机制和传统的 `try...catch...finally` 异常机制孰优孰劣，属于仁者见仁，智者见智，这里不做赘速。有兴趣的同学可以去看看知乎上的讨论：[Go 语言的错误处理机制是一个优秀的设计吗？](https://www.zhihu.com/question/27158146)。


## 面向对象 -> 一切皆类型

Python 推崇“一切皆对象”，而在 Go 语言中，类型才是一等公民。

我们可以这样定义一个结构体：

```go
type Name struct {
    First  string
    Middle string
    Last   string
}
```

同样也可以定义基础类型：

```go
type SimpleName string
```

还能给任意类型定义方法：

```go
func (s SimpleName) String() string { return string(s) }
// 或者
func (s string) NoWay()
```


## Golang VS Python

最后我们通过几个例子来比较一下 Golang 与 Python 的一些基本用法，如下：

#### 生成器（Generator）

* Python 版本

```python
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
        yield a

for x in fib(10):
    print x

print 'done'
```

* Golang 版本

```go
package main

import "fmt"

func fib(n int) chan int {
    c := make(chan int)
    go func() {
        a, b := 0, 1
        for i := 0; i < n; i++ {
            a, b = b, a+b
            c <- a
        }
        close(c)
    }()
    return c
}

func main() {
    for x := range fib(10) {
        fmt.Println(x)
    }
}
```

#### 装饰器（Decorator）

* Python 版本

```python
from urlparse import urlparse, parse_qs
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

def auth_required(myfunc):
    def checkuser(self):
        user = parse_qs(urlparse(self.path).query).get('user')
        if user:
            self.user = user[0]
            myfunc(self)
        else:
            self.wfile.write('unknown user')
    return checkuser

class myHandler(BaseHTTPRequestHandler):
    @auth_required
    def do_GET(self):
        self.wfile.write('Hello, %s!' % self.user)

if __name__ == '__main__':
    try:
        server = HTTPServer(('localhost', 8080), myHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
```

* Golang 版本

```go
package main

import (
    "fmt"
    "net/http"
)

var hiHandler = authRequired(
    func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hi, %v", r.FormValue("user"))
    },
)

func authRequired(f http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        if r.FormValue("user") == "" {
            http.Error(w, "unknown user", http.StatusForbidden)
            return
        }
        f(w, r)
    }
}

func main() {
    http.HandleFunc("/hi", hiHandler)
    http.ListenAndServe(":8080", nil)
}
```

#### 猴子补丁（Monkey patching）

* Python 版本

```python
import urllib

def say_hi(usr):
    if auth(usr):
        print 'Hi, %s' % usr
    else:
        print 'unknown user %s' % usr

def auth(usr):
    try:
        auth_url = 'localhost'
        r = urllib.urlopen(auth_url + '/' + usr)
        return r.getcode() == 200
    except:
        return False

def sayhitest():
    # Test authenticated user
    globals()['auth'] = lambda x: True
    say_hi('John')

    # Test unauthenticated user
    globals()['auth'] = lambda x: False
    say_hi('John')

if __name__ == '__main__':
    sayhitest()
```

* Golang 版本

```go
package main

import (
    "fmt"
    "net/http"
)

func sayHi(user string) {
    if !auth(user) {
        fmt.Printf("unknown user %v\n", user)
        return
    }
    fmt.Printf("Hi, %v\n", user)
}

var auth = func(user string) bool {
    authURL := "localhost"
    res, err := http.Get(authURL + "/" + user)
    return err == nil && res.StatusCode == http.StatusOK
}

func testSayHi() {
    auth = func(string) bool { return true }
    sayHi("John")

    auth = func(string) bool { return false }
    sayHi("John")
}

func main() {
    testSayHi()
}
```


相关链接：  
[https://blog.golang.org/gos-declaration-syntax](https://blog.golang.org/gos-declaration-syntax)  
[https://se77en.cc/2014/06/30/array-slice-map-and-set-in-golang/](https://se77en.cc/2014/06/30/array-slice-map-and-set-in-golang/)  
[https://golang.org/doc/faq#overloading](https://golang.org/doc/faq#overloading)  
[https://www.zhihu.com/question/27158146](https://www.zhihu.com/question/27158146)  
[https://talks.golang.org/2013/go4python.slide](https://talks.golang.org/2013/go4python.slide)  
