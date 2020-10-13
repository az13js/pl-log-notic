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