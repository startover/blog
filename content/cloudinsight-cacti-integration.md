Title: Cloudinsight Agent 与 Cacti 集成
Date: 2016-05-13 18:00
Category: 系统监控
Tags: Cloudinsight, Cacti
Slug: cloudinsight-cacti-integration
Authors: startover

## 原理介绍

Cloudinsight Agent 通过 [python-rrdtool](https://pypi.python.org/pypi/python-rrdtool) 读取 Cacti 生成的 rrd 文件（在 cacti 根目录的 rra 文件夹下），并将其中的数据解析后上传至 [Cloudinsight](http://cloudinsight.oneapm.com/) 进行可视化。

## Cacti 安装配置

由于 Cacti 安装配置较为繁琐，这里通过 Docker 容器的方式来解决这个问题。

然而，Cloudinsight Agent 需要读取 Cacti 生成的 rrd 文件，所以我们需要将这部分文件挂载到系统主机上。

* 创建挂载文件

```
$ sudo mkdir -p /var/lib/cacti/rra
$ sudo wget -O /etc/mysql/mysqld.cnf https://raw.githubusercontent.com/cloudinsight/cloudinsight-docker-cacti/master/mysqld.cnf
```

* 挂载文件权限设置

由于挂载文件默认是root用户访问权限，需将其赋予容器内的 www-data 用户，如下：

```
$ sudo chown -R 33:33 /var/lib/cacti
```

* 运行 Cacti 容器

```
$ docker run -d --name docker-cacti \
             -h docker-cacti \
             -p 80 \
             -v /etc/mysql/mysqld.cnf:/etc/mysql/mysql.conf.d/mysqld.cnf \
             -v /var/lib/cacti/rra:/var/lib/cacti/rra \
             -v /etc/localtime:/etc/localtime:ro \
             quantumobject/docker-cacti
```

## Cloudinsight Agent 集成

* [安装](http://cloud.oneapm.com/#/settings) Cloudinsight Agent

* 配置 MySQL 访问权限

```
$ docker exec docker-cacti mysql -e "create user 'oneapm'@'%' identified by 'oneapm';" -uroot -pmysqlpsswd
$ docker exec docker-cacti mysql -e "grant select on cacti.* to 'oneapm'@'%';" -uroot -pmysqlpsswd
```

* 安装 RRDTool 依赖包

由于 Cacti 运行在 docker 容器内，为确保 [python-rrdtool](https://pypi.python.org/pypi/python-rrdtool) 能够正常运行，需要在本机安装相关依赖。

Debian/Ubuntu
```
sudo apt-get install rrdtool
```

CentOS/Redhat
```
sudo yum -y install rrdtool*
```

* 配置 Cacti 监控

```
$ docker inspect --format '{{ .NetworkSettings.IPAddress }}' docker-cacti
172.17.0.2
$ cd /etc/cloudinsight-agent/conf.d
$ sudo cp cacti.yaml.example cacti.yaml
$ sudo vi cacti.yaml
init_config:

instances:
  - mysql_host: 172.17.0.2  # 这里是容器的IP地址，可通过上面的命令获取
    mysql_user: oneapm
    mysql_password: oneapm
    rrd_path: /var/lib/cacti/rra
```

* 重启 Cloudinsight Agent

```
$ sudo /etc/init.d/cloudinsight-agent restart
```

相关链接：
[https://github.com/QuantumObject/docker-cacti](https://github.com/QuantumObject/docker-cacti)
