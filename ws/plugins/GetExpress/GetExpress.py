import requests
import json
import random
import time


class Express:
    def __init__(self, num):
        self.num = num
        self.text = ''
        self.url_1 = f'https://alayn.baidu.com/express/appdetail/get_com?num={num}&cb='
        self.time_json()
        self.post_get = requests.session()
        self.ua = {'User-Agent':  random.choice([
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25 ',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4',
            'Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        ])}
        self.express_type = {
            'all': {'type': 'POST', 'url': 'https://api.huiniao.top/interface/third/kuaidi', 'data': {'num': num}, 'data_type': 'data'},
            'yuantong': {'type': 'POST', 'url': 'https://www.yto.net.cn/ec/order/gwWaybillInfoList', 'data': [num], 'data_type': 'json'}
        }

    def time_json(self):
        timestamp_full = time.time()
        timestamp_int = int(timestamp_full)
        timestamp_fraction = int((timestamp_full - timestamp_int) * 1000)  # 小数点后三位
        formatted_string = f"jsonp_{timestamp_int}_{timestamp_fraction:03d}"
        self.url_1 = self.url_1 + formatted_string

    def getExpressType(self):
        try:
            r = self.post_get.get(self.url_1, headers=self.ua)
            if r.status_code == 200:
                r = r.text
                start_index = r.index('(') + 1
                end_index = r.rindex(')')
                r = json.loads(r[start_index:end_index])
                return True, r['data']['company']
            else:
                return False, f'获取快递公司失败'
        except Express as e:
            return False, f'程序错误:{e}'

    def print_logistics(self, logistics):
        for item in logistics['data']['list']:
            timestamp = item['time']
            status = item['status']
            desc = item['desc']
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            self.text = self.text + f"\n【{status}】-【{formatted_time}】- {desc}"

    def print_logistics_info(self, logistics):
        for info in logistics:
            op_time = info['opTime']
            # op_org_name = info['opOrgName']
            op_name = info['opName']
            description = info['description']
            self.text = self.text + f'\n【{op_name}】-【{op_time}】- {description}'

    def getExpress(self):
        try:
            get_express_type = self.getExpressType()
            if get_express_type[0]:
                if get_express_type[1] in self.express_type:
                    if self.express_type[get_express_type[1]]['type'] == 'POST':
                        r = self.post_get.post(self.express_type[get_express_type[1]]['url'], json=self.express_type[get_express_type[1]]['data'])
                        if r.status_code == 200:
                            r = json.loads(r.text)
                            self.print_logistics_info(r[0]['waybillProcessInfo'])
                            return f'快递单号：{self.num}' + self.text
                        else:
                            return '获取快递信息失败'
                    else:
                        return f'{get_express_type[1]} 快递, 暂不支持get查询'
                elif get_express_type[1] == '':
                    return f'请输入正确的快递单号'
                else:
                    if self.express_type['all']['type'] == 'POST':
                        r = self.post_get.post(self.express_type['all']['url'], json=self.express_type['all']['data'])
                        if r.status_code == 200:
                            r = json.loads(r.text)
                            if r['code'] == 1:
                                self.print_logistics(r)
                                return f'快递单号：{self.num}' + self.text
                            else:
                                info = f'快递单号：{self.num}\n \n{r["info"]}'
                                return False, info
                        else:
                            return '获取快递信息失败'
                    else:
                        return f'{get_express_type[1]} 快递, 暂不支持get查询'
            else:
                return get_express_type[1]
        except Express as e:
            return f'程序错误:{e}'

