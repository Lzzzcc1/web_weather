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
        content = html.xpath("//div[@class='main_left inleft']/div[@class='tian_three']/ul/li")
        history_data = []
        for i in content:
            everyday_data = i.xpath('./div/text()')
            everyday_data_dict = {
                "date": everyday_data[0],
                "highest_temperature": everyday_data[1],
                "lowest_temperature": everyday_data[2],
                "weather": everyday_data[3],
                "wind_direction": everyday_data[4],
                "year": self.condition[0],
                "month": self.condition[1],
                "city": self.condition[2]
            }
            history_data.append(everyday_data_dict)
        return history_data


if __name__ == '__main__':
    weather = Weather(MYSQL_CONFIG, 2021, 4, 'hangzhou')
    data = weather.get_data()
    weather.insert_everyday_data(data)
