# -*- coding: utf-8 -*-
"""
作者：   只会敲键盘的猿人
时间：   2024.10.11日
公众号： 只会敲键盘的猿人
版本：   V1.0.1
"""

from plugins.base import Base
import requests
import json
import time


class Plugin(Base):
    def __init__(self):
        super().__init__()
        self.is_at = True
        self.post_get = requests.session()
        self.ua = {
            'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320 Edg/129.0.0.0'
        }

    def getAllHash(self, info):
        music_hash = []
        for i in info:
            if i['hash'].strip != '':
                music_hash.append({'hash': i['hash'], 'ownercount': i['ownercount']})
                if i['group']:
                    for ii in i['group']:
                        if 'hash' in ii and ii['hash'].strip != '':
                            music_hash.append({'hash': ii['hash'], 'ownercount': ii['ownercount']})
        if music_hash:
            return True, sorted(music_hash, key=lambda x: x['ownercount'], reverse=True)
        else:
            return False, '未查询到相关歌曲'

    def getUrl(self, music_hash):
        music_url = f'https://m.kugou.com/app/i/getSongInfo.php?cmd=playInfo&hash='
        for i in music_hash:
            try:
                music_r = json.loads(self.post_get.post(music_url + i['hash'], headers=self.ua).text)
                if isinstance(music_r['backup_url'], list):
                    return True, music_r['backup_url'][0]
                time.sleep(0.5)
            except Exception as e:
                return False, f'错误{e}'
        return False, "查询到相关歌曲，但全部收费"

    def getMusic(self, name):
        hash_url = f'http://mobilecdn.kugou.com/api/v3/search/song?format=json&keyword={name}&page=1'
        try:
            hash_r = json.loads(self.post_get.post(hash_url, headers=self.ua).text)
            if 'data' in hash_r and 'info' in hash_r['data']:
                if hash_r['data']['info']:
                    get_all_hash = self.getAllHash(hash_r['data']['info'])
                    if get_all_hash[0]:
                        get_url = self.getUrl(get_all_hash[1])
                        if get_url[0]:
                            return True, get_url[1]
                        else:
                            return True, get_url[1]
                    else:
                        return False, '未查询到相关歌曲'
                else:
                    return False, '未查询到相关歌曲'
            else:
                return False, '未查询到相关歌曲'
        except Exception as e:
            return False, f'错误：{e}'

    def is_match(self, message):
        """检测是否匹配此插件"""
        if message[:2] == '点歌':
            return True
        else:
            return False

    async def handle(self, message):
        a = message[2:].strip()
        if a == '':
            return '''🚀点歌程序
            
发送信息：点歌 + 歌名
                    
想要搜索更准确请在歌名后加入歌手名字'''
        else:
            music = self.getMusic(a)
            if music[0]:
                return f'[CQ:record,file={music[1]},timeout=60]'
            else:
                return music[1]
