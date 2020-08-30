from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PltplconfConfig(AppConfig):
    name = 'pltplconf'
    verbose_name = "pl-log-notic初始化"

    def ready(self):
        """服务器启动后初始化应用"""
        logger.info("初始化pl-log-notic")

