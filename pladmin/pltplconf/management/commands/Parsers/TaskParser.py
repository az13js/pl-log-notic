# -*- coding: utf8 -*-

import logging
import json

logger = logging.getLogger(__name__)

class TaskParser():
    def parse(self, taskSetting, queryLog):
        if "" != taskSetting.placeholders:
            placeholdersData = json.loads(taskSetting.placeholders)
        else:
            placeholdersData = []
        placeholders = []
        for data in placeholdersData:
            placeholders.append(Placeholder(data["placeholder"], data["start"], data["end"]))
        return TemplateParser(placeholders, queryLog).parse(taskSetting.template)

class TemplateParser():
    """模板解析，这个的逻辑跟前端页面typescript的逻辑一致"""
    _placeholders = []
    _placeholderResults = []

    def __init__(self, placeholders, sourceText):
        self._placeholders = placeholders
        for placeholder in placeholders:
            self._placeholderResults.append(placeholder.parse(sourceText))

    def parse(self, templateText):
        replaceString = templateText
        for key in range(len(self._placeholders)):
            placeholder = self._placeholders[key]
            results = self._placeholderResults[key]
            if placeholder.placeholder == "":
                continue
            replaceString = replaceString.replace(placeholder.placeholder, ",".join(results))
        return replaceString

class Placeholder():
    """占位符，这个的逻辑跟前端页面typescript的逻辑一致"""
    placeholder = ""
    start = ""
    end = ""

    def __init__(self, placeholder, start, end):
        self.placeholder = placeholder
        self.start = start
        self.end = end

    def parse(self, contents):
        if "" == self.placeholder:
            return []
        if "" == self.start and "" == self.end:
            return [contents]
        if "" == self.start and "" != self.end:
            endOffset = contents.find(self.end)
            if endOffset < 0:
                return []
            if 0 == endOffset:
                return [""]
            return [contents[0:endOffset]]
        if "" != self.start and "" == self.end:
            startOffset = contents.find(self.end)
            if startOffset < 0:
                return []
            return [contents[startOffset:len(self.start)]]
        matchs = []
        startOffset = 0
        endOffset = 0
        startOffset = contents.find(self.start, endOffset)
        while startOffset >= 0:
              endOffset = contents.find(self.end, startOffset + len(self.start))
              if endOffset < 0:
                  break
              matchs.append(contents[startOffset + len(self.start):endOffset])
              startOffset = contents.find(self.start, endOffset)
        return matchs
