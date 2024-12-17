from plugins.base import Base
import json
import re
from plugins.GetExpress.GetExpress import Express


class Plugin(Base):
    def __init__(self):
        super().__init__()
        self.is_at = True

    def is_match(self, message):
        """检测是否匹配此插件"""
        if message[:2] == '快递':
            return True
        else:
            return False

    async def handle(self, message):
        a = message[2:].strip()
        if a == '':
            return '查快递请输入：快递 xxxxxxxxxx'
        else:
            msg = Express(a).getExpress()
            return msg
