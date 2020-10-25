# -*- coding: utf8 -*-

"""
    导出后的文件处理示例
如果你采用集群的方式部署，那么你可能希望在节点导出完成之后上传到文件服务上，然后给页面返回一个URL
提供用户下载。这里作为单机部署的示例，仅移动文件夹到static目录然后输出一个URL来。
如果你采用集群方式，把文件处理后输出下载的URL就行了。至于原理，那就是导出完成后Python调用一下
配置的脚本命令，把文件夹作为参数传递进来而已。
"""

import sys
import os
import uuid
import zipfile

def main():
    if len(sys.argv) < 1:
        print(__file__ + "【错误】参数个数太少", file = sys.stderr)
        exit(1)
    if False == os.path.isdir(sys.argv[1]):
        print(__file__ + "【错误】文件夹不存在 (" + sys.argv[1] + ")", file = sys.stderr)
        exit(1)

    scriptPath = os.path.split(os.path.realpath(__file__))[0]
    targetPath = scriptPath + os.sep + os.sep.join(["pltplconf", "static"])
    fileName = uuid.uuid1().hex + ".zip"
    targetFile = targetPath + os.sep + fileName

    with zipfile.ZipFile(targetFile, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=False) as zipObject:
        for file in os.listdir(sys.argv[1]):
            zipObject.write(sys.argv[1] + os.sep + file, file)

    # 输出文件下载路径。因为这个是单机示例，所以直接输出web目录为根目录的路径即可
    print("/static/" + fileName)

if __name__ == '__main__':
    main()