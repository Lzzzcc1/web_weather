import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import MYSQL_CONFIG
from models.models import db
from views import login, charts
from datetime import timedelta
from crawl_class.crawl_future import Weather

def create_app():
    path = os.getcwd()
    print(r'{}/static/'.format(path))
    app = Flask(__name__, static_folder=r'C:\Users\wuqua\PycharmProjects\web_weather\static')
    app.secret_key = 'weather'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/' \
                                            '{}?charset=utf8'.format(MYSQL_CONFIG['user'],
                                                                     MYSQL_CONFIG['password'],
                                                                     MYSQL_CONFIG['host'],
                                                                     MYSQL_CONFIG['database'])
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    db.init_app(app)

    @app.route('/', endpoint='index', methods=['GET'])
    def index():
        return render_template('login.html')

    app.register_blueprint(login)
    app.register_blueprint(charts)

    return app


app = create_app()
bootstrap = Bootstrap(app)

if __name__ == '__main__':
    city_list = ['beijing', 'fuzhou', 'shanghai', 'hangzhou', 'shenzhen']
    # for i in city_list:
    #     weather = Weather(MYSQL_CONFIG, i, 15)
    #     weather.get_data()
    #     print(i)
    app.run(host='localhost', port=5000, debug=False)
