# pl-log-notic

这是一个通过读取 Elasticsearch 中收集的错误日志，发送消息到企业微信来实现生产系统错误提醒的预警系统。下面介绍如何安装部署。

## 安装构建静态文件所需的模块，以及构建静态文件

安装构建所需的模块

    cd webpage
    npm install

注：速度慢可以更换淘宝的源

    cd webpage
    npm config set registry https://registry.npm.taobao.org
    npm install

然后构建页面

    npm run build

构建出来的静态文件位于`webpage/public/`目录下，手动拷贝它们到`pladmin/pltplconf/templates/pltplconf/`，然后把`index.html`进行模板标签替换，最后把静态文件移动到`pladmin/pltplconf/static`。

## 使用`Makefile`构建

你可能想使用`Makefile`，因为这样就不需要每次执行构建、手动拷贝再替换标签了：

    make clean && make

## 服务环境部署

### 安装依赖

注：`pl-log-notic`是在`Python 3.8`环境下开发的。

    pip install -r requirements.txt

如果安装缓慢可以尝试换个镜像，比如

    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

#### 关于依赖项和安装的包的位置相关问题

特殊情况下，可能需要把包安装在特定的位置，这时通过指定`--target`选项来实现，例如指定当前目录下的`package`目录：

    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --target=package

也可以相对路径或者绝对路径：

    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --target=./my_package
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --target=/tmp/my_package

启动`python`命令时就需要指定一个环境变量，`PYTHONPATH`，如：

    PYTHONPATH=package python

这时模块路径就能包含当前目录的`package`目录：

    $ PYTHONPATH=package python
    Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
    [GCC 9.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import sys
    >>> sys.path
    ['', '/home/az13js/pl-log-notic/package', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/home/az13js/.local/lib/python3.8/site-packages', '/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages']

### 初始化数据库的表

    cd pladmin
    python3 manage.py migrate

默认情况下使用的是`sqlite3`本地数据库，数据库文件位于`pladmin/db.sqlite3`。

#### 使用MySQL？

如果使用MySQL需要进行一些调整。

一，调整配置文件，默认配置文件位于`pladmin/pladmin/settings.py`，除非自定义修改了配置文件路径。

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # 数据库引擎
            'NAME': 'test_001', # 数据库名
            'USER': 'root', # 账号
            'PASSWORD': 'PASSWORD', # 密码
            'HOST': '127.0.0.1', # HOST
            'POST': 3306, # 端口
            'CONN_MAX_AGE': 60 # 数据库连接维持时间
        }
    }

二，修改代码，在`pladmin/pltplconf/__init__.py`，导入plmysql并设置：

    import pymysql
    pymysql.install_as_MySQLdb()

### 启动定时任务

    cd pladmin
    python3 manage.py scheduler

注：这命令不会自己转后台，最好配置`supervisor`去监控。如果使用`sqlite3`的话可能出现数据库锁定导致操作错误，这种情况它会自己尝试继续运行，并发低的时候问题不大。

### 运行服务器

    cd pladmin
    python3 manage.py runserver 9210

注：`9210`是 web 服务的监听端口号，可以自定义这个端口号，应用不依赖特定端口。

### 查看页面

浏览器访问`http://127.0.0.1:9210/`。

### 创建超级用户

服务器端使用的是`Django`框架，如果你打算使用框架内置的后台，那你可能想创建超级用户。

    cd pladmin
    python3 manage.py createsuperuser

按照提示填写用户信息和密码就行了。

## 启动ES数据导出的节点

这个系统支持根据自定义的规则从ES中按照时间段导出全部数据。原理是采用Worker节点从Web服务中查询出导出的任务，领取后在节点上执行数据导出的工作。Worker可以运行多个，通过不同的Worker名称来区分。启动Worker需要按照下面的方式通过环境变量配置：

- `WORKER_NAME`节点名，必填，保证每个进程有不同的节点名
- `HOST`通过HTTP访问时的主机名称，只通过IP就能访问的话可以随便写，此参数是必填的
- `IP`WEB服务的IP地址，如果IP地址是可以动态改变的话，那么可以不设置此参数
- `PORT`WEB服务端口，默认80，可以不填写
- `CACHETIME`游标缓存时间，默认是1分钟，`1m`
- `USER`HTTP基础认证，用户名，可选
- `PASSWORD`HTTP基础认证，密码，可选

示例：

    $ cd pladmin
    $ WORKER_NAME=local-worker-01 HOST=pl-log-notic.az13js.cn IP=127.0.0.1 PORT=9210 CACHETIME=1m python3 manage.py export_worker

该命令需要使用一些手段防止因为程序异常退出。在单机模式下，导出的文件会保存到`pladmin/pltplconf/static`文件夹，可以在页面上下载。在以多个Worker作为集群部署的时候，如果部署在不同的服务器上那么可能无法下载到导出的文件。这种情况下请参考`pladmin/export_floder_process_script.py`脚本编写一个上传到专门的文件服务的命令，然后修改配置文件里面的`EXPORT_FLODER_PROCESS_COMMAND`参数。Worker进程会在导出ES数据完成的时候，将数据所在的文件夹作为第一个参数传给`EXPORT_FLODER_PROCESS_COMMAND`配置的命令，然后把命令输出的内容作为下载的链接通过Web服务保存起来，然后在页面被用户看到。
