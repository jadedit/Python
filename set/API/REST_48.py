import requests
# https://iapi.bot.or.th/Developer?lang=th

url = \
    'https://iapi.bot.or.th/Stat/Stat-ExchangeRate/DAILY_AVG_EXG_RATE_V1/'
querystring = {'start_period': '2017-08-12', 'end_period': '2017-09-01', 'currency': 'SGD'}
headers = {'api-key': 'U9G1L457H6DCugT7VmBaEacbHV9RX0PySO05cYaGsm'}
response = requests.request('GET', url, headers=headers, params=querystring)
print(response.text)