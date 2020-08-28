# pl-log-notic

**开发中**

允许定期从日志中获取信息，然后自由匹配特定模式的文本，并提取其中的一些内容，发出通知的通用系统。

## 前端页面构建

### 安装构建环境

    npm install

注：速度慢可以更换淘宝的源

    npm config set registry https://registry.npm.taobao.org

### 构建页面

    cd webpage
    npm run build

## 服务环境部署

### 安装依赖

注：`pl-log-notic`是在`Python 3.8`环境下开发的。

    pip install -r requirements.txt

如果安装缓慢可以尝试换个镜像，比如

    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

### 运行服务器

    cd pladmin
    python3 manage.py runserver 9210

注：`9210`是 web 服务的监听端口号，可以自定义这个端口号，应用不依赖特定端口。

### 查看页面

浏览器访问`http://127.0.0.1:9210/`。




