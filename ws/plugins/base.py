class Base:
    def __init__(self):
        self.is_open = True     # 插件开关
        self.is_at = True       # 回复消息时是否at触发之人

    def is_match(self, message):
        """检测是否匹配此插件"""
        return True

    def handle(self, message):
        """核心处理逻辑"""
        pass

    def run(self, message):
        """外部调用入口"""
        if not self.is_open:
            return
        if not self.is_match(message):
            return
        return self.handle(message)
