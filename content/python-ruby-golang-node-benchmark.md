Title: Python Flask vs Ruby Sinatra vs Go Martini vs Node Express
Date: 2016-03-15 14:21
Category: Python, Ruby, Go, Node
Tags: Flask, Sinatra, Martini, Express, Performance
Slug: python-ruby-go-node-benchmark
Authors: startover


题外话一：  
最近一段时间，Cloud Insight接连发布了三种语言（Python, Node, Ruby）的SDK，Cloud Insight Agent也迎来了重大突破，发布了Windows监控第一个版本，总算可以松口气写点东西了~

题外话二：  
偶然的机会看到一篇[blog](https://realpython.com/blog/python/python-ruby-and-golang-a-web-Service-application-comparison/)，文中详细的介绍了[Flask](https://github.com/mitsuhiko/flask)(Python), [Sinatra](https://github.com/sinatra/sinatra)(Ruby)以及 [Matini](https://github.com/go-martini/martini)(Golang)这三类微型框架的用法，并提供了各个框架在Docker下的部署方式。然而，美中不足的是没有提供各个框架的性能对比情况，经过一番搜罗，发现了一篇对现今主流框架做性能对比的[文章](https://medium.com/@tschundeee/express-vs-flask-vs-go-acc0879c2122#.vticwh9tn)，找到两者的结合点，于是才有了今天这篇文章~

* * *


回归正题，之所以选择[Flask](https://github.com/mitsuhiko/flask)(Python), [Sinatra](https://github.com/sinatra/sinatra)(Ruby),  [Matini](https://github.com/go-martini/martini)(Golang)和[Express](https://github.com/expressjs/express)(Node)，主要是经验所限以及个人比较喜欢这类微型框架，下面我们就对各个框架在同等条件下的性能表现一探究竟。

本文源码地址：[https://github.com/startover/fibonacci-webapp-benchmark](https://github.com/startover/fibonacci-webapp-benchmark)

## 环境准备：

* #### [Docker](https://www.docker.com/)

    安装文档：[https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)

* #### [ab](https://httpd.apache.org/docs/2.4/programs/ab.html)

    CentOS/Redhat:

    ```
    yum install httpd-tools
    ```

    Ubuntu/Debian:

    ```
    apt-get update && apt-get install apache2-utils
    ```

## 启动容器

```
$ git clone git@github.com:startover/fibonacci-webapp-benchmark.git
$ cd fibonacci-webapp-benchmark
$ ./docker-compose up -d
Recreating fibonacciwebappbenchmark_python_1...
Recreating fibonacciwebappbenchmark_go_1...
Recreating fibonacciwebappbenchmark_ruby_1...
Recreating fibonacciwebappbenchmark_node_1...
$ docker ps
CONTAINER ID        IMAGE                             COMMAND                  CREATED             STATUS              PORTS                    NAMES
14e0d2388dca        fibonacciwebappbenchmark_node     "npm start"              6 seconds ago       Up 5 seconds        0.0.0.0:8080->8080/tcp   fibonacciwebappbenchmark_node_1
8b1bdd070f83        fibonacciwebappbenchmark_ruby     "bundle exec ruby sin"   23 seconds ago      Up 22 seconds       0.0.0.0:4567->4567/tcp   fibonacciwebappbenchmark_ruby_1
333360123b56        fibonacciwebappbenchmark_go       "go run martini.go"      34 seconds ago      Up 32 seconds       0.0.0.0:3000->3000/tcp   fibonacciwebappbenchmark_go_1
df50829f511b        fibonacciwebappbenchmark_python   "python app.py"          42 seconds ago      Up 41 seconds       0.0.0.0:5000->5000/tcp   fibonacciwebappbenchmark_python_1
```

## 性能测试（请求数10w，并发100）

#### Python + Flask

```
$ ab -n 100000 -c 100 http://localhost:5000/10
...
Concurrency Level:      100
Time taken for tests:   168.322 seconds
Complete requests:      100000
Failed requests:        0
Write errors:           0
Total transferred:      18400000 bytes
HTML transferred:       2900000 bytes
Requests per second:    594.10 [#/sec] (mean)
Time per request:       168.322 [ms] (mean)
Time per request:       1.683 [ms] (mean, across all concurrent requests)
Transfer rate:          106.75 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0      12
Processing:    21  168  15.3    166     295
Waiting:       13  167  15.1    165     286
Total:         26  168  15.3    166     295
...
```

#### Ruby + Sinatra

```
$ ab -n 100000 -c 100 http://localhost:4567/10
...
Concurrency Level:      100
Time taken for tests:   496.401 seconds
Complete requests:      100000
Failed requests:        0
Write errors:           0
Total transferred:      30700000 bytes
HTML transferred:       3000000 bytes
Requests per second:    201.45 [#/sec] (mean)
Time per request:       496.401 [ms] (mean)
Time per request:       4.964 [ms] (mean, across all concurrent requests)
Transfer rate:          60.40 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0      14
Processing:   180  493 522.3    412   10507
Waiting:      177  485 521.7    404   10505
Total:        180  493 522.3    412   10507
...
```

#### Go + Martini

```
$ ab -n 100000 -c 100 http://localhost:3000/10
...
Concurrency Level:      100
Time taken for tests:   48.284 seconds
Complete requests:      100000
Failed requests:        0
Write errors:           0
Total transferred:      15700000 bytes
HTML transferred:       4100000 bytes
Requests per second:    2071.08 [#/sec] (mean)
Time per request:       48.284 [ms] (mean)
Time per request:       0.483 [ms] (mean, across all concurrent requests)
Transfer rate:          317.54 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   0.7      1      14
Processing:    13   47  12.0     47     105
Waiting:        3   35  10.4     34      99
Total:         14   48  12.0     48     112
...
```

#### Node + Express

```
$ ab -n 100000 -c 100 http://localhost:8080/10
...
Concurrency Level:      100
Time taken for tests:   59.962 seconds
Complete requests:      100000
Failed requests:        0
Write errors:           0
Total transferred:      20700000 bytes
HTML transferred:       3000000 bytes
Requests per second:    1667.72 [#/sec] (mean)
Time per request:       59.962 [ms] (mean)
Time per request:       0.600 [ms] (mean, across all concurrent requests)
Transfer rate:          337.13 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.5      0      20
Processing:    26   59  11.2     59     168
Waiting:       16   56  10.8     55     168
Total:         26   60  11.1     59     171
...
```

## 总结：


<table class="table table-bordered table-striped table-condensed">
    <tr>
        <td> </td>
        <td>avg(ms) </td>
        <td>min(ms) </td>
        <td>max(ms)</td>
    </tr>
    <tr>
        <td>Flask(Python) </td>
        <td>168 </td>
        <td>26 </td>
        <td>295</td>
    </tr>
    <tr>
        <td>Sinatra(Ruby) </td>
        <td>496 </td>
        <td>180 </td>
        <td>10507</td>
    </tr>
    <tr>
        <td>Martini(Go) </td>
        <td>48 </td>
        <td>14 </td>
        <td>112</td>
    </tr>
    <tr>
        <td>Express(Node) </td>
        <td>60 </td>
        <td>26 </td>
        <td>171</td>
    </tr>
</table>


可见，[Matini](https://github.com/go-martini/martini)(Golang)和[Express](https://github.com/expressjs/express)(Node)性能优势比较明显，也在意料之中，[Flask](https://github.com/mitsuhiko/flask)(Python)表现中规中矩，相较之下，[Sinatra](https://github.com/sinatra/sinatra)(Ruby)的性能简直是没法忍（PS: 我不是Ruby黑）！感兴趣的亲们可以在自己的环境测试下。完。


参考链接：  
[https://realpython.com/blog/python/python-ruby-and-golang-a-web-Service-application-comparison/](https://realpython.com/blog/python/python-ruby-and-golang-a-web-Service-application-comparison)
[https://medium.com/@tschundeee/express-vs-flask-vs-go-acc0879c2122#.6katm1qn2](https://medium.com/@tschundeee/express-vs-flask-vs-go-acc0879c2122#.6katm1qn2)
