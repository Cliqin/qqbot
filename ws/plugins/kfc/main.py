import datetime
import os
import random

from plugins.base import Base


class Plugin(Base):
    """疯狂星期四"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.fdir = os.path.dirname(os.path.abspath(__file__))
        self.all_msg = self.load_msg()
        self.db = self.load_config()

    def load_msg(self):
        """加载到本地内存"""
        fpath = os.path.join(self.fdir, 'msg.txt')
        with open(fpath) as f:
            data = f.read()
        all_msg = [line for line in data.split('\n') if line.strip()]
        print(f'疯狂星期四语录加载完毕，共 {len(all_msg)} 条数据')
        return all_msg

    def is_match(self, message):
        """检测是否匹配此插件"""
        if 'user_id' in self.data and 'self_id' in self.data:
            if self.data['user_id'] == self.data['self_id']:
                return False
        match_strs = ['kfc', 'KFC', '肯德基', '疯狂星期四', 'vivo50', 'v我50']
        if datetime.datetime.today().isoweekday() == 4:
            for _key in match_strs:
                if _key in message:
                    return True
        return False

    async def handle(self, message):
        msg = random.choice(self.all_msg)
        msg = msg.replace('\\n', '\n')
        return msg
