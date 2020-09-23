# -*- coding: utf8 -*-

"""示例用
"""
import logging
import requests
from django.conf import settings
import json
from string import Template

logger = logging.getLogger(__name__)

class WxTeamTime():
    def send(self, job, params):
        logger.debug("向企业微信群发送消息")
        messageText = """
【${job_name}】
Hi，请求时间统计信息如下：
采集数量：${total}
总时间：  ${total_time}
平均时间：${avg_time}
最大时间：${max_time}
最小时间：${min_time}
查询命令：${query_command}
"""
        tpl = Template(messageText)
        data = {
            "msgtype": "text",
            "text": {
                "content": tpl.substitute(
                    job_name = params["job_name"],
                    total = params["total"],
                    total_time = params["totalTime"],
                    avg_time = params["avgTime"],
                    max_time = params["maxTime"],
                    min_time = params["minTime"],
                    query_command = job.es_query
                )
            }
        }
        logger.debug(json.dumps(data))
        requests.post(url = settings.MESSAGERS_CONFIG["WxTeam"], headers = {"Content-Type": "text/plain"}, json = data)
