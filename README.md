# pl-log-notic

**开发中**

允许定期从日志中获取信息，然后自由匹配特定模式的文本，并提取其中的一些内容，发出通知的通用系统。

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

    cd pladmin
    python3 manage.py createsuperuser

## 运作原理

程序每隔一段时间就从数据库中取出下一次执行时间小于或等于当前时间的任务（这意味着这些任务达到或者超过了期望被执行的时间，却还没有被执行），然后执行它们，并根据它们的间隔时间算好下次执行的时间，然后保存修改到数据库。

任务的执行过程是：对每个从数据库中取出的任务，传递给每个流水线进行处理。假如某个流水线正好需要对这个任务执行实际操作，那么该流水线就把任务交给特定的控制器进行具体的处理，假如流水线不需要处理该任务那么直接不处理这个任务。可以认为不同的流水线针对不同的目标对任务进行筛选，把自己关注的任务派发给特定的控制器进行处理。

不同的控制器具有不同的功能。控制器在被执行的时候根据需要调用不同的收集器取得原始数据，再使用特定的解析器解析出不同的变量，根据需要组装特定的结构传给信使。

最后由信使渲染出推送的消息内容，将消息推送给特定的终端。

*应该对不同的需要定时主动取数据推送数据的场合都适用。*
