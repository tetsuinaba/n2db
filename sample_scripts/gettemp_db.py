import os
import sys
import time
sys.path.append(os.pardir)

# NASCO-FACはNASCORX_System-masterまでpath通ってる.
# だからこう書かないとダメっぽい
import n2db
db = n2db.n2db.n2db()
db.authorize(json='credentials_n2db.json')

import NASCORX_System
IP1 = '192.168.100.104'
IP2 = '192.168.100.105'
tr71w = NASCORX_System.device.TR71W.tr71w(IP=IP1)
tr72w = NASCORX_System.device.TR72W.tr72w(IP=IP2)

def get_temp():
    t = []
    t1 = tr71w.temp()
    temp, hum = tr72w.measure()
    t.append(t1[0])
    t.append(temp[1])
    t.append(hum[1])
    return t

while True:
    data = []
    for i in range(10):
        time.sleep(5)
        ikuta = []
        # get data
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        temp = get_temp()
        ikuta.append(timestamp)
        ikuta.extend(temp)
        data.append(ikuta)
        print(data)
        # wait for next measurement

    # upload to DB
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    db.refresh()
    db.INSERT(pjt='NASCORX', table='Amb', data=data)
    print(time.strftime('%Y-%m-%d %H:%M:%S'))
    print('INSERT')

