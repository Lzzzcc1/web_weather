import pymysql

class Mysql(object):

    def __init__(self, config):
        self.config = config

    def connect_mysql(self):
        conn = pymysql.connect(**self.config)
        return conn

    def insert_history_data(self, args):
        conn = self.connect_mysql()
        cursor = conn.cursor()
        query_sql = 'SELECT * FROM history_weather WHERE year={} and month={} and city="{}"'.format(args[7], args[8], args[9])
        res = cursor.execute(query_sql)
        if not res:
            sql = 'INSERT INTO history_weather (average_high, average_low, highest_temperature, lowest_temperature,' \
                  'average_air_quality, highest_air_quality, lowest_air_quality, year, month, city ) values ' \
                  '("{}","{}","{}","{}","{}",{},{},{},{},"{}")'.format(args[0], args[1], args[2], args[3], args[4],
                                                                       args[5], args[6], args[7], args[8], args[9])
            cursor.execute(sql)
            conn.commit()
        cursor.close()
        conn.close()

    def insert_everyday_data(self, args):
        conn = self.connect_mysql()
        cursor = conn.cursor()
        for i in args:
            query_sql = 'SELECT * FROM everyday_weather WHERE date="{}" and city="{}"'.format(i['date'], i['city'])
            print(query_sql)
            res = cursor.execute(query_sql)
            if not res:
                insert_sql = 'INSERT INTO everyday_weather (date, highest_temperature, lowest_temperature, weather,' \
                             'wind_direction, year, month, city ) values ("{}","{}","{}","{}","{}",{},{},"{}")'\
                             .format(i['date'], i['highest_temperature'], i['lowest_temperature'],
                                     i['weather'], i['wind_direction'], i['year'], i['month'], i['city'])
                cursor.execute(insert_sql)
                conn.commit()
        cursor.close()
        conn.close()

    def insert_mysql(self, items, table_name):
        """
        item: 传入的字典，key的值必须与数据库的字段对应
        """
        conn = pymysql.connect(**self.config)
        # 获得Cursor对象
        cursor = conn.cursor()
        ls = [(k, v) for k, v in items.items() if v is not None]
        search_sql = 'select * from {} where city="{}" and date="{}";'.format(table_name, items['city'], items['date'])
        cursor.execute(search_sql)
        if cursor.fetchall():
            delete_sql = 'delete from {} where city="{}" and date="{}";'.format(table_name, items['city'], items['date'])
            cursor.execute(delete_sql)
            conn.commit()
        sql = 'INSERT INTO %s (' % table_name + ','.join([i[0] for i in ls]) + ') VALUES (' + ','.join(
            repr(i[1]) for i in ls) + ');'
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
