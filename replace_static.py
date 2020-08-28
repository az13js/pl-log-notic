#!/usr/local/bin/python3
# -*- coding: utf8 -*-

"""自动处理放入Django的html文件，替换标签"""
import sys
import os

def main():
    print(__file__ + "【消息】替换HTML中的静态文件路径")
    if len(sys.argv) < 1:
        print(__file__ + "【错误】参数个数太少", file = sys.stderr)
        exit(1)
    if False == os.path.isfile(sys.argv[1]):
        print(__file__ + "【错误】文件不存在 (" + sys.argv[1] + ")", file = sys.stderr)
        exit(1)

    fr = open(sys.argv[1], "r")
    content = fr.read()
    fr.close()

    content = content.replace("./static/", "{% static '");
    for ext in ["js", "css", "png", "jpg", "jpeg"]:
        content = content.replace("." + ext + "\"", "." + ext + "' %}\"");
    # Django需要
    content = "{% load static %}" + content

    fw = open(sys.argv[1], "w")
    fw.write(content)
    fw.close()
    print(__file__ + "【消息】替换完成")

if __name__ == '__main__':
    main()