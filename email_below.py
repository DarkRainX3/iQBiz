from run import ConnectionObject
import pandas as pd
import stmp

def send_email(address):
    server = smtplib.SMTP('smpt.gmail.com', 587, 'nhot2020@gmail', )

def get_managers_below():
    raw_data = ConnectionObject().raw_data
    stores_below = [i[0] for i in raw_data if i[2] < i[-1]]
    print(stores_below)
    raw_data = ConnectionObject('EMPLOYEES').raw_data
    for i in raw_data:
        if str(i[-1]) in stores_below and i[-2] == 'SM':
            manager_email.append(i[0])
        

get_managers_below()
