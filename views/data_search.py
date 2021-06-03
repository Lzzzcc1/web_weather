import datetime
from flask import request, jsonify, render_template, session, make_response, send_from_directory
from views import charts
from models import db
from models.models import Everyday, History, User, Future
from sqlalchemy import desc, func
import re
import os
import csv

@charts.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = username
            return render_template('index.html')
        else:
            return render_template('login.html')

@charts.route('/index', methods=["GET"])
def to_index():
    if request.method == 'GET':
        return render_template('index.html')

@charts.route('/to_table', methods=["GET"])
def to_table():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        table_weather = Everyday.query.filter_by(city=city, year=year, month=month).all()
        res = []
        for i in table_weather:
            current_data = {
                "date": i.date,
                "highest": i.highest_temperature,
                "lowest": i.lowest_temperature,
                "weather": i.weather,
                "wind": i.wind_direction,
                "city": i.city
            }
            res.append(current_data)
        return jsonify(res)

@charts.route('/table', methods=["GET"])
def table():
    data = request.args.get("data")
    data = eval(data)
    print(data)
    return render_template('table.html', u=data)

@charts.route('/special', methods=["GET"])
def special():
    user = User.query.filter_by(username=session['user']).first()
    if not user.special_city:
        return ''
    return user.special_city

@charts.route('/to_register', methods=["GET"])
def to_register():
    return render_template('register.html')

@charts.route('/to_login', methods=["GET"])
def to_login():
    return render_template('login.html')

@charts.route('/return', methods=["GET"])
def return_index():
    return render_template('index.html')

@charts.route('/c1', methods=["GET"])
def c1():
    city = request.args.get("city")
    month = request.args.get("year_and_month")
    return jsonify({"city": city, "month": month})

@charts.route('/register', methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    user = User.query.filter_by(username=username).first()
    if user:
        return '已存在用户名'
    else:
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')


@charts.route('/line', methods=["GET"])
def line():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        everyday_data = Everyday.query.filter_by(city=city, year=year, month=month)
        date, highest, lowest = [], [], []
        for data in everyday_data:
            date.append(data.date[5:10])
            highest.append(float(data.highest_temperature.strip('℃')))
            lowest.append(float(data.lowest_temperature.strip('℃')))
        return jsonify({"date": date, "highest": highest, "lowest": lowest})


@charts.route('/follow', methods=["POST"])
def follow():
    city = request.form['city']
    user = User.query.filter_by(username=session['user']).first()
    user.special_city = city
    db.session.commit()
    db.session.close()
    return make_response('ok')


@charts.route('/export', methods=["POST"])
def export():
    city = request.form['city']
    year_and_month = request.form["year_and_month"]
    if not city:
        city = 'beijing'
    if not year_and_month:
        year_and_month = '2021 4'
    year = int(year_and_month.split(' ')[0])
    month = int(year_and_month.split(' ')[1])
    weather_data = Everyday.query.filter_by(city=city, year=year, month=month).all()
    result = []
    for i in weather_data:
        one_data = (i.date, i.highest_temperature, i.lowest_temperature, i.weather, i.wind_direction, i.year, i.month,
                    i.city)
        result.append(one_data)
    path = os.getcwd() + '/csv/weather_data.csv'
    csv_file = open(path, 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(('日期', '最高温度', '最低温度', '天气', '风向等级', '年', '月', '城市'))
    writer.writerows(result)
    csv_file.close()
    return make_response('ok')

@charts.route('/download', methods=['GET'])
def download():
    directory = os.getcwd() + '/csv'
    print(directory)
    return send_from_directory(directory, 'weather_data.csv', as_attachment=True)

@charts.route('/histogram', methods=["GET"])
def histogram():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        everyday_weather = []
        everyday_weather_count = []
        everyday_data = Everyday.query.add_columns(func.count(Everyday.weather),
                                                   Everyday.weather).filter_by(city=city, year=year, month=month).\
                                                   group_by(Everyday.weather). order_by(Everyday.weather).all()
        for i in everyday_data:
            everyday_weather_count.append(i[1])
            everyday_weather.append(i[2])
        return jsonify({"weather": everyday_weather, "count": everyday_weather_count})

@charts.route('/history', methods=["GET"])
def history():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        history_data = History.query.filter_by(city=city, year=year, month=month).first()
        result = {"ah": history_data.average_high, "al": history_data.average_low,
                  "ht": history_data.highest_temperature, "lt": history_data.lowest_temperature,
                  "aaq": history_data.average_air_quality, "haq": history_data.highest_air_quality,
                  "laq": history_data.lowest_air_quality}
        return jsonify(result)


@charts.route('/wind', methods=["GET"])
def wind():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        wind_all = Everyday.query.filter_by(city=city, year=year, month=month)
        wind_result = []
        date = []
        for one_wind in wind_all:
            wind_level = re.findall(r" (.+?)级", one_wind.wind_direction)[0]
            wind_result.append(int(wind_level))
            date.append(one_wind.date[5:10])
        return jsonify({"wind": wind_result, "date": date})


@charts.route('/wind_histogram', methods=["GET"])
def wind_histogram():
    if request.method == 'GET':
        city = request.args.get("city")
        year_and_month = request.args.get("year_and_month")
        if not city:
            city = 'beijing'
        if not year_and_month:
            year_and_month = '2021 4'
        year = int(year_and_month.split(' ')[0])
        month = int(year_and_month.split(' ')[1])
        everyday_wind = []
        everyday_wind_count = []
        total_wind = Everyday.query.add_columns(func.count(Everyday.wind_direction),
                                                Everyday.wind_direction).filter_by(city=city, year=year, month=month)\
            .group_by(Everyday.wind_direction).order_by(Everyday.wind_direction).all()
        for i in total_wind:
            everyday_wind_count.append(i[1])
            everyday_wind.append(i[2])
        return jsonify({"wind": everyday_wind, "wind_count": everyday_wind_count})

@charts.route('/future_weather', methods=["GET"])
def future_weather():
    if request.method == 'GET':
        city = request.args.get("city")
        now_date = datetime.datetime.now().strftime("%m-%d")
        date_list = []
        for i in range(15):
            date_list.append((datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%m-%d"))
        return render_template('future.html', city=city, date_list=date_list)

@charts.route('/future_line', methods=["POST"])
def future_line():
    if request.method == 'POST':
        city = request.form["city"].strip()
        if not city:
            city = 'beijing'
        everyday_data = Future.query.filter_by(city=city)
        date, highest, lowest = [], [], []
        for data in everyday_data:
            date.append(data.date)
            highest.append(data.highest_temperature)
            lowest.append(data.lowest_temperature)
        return jsonify({"date": date, "highest": highest, "lowest": lowest})

@charts.route('/humidity_line', methods=["POST"])
def humidity_line():
    if request.method == 'POST':
        city = request.form["city"].strip()
        if not city:
            city = 'beijing'
        everyday_data = Future.query.filter_by(city=city)
        date, humidity = [], []
        for data in everyday_data:
            date.append(data.date)
            humidity.append(data.humidity.strip('%'))
        return jsonify({"date": date, "humidity": humidity})

@charts.route('/future_histogram', methods=["POST"])
def future_histogram():
    if request.method == 'POST':
        city = request.form["city"].strip()
        if not city:
            city = 'beijing'
        future_weather_count = []
        future_fif_weather = []
        everyday_data = Future.query.add_columns(func.count(Future.weather), Future.weather).filter_by(city=city).\
            group_by(Future.weather).order_by(Future.weather).all()
        for i in everyday_data:
            future_weather_count.append(i[1])
            future_fif_weather.append(i[2])
        return jsonify({"weather": future_fif_weather, "count": future_weather_count})

@charts.route('/current_data', methods=["POST"])
def current_data():
    if request.method == 'POST':
        city = request.form["city"].strip()
        date = request.form["date"].strip()
        if not city:
            city = 'beijing'
        search_weather = Future.query.filter_by(city=city, date=date).first()
        if search_weather:
            result = {"date": search_weather.date, "ht": search_weather.highest_temperature,
                      "lt": search_weather.lowest_temperature, "weather": search_weather.weather,
                      "humidity": search_weather.humidity}
        else:
            result = {"date": "", "ht": "",
                      "lt": "", "weather": "",
                      "humidity": ""}
        return jsonify(result)

@charts.route('/export_future', methods=["POST"])
def export_future():
    city = request.form['city'].strip()
    date = request.form["date"].strip()
    future_data = Future.query.filter(Future.city == city).filter(Future.date >= date).all()
    print(future_data)
    result = []
    for i in future_data:
        one_data = (i.date, i.highest_temperature, i.lowest_temperature, i.weather, i.humidity, i.city)
        result.append(one_data)
    path = os.getcwd() + '/csv/weather_data.csv'
    csv_file = open(path, 'w', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(('日期', '最高温度', '最低温度', '天气', '湿度', '城市'))
    writer.writerows(result)
    csv_file.close()
    return make_response('ok')
# @charts.route('/time')
# def get_time():
#     time_str = time.strftime("%Y{}%m{}%d{} %X")
#     return time_str.format("年", "月", "日")