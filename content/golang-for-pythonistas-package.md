Title: Python 程序员的 Golang 学习指南（IV）: 包管理篇
Date: 2016-09-07 10:24
Category: Golang
Tags: Golang, Python
Slug: golang-for-pythonistas-package
Authors: startover

在[第一篇文章](http://startover.github.io/articles/2016/08/15/golang-for-pythonistas/)我们有提到，Golang 官方并没有推荐最佳的包管理方案，对于像我这样习惯了 Python 包管理的开发者，自然还是希望有像 pip 一样好用的工具，帮助我们进行依赖管理，下面就让我们对 Golang 的包管理机制一探究竟。

## Golang 包管理机制

Go 语言的包管理系统是去中心化的，我们可以通过 `go get` 命令获取存放在远程仓库的代码协议。实际上，`go get` 支持以下 VCS 协议：

| 名称       | 主命令 | 说明                                                                                                                                                             |
|------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mercurial  | hg     | Mercurial是一种轻量级分布式版本控制系统，采用Python语言实现，易于学习和使用，扩展性强。                                                                          |
| Git        | git    | Git最开始是Linux Torvalds为了帮助管理 Linux 内核开发而开发的一个开源的分布式版本控制软件。但现在已被广泛使用。它是被用来进行有效、高速的各种规模项目的版本管理。 |
| Subversion | svn    | Subversion是一个版本控制系统，也是第一个将分支概念和功能纳入到版本控制模型的系统。但相对于Git和Mercurial而言，它只算是传统版本控制系统的一员。                   |
| Bazaar     | bzr    | Bazaar是一个开源的分布式版本控制系统。但相比而言，用它来作为VCS的项目并不多。                                                                                    |

比如，我们现在需要获取 godep 这个项目，可以执行如下命令：

```
$ go get github.com/tools/godep
```

需要指出的是，`go get` 实际上执行了两个步骤：1. 下载源码包；2. 执行 `go install`，如果只下载不安装，则需要指定 `-d` 参数，如下：

```
$ go get -d github.com/tools/godep
```

除了 `go get`，Go 语言还提供了一个 `Workspace` 的机制，即通过设定 GOPATH 环境变量，指定除了 GOROOT 所指定的目录之外，Go 代码所在的位置(也就是 `Workspace` 的位置)。 一般来说，GOPATH 目录下会包含 pkg、src 和 bin 三个子目录，这三个目录各有用处。

* bin 目录用于放置编译好的可执行文件，为了使得这里的可执行文件可以方便的运行， 可在 shell 中设置 PATH 环境变量。
* src 目录用于放置代码源文件，在进行 import 时，是使用这个位置作为根目录的。自己编写的代码也应该放在这下面。
* pkg 用来放置安装的包的链接对象(Object)的。这个概念有点类似于链接库，Go 会将编译出的可连接库放在这里， 方便编译时链接。不同的系统和处理器架构的对象会在 pkg 存放在不同的文件夹中。

## Golang 包管理现状

显然，通过 `go get` 和 `Workspace` 的方式并不足以解决项目依赖和版本依赖的问题，主要有以下几点：

1. 第三方包的版本控制。如果没有明确指定依赖的第三方包的版本，团队开发很容易导入不一样的版本，导致项目无法正常运行。
2. 第三方包没有内容安全审计，很容易引入代码 Bug，这是泛中心化包管理普遍存在的问题。
3. 依赖的完整性无法校验，程序编译时无法保障百分百成功。

因此，我们必须借助第三方工具来解决这些问题。

## 第三方解决方案

这里我从[官方推荐包管理工具](https://github.com/golang/go/wiki/PackageManagementTools)中挑选了几个比较常用的工具：Godep, Govendor 以及 Glide，作下简单介绍。

#### [Godep](https://github.com/tools/godep)

* godep save

这个命令做了以下几件事：

> 1. 查找项目中所用到的所有的第三方包。
> 2. 在项目目录下创建 Godeps 目录，Godeps/Godeps.json 是依赖文件，包括了 go 的版本，用到的第三方包的引入路径，版本号等信息，json 文件需要一并加入到版本控制里。
> 3. 所有依赖的第三方包的代码会被拷贝到 vendor/ 下，并且移除了 .git 这样的版本控制信息。

* godep restore

当下载别人发布的项目时，如果下载的项目中只有 Godeps.json 文件，而没有包含第三方包，则可以使用 `godep restore` 这个命令将所有的依赖包下载到 `$GOPATH` 目录下，而不用一个一个去 `go get`，还是很方便的。

#### [Govendor](https://github.com/kardianos/govendor)

* govendor init

执行 `govendor init` 会在根目录下生成一个 vendor 文件夹，以及 vendor/vendor.json，其中 vendor.json 类似 godep 工具中的描述文件版本的功能。

* govendor add +external

执行 `govendor add +external` 会将所有依赖的第三方包的代码拷贝到 vendor 文件夹下，并且移除了 .git 这样的版本控制信息，测试所需依赖以及依赖项目的测试文件。与 `godep save` 的功能类似。

* govendor fetch

执行 `govendor fetch` 新增的第三方包直接被 get 到根目录的 vendor 文件夹下，不会与其它的项目混用第三方包，完美避免了多个项目同用同一个第三方包的不同版本问题。

这样，我们只需对 vendor/vendor.json 进行版本控制，即可对第三包依赖关系进行控制。

#### [Glide](https://github.com/Masterminds/glide)

* glide init

执行 `glide init` 或 `glide create` 会在项目根目录下生成一个 glide.yaml，这个文件用来记录项目用到的第三方包的依赖关系，并支持编辑修改。


* glide install

执行 `glide install`，会把所有依赖的第三方包都下载到 vendor 文件夹下，并且会在 glide.yaml 中添加所有依赖的第三方包名称，以及在 glide.lock 文件中记录具体的版本管理信息。

## 总结

上面我们分别对 Godep, Govendor 以及 Glide 这三种工具做了简单的介绍，对于 Python 开发者，个人还是比较认同 Govendor 的方式，因为其很容易实现类似 Virtualenv 的模式，从而实现不同程序使用不同版本依赖的目的。

当然，如果你是 Node.js 的开发者，可能对于 [Godep](https://github.com/tools/godep) 有更加熟悉的感觉，而对于 Ruby 开发者，[gom](https://github.com/mattn/gom) 会让你感到更加亲切。

因此，针对第三方包管理工具的选择，现阶段还完全交由开发者做裁定，这里就“仁者见仁，智者见智”了。


相关链接：  
[http://www.infoq.com/cn/articles/golang-package-management](http://www.infoq.com/cn/articles/golang-package-management)  
[https://io-meter.com/2014/07/30/go's-package-management/](https://io-meter.com/2014/07/30/go's-package-management/)  
[https://github.com/golang/go/wiki/PackageManagementTools](https://github.com/golang/go/wiki/PackageManagementTools)
