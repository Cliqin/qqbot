from collections import deque

from plugins.base import Base


class Plugin(Base):
    """复读机"""
    def __init__(self):
        super().__init__()
        self.is_at = False
        self.data = None
        self.maxlen = 2
        self.msgs = {}

    async def handle(self, message):
        group_id = self.data['group_id']
        if group_id not in self.msgs:
            self.msgs[group_id] = deque(maxlen=self.maxlen)

        if self.data['user_id'] == self.data['self_id']:
            self.msgs[group_id].clear()
        else:
            self.msgs[group_id].append(message.strip())
            if len(self.msgs[group_id]) == self.maxlen \
                    and len(set(self.msgs[group_id])) == 1:
                return message
