# !/usr/bin/env python

import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='sandbox')

cur = conn.cursor()
cur.execute("SELECT * FROM users")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()