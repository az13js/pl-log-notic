# Next：支持后台大量导出ES的数据

用户在页面上填写导出的开始和结束时间，配置导出的模板和导出的内容的分隔符号。然后点击测试导出，可以看到导出的结果（文字方式在页面上呈现）。

如果用户觉得这样导出就可以了，那么点击按钮，提交导出任务。人物提交后是待处理的状态，可能的状态有：待处理，处理中，处理完成。用户可以在待处理和处理中的状态下点击终止来停止。

节点启动

- `WORKER_NAME`节点名，必填，保证每个进程有不同的节点名
- `HOST`通过HTTP访问时的主机名称，只通过IP就能访问的话可以随便写，此参数是必填的
- `IP`WEB服务的IP地址，如果IP地址是可以动态改变的话，那么可以不设置此参数
- `PORT`WEB服务端口，默认80，可以不填写
- `CACHETIME`游标缓存时间，默认是1分钟，`1m`

    cd pladmin
    WORKER_NAME=local-worker-01 HOST=pl-log-notic.az13js.cn IP=127.0.0.1 PORT=9210 CACHETIME=1m python3 manage.py export_worker
    WORKER_NAME=local-worker-02 HOST=pl-log-notic.az13js.cn IP=127.0.0.1 PORT=9210 CACHETIME=1m python3 manage.py export_worker
