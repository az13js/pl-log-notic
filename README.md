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

### 初始化数据库的表

    cd pladmin
    python3 manage.py migrate

默认情况下使用的是`sqlite3`本地数据库，数据库文件位于`pladmin/db.sqlite3`。

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

示例：

    $ cd pladmin
    $ WORKER_NAME=local-worker-01 HOST=pl-log-notic.az13js.cn IP=127.0.0.1 PORT=9210 CACHETIME=1m python3 manage.py export_worker

该命令需要使用一些手段防止因为程序异常退出。在单机模式下，导出的文件会保存到`pladmin/pltplconf/static`文件夹，可以在页面上下载。在以多个Worker作为集群部署的时候，如果部署在不同的服务器上那么可能无法下载到导出的文件。这种情况下请参考`pladmin/export_floder_process_script.py`脚本编写一个上传到专门的文件服务的命令，然后修改配置文件里面的`EXPORT_FLODER_PROCESS_COMMAND`参数。Worker进程会在导出ES数据完成的时候，将数据所在的文件夹作为第一个参数传给`EXPORT_FLODER_PROCESS_COMMAND`配置的命令，然后把命令输出的内容作为下载的链接通过Web服务保存起来，然后在页面被用户看到。
