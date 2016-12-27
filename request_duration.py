import requests, json, datetime

from datetime import datetime, timedelta
import pytz
from dominate.tags import s

tz = pytz.timezone('Asia/Ho_Chi_Minh')
vietname_time = datetime.now(tz)
startTime = str(vietname_time.date()) + 'T00:00:00'

print  vietname_time

yesterday = vietname_time - timedelta(days=7)
print yesterday
yesterday.strftime('%m%d%y')
#
# respond1 = requests.post("https://lbasense-hust.appspot.com/data", data={},
#                          headers={'type': 'VisitDurations', 'user': 'student-hust', 'pass': '123456a@', 'region': '0',
#                                   'startTime': '2016-11-03T00:00:00', 'endTime': '2016-11-06T14:00:00',
#                                   'resolution': 'hours'})
# print respond1.content
#
#
# respond1 = requests.post("https://lbasense-hust.appspot.com/data", data={},
#                          headers={'type': 'StatsSummary', 'user': 'student-hust', 'pass': '123456a@', 'region': '0',
#                                   'startTime': '2016-10-29T00:00:00', 'endTime': '2016-10-29T23:00:00',
#                                   'resolution': 'hours'})
# # print respond1.content
#
# respond1 = requests.post("https://lbasense-hust.appspot.com/data", data={},
#                          headers={'type': 'StatsSummary', 'user': 'student-hust', 'pass': '123456a@', 'region': '0',
#                                   'startTime': '2016-11-04T00:00:00', 'endTime': '2016-11-04T23:00:00',
#                                   'resolution': 'hours'})
# print respond1.content