Title: Python 程序员的 Golang 学习指南（V）: 测试篇
Date: 2016-09-14 21:10
Category: Golang
Tags: Golang, Python
Slug: golang-for-pythonistas-testing
Authors: startover

这篇文章我们介绍下 Go 语言中如何进行测试。

## 单元测试

* 功能测试

Go 语言内置测试框架，其通过 `testing` 包以及 `go test` 命令来提供测试功能。

但编写测试代码需**遵循以下原则**：

> 1. 文件名必须是 `_test.go` 结尾的，这样在执行 `go test` 的时候才会执行到相应的代码。
> 2. 你必须 import `testing` 这个包。
> 3. 所有的测试用例函数必须是 `Test` 开头。
> 4. 测试用例会按照源代码中写的顺序依次执行。
> 5. 测试函数 `TestXxx()` 的参数是 `testing.T`，我们可以使用该类型来记录错误或者是测试状态。
> 6. 测试格式：`func TestXxx (t *testing.T)`, `Xxx` 部分可以为任意的字母数字的组合，但是首字母不能是小写字母 [a-z] ，例如 `Testintdiv` 是错误的函数名。
> 7. 函数中通过调用 `testing.T` 的 `Error`, `Errorf`, `FailNow`, `Fatal`, `FatalIf` 方法，说明测试不通过，调用 `Log` 方法用来记录测试的信息。

假设我们现在需要测试 `stringutil.go`，内容如下：

```go
// Package stringutil contains utility functions for working with strings.
package stringutil

// Reverse returns its argument string reversed rune-wise left to right.
func Reverse(s string) string {
    r := []rune(s)
    for i, j := 0, len(r)-1; i < len(r)/2; i, j = i+1, j-1 {
        r[i], r[j] = r[j], r[i]
    }
    return string(r)
}
```

那我们的测试用例可以写成下面这样：

```go
package stringutil

import "testing"

func TestReverse(t *testing.T) {
    const in, want = "Hello, world", "dlrow ,olleH"
    got := Reverse(in)
    if got != want {
        t.Errorf("Reverse(%q) == %q, want %q", in, got, want)
    }
}
```

执行 `go test -v`，得到如下输出：

```
=== RUN   TestReverse
--- PASS: TestReverse (0.00s)
PASS
ok      github.com/startover/testing    0.001s
```

* 基准测试

基准测试与功能测试类似，不过有以下几点需要注意：

> 1. 基准测试用例必须遵循如下格式：`func BenchmarkXXX(b *testing.B) { ... }`，其中 XXX 可以是任意字母数字的组合，但是首字母不能是小写字母。
> 2. go test不会默认执行基准测试的函数，如果要执行基准测试需要带上参数 `-test.bench`，语法：`-test.bench="test_name_regex"`，例如 `go test -test.bench=".*"` 表示测试全部的基准测试函数。
> 3. 在基准测试用例中，请记得在循环体内使用 `testing.B.N`，以使测试可以正常的运行。
> 4. 文件名也必须以 `_test.go` 结尾。

代码示例如下：

```go
package stringutil
 
import "testing"
 
func BenchmarkReverse(b *testing.B) {
    const in = "Hello, world"
    for n := 0; n < b.N; n++ {
        Reverse(in)
    }
}
```

执行 `go test -v -test.bench=".*"`，得到如下输出：

```
PASS
BenchmarkReverse-4   5000000           260 ns/op
ok      github.com/startover/testing    1.579s
```

* 表驱动测试

编写测试代码时，一个较好的办法是把测试的输入数据和期望的结果写在一起组成一个数据表：表中的每条记录都是一个含有输入和期望值的完整测试用例，有时还可以结合像测试名字这样的额外信息来让测试输出更多的信息。这就是**表驱动测试**。

Go 语言的 struct 字面值语法让我们可以轻松写出表驱动测试，代码示例如下：

```go
package stringutil

import "testing"

func TestTableReverse(t *testing.T) {
    for _, c := range []struct {
        in, want string
    }{
        {"Hello, world", "dlrow ,olleH"},
        {"Hello, 世界", "界世 ,olleH"},
        {"", ""},
    } {
        got := Reverse(c.in)
        if got != c.want {
            t.Errorf("Reverse(%q) == %q, want %q", c.in, got, c.want)
        }
    }
}
```

* 测试覆盖率

执行 `go test -v -cover` 可以得到代码覆盖率的统计信息，如下：

```
$ go test -v -cover
=== RUN   TestReverse
--- PASS: TestReverse (0.00s)
=== RUN   TestTableReverse
--- PASS: TestTableReverse (0.00s)
PASS
coverage: 100.0% of statements
ok      github.com/startover/testing    0.004s

```

此外，`go test` 还可以将代码覆盖率的统计信息保存到某个文件中，这个文件可以被 `cover` 工具解析。

```
$ go test -coverprofile=cover.out
$ go tool cover -func=cover.out
github.com/startover/testing/stringutil.go:5:   Reverse     100.0%
total:                          (statements)    100.0%
```

## BDD 测试

Go 语言比较主流的 BDD 测试框架主要有：[GoConvey](https://github.com/smartystreets/goconvey) 和 [Ginkgo](https://github.com/onsi/ginkgo)。下面让我们感受下 BDD 风格的测试代码：

* [GoConvey](https://github.com/smartystreets/goconvey)

```go
package stringutil

import (
    "testing"

    . "github.com/smartystreets/goconvey/convey"
)

func TestSpec(t *testing.T) {

    // Only pass t into top-level Convey calls
    Convey("Given some ASCII and UTF8 strings", t, func() {
        const in, want = "Hello, world", "dlrow ,olleH"
        Convey("The value should be equal the reversed one", func() {
            got := Reverse(in)
            So(got, ShouldEqual, want)
        })
    })
}
```

* [Ginkgo](https://github.com/onsi/ginkgo) & [Gomega](https://github.com/onsi/gomega)

```go
package stringutil

import (
    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
)

var _ = Describe("StringutilTest", func() {
    var in, want string

    BeforeEach(func() {
        const in, want = "Hello, world", "dlrow ,olleH"
    })

    Describe("With ASCII and UTF8 strings defined", func() {
        Context("Reverse the give strings", func() {
            It("should be reversed", func() {
                got := Reverse(in)
                Expect(got).To(Equal(want))
            })
        })
    })
})
```

这里需要特别注意的是，运行 Ginkgo 风格的测试代码需要执行 `ginkgo -r`，而不是 `go test`。

完整的代码示例见：[https://github.com/startover/testing](https://github.com/startover/testing)


相关链接：  
[https://talks.golang.org/2014/testing.slide#1](https://talks.golang.org/2014/testing.slide#1)  
[https://nathany.com/go-testing-toolbox/](https://nathany.com/go-testing-toolbox/)  
[http://codethoughts.info/go/2015/04/05/how-to-test-go-code/](http://codethoughts.info/go/2015/04/05/how-to-test-go-code/)  
[https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/11.3.md](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/11.3.md)
