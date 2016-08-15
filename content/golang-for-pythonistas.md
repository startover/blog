Title: Python 程序员的 Golang 学习指南（I）: Go 之初体验
Date: 2016-08-15 12:00
Category: Golang
Tags: Golang, Python
Slug: golang-for-pythonistas
Authors: startover

## Go 语言简介

Go，又称 golang，是 Google 开发的一种静态强类型，编译型，并发型，并具有垃圾回收功能的编程语言。

Go 语言于2009年11月正式宣布推出，自2012年发布1.0，最新稳定版1.6。目前，Go的相关工具和生态已逐渐趋于完善，也不乏重量级项目，如 Docker, Kubernetes, Etcd, InfluxDB 等。

## Go 语言能解决什么样的问题

同绝大多数通用型编程语言相比，Go 语言更多的是为了解决我们在构建大型服务器软件过程中所遇到的软件工程方面的问题而设计的。乍看上去，这么讲可能会让人感觉 Go 非常无趣且工业化，但实际上，在设计过程中就着重于清晰和简洁，以及较高的可组合性，最后得到的反而会是一门使用起来效率高而且很有趣的编程语言，很多程序员都会发现，它有极强的表达力而且功能非常强大。

总结为以下几点：

* 清晰的依赖关系
* 清晰的语法
* 清晰的语义
* 偏向组合而不是继承
* 编程模型（垃圾回收、并发）所代理的简单性
* 易于为它编写工具（Easy tooling ）(gotool、gofmt、godoc、gofix)

建议有兴趣的同学看看 [Go在谷歌：以软件工程为目的的语言设计](http://www.oschina.net/translate/go-at-google-language-design-in-the-service-of-software-engineering)。

## Go 语言相对 Python 有哪些优势

这里引用一段[知乎](https://www.zhihu.com/question/21409296)上某大牛的回答，如下：

* **部署简单**。Go 编译生成的是一个静态可执行文件，除了 glibc 外没有其他外部依赖。这让部署变得异常方便：目标机器上只需要一个基础的系统和必要的管理、监控工具，完全不需要操心应用所需的各种包、库的依赖关系，大大减轻了维护的负担。这和 Python 有着巨大的区别。由于历史的原因，Python 的部署工具生态相当混乱【比如 setuptools, distutils, pip, buildout 的不同适用场合以及兼容性问题】。官方 PyPI 源又经常出问题，需要搭建私有镜像，而维护这个镜像又要花费不少时间和精力。
* **并发性好**。Goroutine 和 channel 使得编写高并发的服务端软件变得相当容易，很多情况下完全不需要考虑锁机制以及由此带来的各种问题。单个 Go 应用也能有效的利用多个 CPU 核，并行执行的性能好。这和 Python 也是天壤之比。多线程和多进程的服务端程序编写起来并不简单，而且由于全局锁 GIL 的原因，多线程的 Python 程序并不能有效利用多核，只能用多进程的方式部署；如果用标准库里的 multiprocessing 包又会对监控和管理造成不少的挑战【我们用的 supervisor 管理进程，对 fork 支持不好】。部署 Python 应用的时候通常是每个 CPU 核部署一个应用，这会造成不少资源的浪费，比如假设某个 Python 应用启动后需要占用 100MB 内存，而服务器有 32 个 CPU 核，那么留一个核给系统、运行 31 个应用副本就要浪费 3GB 的内存资源。
* **良好的语言设计**。从学术的角度讲 Go 语言其实非常平庸，不支持许多高级的语言特性；但从工程的角度讲，Go 的设计是非常优秀的：规范足够简单灵活，有其他语言基础的程序员都能迅速上手。更重要的是 Go 自带完善的工具链，大大提高了团队协作的一致性。比如 gofmt 自动排版 Go 代码，很大程度上杜绝了不同人写的代码排版风格不一致的问题。把编辑器配置成在编辑存档的时候自动运行 gofmt，这样在编写代码的时候可以随意摆放位置，存档的时候自动变成正确排版的代码。此外还有 gofix, govet 等非常有用的工具。
* **执行性能好**。虽然不如 C 和 Java，但通常比原生 Python 应用还是高一个数量级的，适合编写一些瓶颈业务。内存占用也非常省。

从个人对 Golang 的初步使用来说，体验还是相当不错的，但是也有下面几点需要注意：

* 驼峰式命名风格（依据首字母大小写来决定其是否能被其他包引用），但我更喜欢 Python 的小写字母加下划线命名风格。
* 没有好用的包管理器，Golang 官方也没有推荐最佳的包管理方案，目前公认的比较好用的有 Godeps, Govendor及Glide，而 Python 的包管理器 pip 已形成自己的一套标准。
* 多行字符串的变量声明需要用反引号（`），Python 里是三个双引号（"""），参考[http://stackoverflow.com/questions/7933460/how-do-you-write-multiline-strings-in-go](http://stackoverflow.com/questions/7933460/how-do-you-write-multiline-strings-in-go)
* Golang 中的类型匹配是很严格的，不同的类型之间通常需要手动转换，所以在字符串拼接时往往需要对整型进行显式转换，如 `fmt.Println("num: " + strconv.Itoa(1))`
* Golang 语言语法里的语法糖并不多，如在 Python 中很流行的 map, reduce, range 等，在 Golang 里都没有得到支持。

另外，推荐阅读 [Golang 新手开发者要注意的陷阱和常见错误](http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/)。

## 学习资料推荐

建议先把 Go 的[官方文档](https://golang.org/doc/)过一遍，主要有以下几项：

* [A Tour of Go](https://tour.golang.org/welcome/1)
* [How to write Go code](https://golang.org/doc/code.html)
* [Effective Go](https://golang.org/doc/effective_go.html)
* [Language Specification](https://golang.org/ref/spec)

官方文档看完后，基本也算入门了，这时候可以看看 [Go 的示例代码](https://gobyexample.com/)，或者去 [Project Euler](https://projecteuler.net/) 刷刷题。

当然也可以去知乎看看大牛们都是如何学习的，链接 [https://www.zhihu.com/question/23486344](https://www.zhihu.com/question/23486344)。

## 总结

虽然 Go 有很多被诟病的地方，比如 GC 和对错误的处理方式，但没有任何语言是完美的，从实用角度来讲，Go 有不输于 Python 的开发效率，完善的第三方工具，以及强大的社区支持，这些就足够了。



参考链接：  
[https://golang.org/doc/](https://golang.org/doc/)  
[https://talks.golang.org/2012/splash.article](https://talks.golang.org/2012/splash.article)  
[https://www.zhihu.com/question/21409296](https://www.zhihu.com/question/21409296)  
[https://www.zhihu.com/question/23486344](https://www.zhihu.com/question/23486344)  
[http://stackoverflow.com/questions/7933460/how-do-you-write-multiline-strings-in-go](http://stackoverflow.com/questions/7933460/how-do-you-write-multiline-strings-in-go)  
[http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/](http://devs.cloudimmunity.com/gotchas-and-common-mistakes-in-go-golang/)  
[http://www.oschina.net/translate/go-at-google-language-design-in-the-service-of-software-engineering](http://www.oschina.net/translate/go-at-google-language-design-in-the-service-of-software-engineering)
