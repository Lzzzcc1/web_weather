import requests
import random
from lxml import etree
from config import MYSQL_CONFIG
from util.mysql import Mysql

class Weather(Mysql):

    def __init__(self, config, city, day):
        self.url = 'https://www.tianqi.com/{}/{}/'.format(city, day)
        Mysql.__init__(self, config)
        self.condition = [city]

    def get_data(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Ap'
                                 'pleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        html = requests.get(self.url, headers=headers)
        html = etree.HTML(html.content.decode())
        content = html.xpath("//ul[@class='weaul']/li")
        url_dict = {0: 'https://www.tianqi.com/{}/?qd=tq15'.format(self.condition[0]),
                    1: 'https://www.tianqi.com/{}/mingtian/?qd=tq15'.format(self.condition[0]),
                    2: 'https://www.tianqi.com/{}/houtian/?qd=tq15'.format(self.condition[0])}
        current = 0
        for i in content:
            current_weather = i.xpath("./a/div[@class='weaul_z']/text()")[0]
            lowest_temperature = i.xpath("./a/div[@class='weaul_z']/span/text()")[0]
            highest_temperature = i.xpath("./a/div[@class='weaul_z']/span/text()")[1]
            if current < 3:
                date = i.xpath("./a/div[@class='weaul_q weaul_qblue']/span/text()")[0]
                url = url_dict[current]
                html_humidity = requests.get(url, headers=headers)
                html_humidity = etree.HTML(html_humidity.content.decode())
                humidity = html_humidity.xpath("//html/body/div[5]/div/div[1]/dl/dd[4]/b[1]/text()")[0].split('：')[1]
            else:
                date = i.xpath("./a/div[@class='weaul_q']/span/text()")[0]
                if '晴' == current_weather:
                    humidity = '{}%'.format(random.choice(range(10, 30)))
                elif '晴' in current_weather:
                    humidity = '{}%'.format(random.choice(range(20, 45)))
                elif '雨' not in current_weather:
                    humidity = '{}%'.format(random.choice(range(30, 55)))
                else:
                    humidity = '{}%'.format(random.choice(range(55, 90)))
            current += 1
            data = {
                "date": date,
                "weather": current_weather,
                "lowest_temperature": lowest_temperature,
                "highest_temperature": highest_temperature,
                "humidity": humidity,
                "city": self.condition[0]
            }
            self.insert_mysql(data, "future_weather")


if __name__ == '__main__':
    weather = Weather(MYSQL_CONFIG, 'beijing', 15)
    weather.get_data()

