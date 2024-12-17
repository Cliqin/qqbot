# -*- coding: utf-8 -*-
"""
简易查询IP归属地
作者： 快乐哈哈
时间： 2024.11.01
"""
import os
import json
import requests

from plugins.base import Base


class Plugin(Base):
    """查询 IP 归属地插件"""

    def __init__(self):
        super().__init__()
        self.is_at = True
        self.ip_location_api_url = 'https://webapi-pc.meitu.com/common/ip_location'
        self.last_activity_time = None

    def is_match(self, message):
        return message.startswith('IP:') or message.startswith('ip:') or message.startswith(
            'IP：') or message.startswith('ip：')

    async def handle(self, message):
        if self.is_match(message):
            ip = message.split('IP:')[1].strip()
            if ip:
                return self.get_ip_location(ip)
            else:
                return "请提供要查询的 IP 地址。"
        else:
            return None

    def get_ip_location(self, ip):
        url = f'{self.ip_location_api_url}?ip={ip}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data.get('code') == 0:
                    ip_info = data['data'].get(ip, None)
                    if ip_info:
                        nation = ip_info['nation']
                        province = ip_info['province']
                        city = ip_info['city']
                        return f"{nation} {province} {city}"
                    else:
                        return f"无法查询 IP {ip} 的归属地。"
                else:
                    return f"无法查询 IP {ip} 的归属地。"
            else:
                return f"查询 IP {ip} 归属地失败。状态码：{response.status_code}。"
        except requests.exceptions.RequestException as e:
            return f"查询 IP {ip} 归属地时出现错误：{str(e)}。"
