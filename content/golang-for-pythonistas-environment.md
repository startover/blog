Title: Python 程序员的 Golang 学习指南（II）: 开发环境搭建
Date: 2016-08-22 16:10
Category: Golang
Tags: Golang, Python
Slug: golang-for-pythonistas-environment
Authors: startover

[上一篇文章](http://startover.github.io/articles/2016/08/15/golang-for-pythonistas/)我们已经对 Golang 有了初步的了解，这篇主要介绍如何在 Ubuntu 14.04 上搭建 Golang 开发环境。

## 安装 Golang

这里就按照[官方文档](https://golang.org/doc/install#install)进行安装即可，如下：

* 下载并解压安装包到指定目录

```
$ wget https://storage.googleapis.com/golang/go1.6.3.linux-amd64.tar.gz
$ tar -C /usr/local -xzf go1.6.3.linux-amd64.tar.gz
```

* 设置 PATH

```
$ echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
$ source ~/.bashrc
```

* 验证安装

```
$ go version
go version go1.6.3 linux/amd64
```

## 环境变量设置

```
$ echo "export GOROOT=/usr/local/go" >> ~/.bashrc
$ echo "export GOPATH=$HOME/go" >> ~/.bashrc
$ source ~/.bashrc
```

其中，GOROOT 为 Golang 的安装目录，只有当 Golang 安装到除 /usr/local 之外的路径时需要设置，反之则不用设置，GOPATH 是 Golang 的开发目录，详细可参考[官方文档](https://golang.org/cmd/go/#hdr-GOPATH_environment_variable)。

## 开发工具

工欲善其事，必先利其器，作为一名伪 VIMer，这里主要介绍下如何在 Vim 下配置 Golang 开发环境。

由于之前一直使用 [k-vim](https://github.com/wklken/k-vim) 作为 Python 开发环境，而 [k-vim](https://github.com/wklken/k-vim) 已经集成了当前使用最为广泛的用于搭建 Golang 开发环境的 vim 插件 [vim-go](https://github.com/fatih/vim-go)，只是默认没有开启，需要我们手动进行相关设置。 

在 [k-vim](https://github.com/wklken/k-vim) 中开启 Golang 语言的支持，非常简单，如下：

* 修改 ~/.vimrc.bundles（开启 golang 支持，并修改 vim-go 的默认配置，增加快捷键配置等）。

```bash
let g:bundle_groups=['python', 'javascript', 'markdown', 'html', 'css', 'tmux', 'beta', 'json', 'golang']

" vimgo {{{
    let g:go_highlight_functions = 1
    let g:go_highlight_methods = 1
    let g:go_highlight_structs = 1
    let g:go_highlight_operators = 1
    let g:go_highlight_build_constraints = 1
 
    let g:go_fmt_fail_silently = 1
    let g:go_fmt_command = "goimports"
    let g:syntastic_go_checkers = ['golint', 'govet', 'errcheck']
 
    " vim-go custom mappings
    au FileType go nmap <Leader>s <Plug>(go-implements)
    au FileType go nmap <Leader>i <Plug>(go-info)
    au FileType go nmap <Leader>gd <Plug>(go-doc)
    au FileType go nmap <Leader>gv <Plug>(go-doc-vertical)
    au FileType go nmap <leader>r <Plug>(go-run)
    au FileType go nmap <leader>b <Plug>(go-build)
    au FileType go nmap <leader>t <Plug>(go-test)
    au FileType go nmap <leader>c <Plug>(go-coverage)
    au FileType go nmap <Leader>ds <Plug>(go-def-split)
    au FileType go nmap <Leader>dv <Plug>(go-def-vertical)
    au FileType go nmap <Leader>dt <Plug>(go-def-tab)
    au FileType go nmap <Leader>e <Plug>(go-rename)
    au FileType go nnoremap <leader>gr :GoRun %<CR>
" }}}
```

* 在 Vim 内执行 `:PlugInstall`，安装 [vim-go](https://github.com/fatih/vim-go)。

* 在 Vim 内执行 `:GoInstallBinaries`，下载并安装 [vim-go](https://github.com/fatih/vim-go) 依赖的二进制工具，`goimports`，`golint` 等。

* 安装 [gotags](https://github.com/jstemmer/gotags)，使 `tagbar` 配置生效。

```
$ go get -u github.com/jstemmer/gotags
```

我们来看一下最终效果：

![Image of Golang Environment in Vim]({filename}/images/golang-for-pythonistas-environment.png)


## 编写第一个程序

进入工作目录，新建文件 `hello.go`，如下：

```
$ cd $GOPATH
$ vim hello.go
package main
 
import "fmt"
 
func main() {
    fmt.Println("Hello, World！")
}
```

运行程序：

```
$ go run hello.go
Hello, World！
```
