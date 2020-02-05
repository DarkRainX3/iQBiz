from run import ConnectionObject
import urllib.request
import json

raw_data = ConnectionObject(table = 'currency_code').raw_data
api_key = []
for row in raw_data:
    api_key.append(row[1])
api_key = ','.join(api_key)

res_body = urllib.request.urlopen(f'https://api.exchangeratesapi.io/latest?base=USD&symbols={api_key}').read()
j = json.loads(res_body.decode("utf-8"))
rates = j['rates']

temp = ConnectionObject()
for i in rates.keys():
    temp.update_api_table(i, round(rates[i], 3))
   