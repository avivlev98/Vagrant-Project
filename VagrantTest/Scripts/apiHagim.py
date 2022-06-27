import requests
import json
from datetime import date
from datetime import datetime
st = datetime.strptime('2022-10-01', '%Y-%m-%d')
end = datetime.strptime('2022-12-01', '%Y-%m-%d')

response = requests.get('https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year=now&month=x&ss=on&mf=on&c=on&geo=geoname&geonameid=3448439&M=on&s=on',verify=False).json()
holidays_list = []
#packages_str = json.dumps(response, indent=2)
#print(packages_str)
for item in response['items']:
    if item['category']=='holiday':
        date_time_str = item['date']
        date_time_str = date_time_str[0:10]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
        if st <= date_time_obj <= end:
            hagim = json.dumps(item['hebrew'],ensure_ascii=False)
            data_time = json.dumps(item['date'],ensure_ascii=False)
            holidays_list.append([hagim, data_time])
            print(item['hebrew'])
            print(item['date'])



with open('data.json', 'w',encoding='utf-8') as outfile:
        json.dump(holidays_list, outfile,ensure_ascii=False)








