import requests
from lxml import etree
from config import MYSQL_CONFIG
from util.mysql import Mysql

class Weather(Mysql):

    def __init__(self, config, year, month, city):
        if month >= 10:
            self.url = 'http://lishi.tianqi.com/{}/{}{}.html'.format(city, year, month)
        else:
            self.url = 'http://lishi.tianqi.com/{}/{}0{}.html'.format(city, year, month)
        Mysql.__init__(self, config)
        self.condition = [year, month, city]

    def get_data(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap'
                                 'pleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        html = requests.get(self.url, verify=False, headers=headers)
        html = etree.HTML(html.content.decode())
        content = html.xpath("//div[@class='main clearfix']/div/div[@class='inleft_tian']/ul/li")
        num = 0
        history_data = []
        for i in content:
            if num == 0:
                history_data.append(''.join(i.xpath("./div[1]/div[1]/text()")).strip())
                history_data.append(''.join(i.xpath("./div[2]/div[1]/text()")).strip())
            else:
                history_data.append(''.join(i.xpath("./div[1]/text()")).strip())
            num += 1
        history_data.extend(self.condition)
        return history_data


if __name__ == '__main__':
    weather = Weather(MYSQL_CONFIG, 2021, 4, 'hangzhou')
    data = weather.get_data()
    weather.insert_history_data(data)