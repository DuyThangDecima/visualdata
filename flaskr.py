# -*- coding: utf-8 -*-

import os
import requests
from sqlite3 import dbapi2 as sqlite3

from datetime import date
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify
import time
import datetime

# create our little application :)
from flask import json
import datetime
import pytz

app = Flask(__name__)

# Load default config and override config from an environment variable
# app.config.update(dict(
#     DATABASE=os.path.join(app.root_path, 'flaskr.db'),
#     DEBUG=True,
#     SECRET_KEY='development key',
#     USERNAME='admin',
#     PASSWORD='default'
# ))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
#
# def init_db():
#     """ Thực hiện tạo database."""
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#
#
# @app.cli.command('initdb')
# def initdb_command():
#     """Creates the database tables."""
#     init_db()
#     print('Initialized the database.')
#
#
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()
#
#
# @app.route('/')
# def show_entries():
#     db = get_db()
#     cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)
#
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     db = get_db()
#     db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('current2.html')


@app.route("/ajax_current", methods=['POST'])
def ajax_current():
    # region = request.json['region'];
    time = request.json['time']
    # Lấy giờ Việt Nam online
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietname_time = datetime.datetime.now(tz).date();
    if time == 'today':
        date = vietname_time;
        startTime = str(date) + 'T00:00:00'
        endTime = str(vietname_time) + 'T23:00:00'
    elif time == 'yesterday':
        date = vietname_time - datetime.timedelta(days=1)
        startTime = str(date) + 'T00:00:00'
        endTime = str(date) + 'T23:00:00'
    elif time == 'last7day':
        date = vietname_time - datetime.timedelta(days=7)
        yesterday = vietname_time - datetime.timedelta(days=1)
        startTime = str(date) + 'T00:00:00'
        endTime = str(yesterday) + 'T23:00:00'

    print startTime
    print endTime
    return statsSummaryCurrent(startTime, endTime, "hours")


@app.route('/duration', methods=['GET', 'POST'])
def duration():
    return render_template('duration.html')


@app.route("/ajax_duration", methods=['POST'])
def ajax_duration():
    # Chuẩn hóa lại startTime
    startTime = request.json['startTime'];
    d = datetime.datetime.strptime(startTime, "%d/%m/%Y %H:%M:%S")
    startTime = d.strftime("%Y-%m-%dT%H:%M:%S")

    # Chuẩn hóa lại endTime
    endTime = request.json['endTime'];
    d = datetime.datetime.strptime(endTime, "%d/%m/%Y %H:%M:%S")
    endTime = d.strftime("%Y-%m-%dT%H:%M:%S")

    # Region cần lấy số liệu:
    # 00 là tất cả
    # 01, 02, 03, 04 theo thứ tự region HUST1. HUST2. HUST3. HUST4.
    region = request.json['region'];

    print "START_TIME" + startTime
    print "end_TIME" + startTime
    print "region" + region
    respond = requests.post("https://lbasense-hust.appspot.com/data", data={},
                            headers={'type': 'VisitDurations', 'user': 'student-hust', 'pass': '123456a@',
                                     'region': region,
                                     'startTime': startTime, 'endTime': endTime})
    print respond.content;
    return jsonify(data=respond.content, region=region)


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('.html')


@app.route('/visit_return', methods=['GET', 'POST'])
def visit_return():
    return render_template('visit-return.html')


# Hàm ajax nhận request hiển thị đồ thị
# Dữ liệu trả về {data=data,resolution=resolution,region=region}


@app.route("/ajax_visit_return", methods=['POST'])
def ajax_visit_return():
    # Chuẩn hóa lại startTime
    startTime = request.json['startTime'];
    endTime = request.json['endTime'];

    if startTime != "" and endTime != "":
        d = datetime.datetime.strptime(startTime, "%d/%m/%Y %H:%M:%S")
        startTime = d.strftime("%Y-%m-%dT%H:%M:%S")

        # Chuẩn hóa lại endTime
        d = datetime.datetime.strptime(endTime, "%d/%m/%Y %H:%M:%S")
        endTime = d.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        # Nếu mà startTime với EndTime chưa có nghĩa là
        # load trang lần đầu, tự động ajax
        # Mình se hiển thị dữ liệu trong 1 tháng
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        vietname_time = datetime.datetime.now(tz).date();
        date = vietname_time - datetime.timedelta(days=30)

        startTime = str(date) + 'T00:00:00'
        endTime = str(vietname_time) + 'T23:00:00'

    # Kiểu hiển thị days hoặc hourse
    resolution = request.json['resolution'];

    # Region cần lấy số liệu:
    # 00 là tất cả
    # 01, 02, 03, 04 theo thứ tự region HUST1. HUST2. HUST3. HUST4.
    region = request.json['region'];
    return statsSummary(region, startTime, endTime, resolution)


# Lấy thời gian hiện tại
def statsSummaryCurrent(startTime, endTime, resolution):
    # Lấy thông tin các region
    infoRegions = requests.post("https://lbasense-hust.appspot.com/data", data={},
                                headers={'type': 'RegionNames', 'user': 'student-hust',
                                         'pass': '123456a@'}).content

    print infoRegions
    infoRegions = json.loads(infoRegions);

    # Đinh dạng data
    # {
    #  {"regionName":"",
    #   "value":[]
    #  }
    # ,{
    #   "regionName":"",
    #   "value":[] }...}
    #  }
    #
    data = []

    # Lần lượt request theo region lấy số liệu

    for key, value in infoRegions.items():
        reponds = requests.post("https://lbasense-hust.appspot.com/data", data={},
                                headers={'type': 'StatsSummary',
                                         'user': 'student-hust',
                                         'pass': '123456a@',
                                         'region': key,
                                         'startTime': startTime,
                                         'endTime': endTime,
                                         'resolution': resolution})
        if reponds.status_code == 200:
            items = {}
            items["value"] = (json.loads(reponds.content))["summaryStats"]
            items["regionName"] = value
            data.append(items)

    # Chuẩn hóa lại thời gian, gửi cho client. Đáng nhẽ làm ở client
    d = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    startTime = d.strftime("%d/%m/%Y %H:%M:%S")

    d = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")
    endTime = d.strftime("%d/%m/%Y %H:%M:%S")
    result = jsonify(data=data, resolution=resolution, startTime=startTime, endTime=endTime)
    return result

def statsSummary(region, startTime, endTime, resolution):
    # Lấy số lượng region
    infoRegions = requests.post("https://lbasense-hust.appspot.com/data", data={},
                                headers={'type': 'RegionNames', 'user': 'student-hust',
                                         'pass': '123456a@'}).content
    print infoRegions;

    inforRegionJson = json.loads(infoRegions).keys();
    print infoRegions
    numberRegion = len(inforRegionJson);
    print "NUMBERREGION" + str(numberRegion)

    # Lần lượt request theo region lấy số liệu
    array_total = []
    data = '{"data":['
    for i in range(numberRegion):

        reponds = requests.post("https://lbasense-hust.appspot.com/data", data={},
                                headers={'type': 'StatsSummary',
                                         'user': 'student-hust',
                                         'pass': '123456a@',
                                         'region': inforRegionJson[i],
                                         'startTime': startTime,
                                         'endTime': endTime,
                                         'resolution': resolution})
        if reponds.status_code == 200:
            if (i + 1) != numberRegion:
                data += reponds.content.replace("summaryStats", "HUST") + ","
            else:
                data += reponds.content.replace("summaryStats", "HUST") + "]}"

    print data;

    # Chuẩn hóa lại thời gian, gửi cho client. Đáng nhẽ làm ở client
    d = datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
    startTime = d.strftime("%d/%m/%Y %H:%M:%S")

    d = datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")
    endTime = d.strftime("%d/%m/%Y %H:%M:%S")

    result = jsonify(data=data, resolution=resolution, region=region, startTime=startTime, endTime=endTime)
    return result


def process(array_total, charType):
    print "PROCESS"
    array_date = []
    indexs = []
    for i in range(len(array_total)):
        indexs.append(0)

    while True:
        dates = []

        countFinish = 0;
        teampDates = []
        for i in range(len(indexs)):
            if indexs[i] >= len(array_total[i]):
                countFinish = countFinish + 1;

        if countFinish == len(indexs):
            break;

        for i in range(len(indexs)):
            if indexs[i] < len(array_total[i]):
                date = array_total[i][indexs[i]]['date']
                dates.append(date)
                teampDates.append(date)
            else:
                teampDates.append("")

        minDate = min(dates)
        added = False
        for i in range(0, len(indexs)):
            if teampDates[i] == minDate:
                indexs[i] = indexs[i] + 1;
                if not added:
                    added = True
                    array_date.append(minDate)

    print array_date
    # result = "["
    result = ""
    # Vơí mỗi ngày
    for i in range(len(array_date)):
        dateEach = array_date[i]
        result += '{"date":' + '"' + dateEach + '",'
        # Tìm kiếm trong danh sách mảng
        for j in range(len(array_total)):
            value = ""
            isExist = False
            # Trong mảng của mỗi phẩn tử,
            for k in range(len(array_total[j])):
                if (array_total[j][k]['date'] == dateEach):
                    value = '"0' + str(j) + '":"' + str(array_total[j][k][charType]) + '",'
                    isExist = True
                    break;

            if isExist:
                result += value;
            else:
                result += '"0' + str(j) + '":' + '"0",'

        # Xóa dấu , ở cuối cùng
        potision = result.rfind(",")
        result = list(result)

        result[potision] = ''
        result = ''.join(result)

        result += "},"
    # result += "]"
    potision = result.rfind(",")
    result = list(result)

    result[potision] = ''
    result = ''.join(result)

    print result
    return result


# Lấy số lượng region từ server
def getNumberRegion():
    infoRegions = requests.post("https://lbasense-hust.appspot.com/data", data={},
                                headers={'type': 'RegionNames', 'user': 'student-hust',
                                         'pass': '123456a@'}).content
    print infoRegions;

    inforRegionJson = json.loads(infoRegions).keys();
    print infoRegions
    numberRegion = len(inforRegionJson);
    return numberRegion;
