# -*- coding: utf8 -*-

import json
import logging

logger = logging.getLogger(__name__)

class ErrorFormate():

    # 分析规则
    rules = [
        {"start": "[msg] => ","end": "\n"}
    ]

    def parse(self, contents):
        """分析ES搜索到的记录，返回所需的信息"""
        results = json.loads(contents)
        errorMessages = []
        total = 0
        for log in results['responses']:
            for unit in log['hits']['hits']:
                total = total + 1
                for analysisInfo in self.analysis(unit['_source']['message']):
                    if analysisInfo['rule'] == 0:
                        errorMessages.append(analysisInfo['str'])
        return {"total": total, "errorMessages": errorMessages}

    def analysis(self, message):
        """分析日志文本"""

        rules = self.rules
        matchResults = []

        # 计算出每个符号的长度
        for u in rules:
            if "start" in u:
                u["startLen"] = len(u["start"])
            u["endLen"] = len(u["end"])

        # 待解析的字符长度
        messageLen = len(message)

        globalOffset = 0
        while True:
            minOffet = -2 # 最小的开始偏移值
            minOffetStrLen = -2 # 最小偏移值的规则的开始符长度
            minRuleKey = -2 # 规则

            # 计算当前字符串中，所有字符的起始位置，开始位置最前的记录下来。如果两个开始位置都最前，那么取开始字符长度最大的
            key = 0
            for u in rules:
                if "start" in u:
                    u["startOffset"] = message.find(u["start"], globalOffset)
                else:
                    minOffet = 0
                    minOffetStrLen = 0
                    minRuleKey = key
                    break

                if u["startOffset"] == -1:
                    ""
                else:
                    if minOffet == -2:
                        minOffet = u["startOffset"]
                        minOffetStrLen = u["startLen"]
                        minRuleKey = key
                    else:
                        if (u["startOffset"] < minOffet) or ((u["startOffset"] == minOffet) and (u["startLen"] > minOffetStrLen)):
                            minOffet = u["startOffset"]
                            minOffetStrLen = u["startLen"]
                            minRuleKey = key
                key = key + 1

            # 匹配失败，退出循环
            if minOffet == -2:
                break

            # 就匹配到的规则，开始寻找结束符号，提取中间的字符作为值
            matchRule = rules[minRuleKey]
            endOffset = message.find(matchRule["end"], minOffet + minOffetStrLen)
            # 查询失败退出循环
            if -1 == endOffset:
                break
            strMatch = message[(minOffet + minOffetStrLen) : endOffset]
            matchResults.append({
                "str": strMatch,
                "rule": minRuleKey
            })

            globalOffset = endOffset
            if minOffetStrLen == 0:
                break
        return matchResults
