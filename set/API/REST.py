import requests
# อัตราแลกเปลี่ยนเฉลี่ยของธนาคารพาณิชย์ในกรุงเทพมหานคร (2545-ปัจจุบัน)","report_uoq_name_eng":"(Unit : Baht / 1 Unit of Foreign Currency)","report_uoq_name_th":"(หน่วย : บาท ต่อ 1 หน่วยเงินตราต่างประเทศ)
# https://www.bot.or.th/Thai/Statistics/EconomicAndFinancial/Pages/API.aspx

url = \
    'https://iapi.bot.or.th/Stat/Stat-ReferenceRate/DAILY_REF_RATE_V1/'
querystring = {'start_period': '2017-08-12', 'end_period': '2017-09-01'}
headers = {'api-key': 'U9G1L457H6DCugT7VmBaEacbHV9RX0PySO05cYaGsm'}
response = requests.request('GET', url, headers=headers, params=querystring)
print(response.text)
