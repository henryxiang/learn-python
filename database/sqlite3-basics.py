#/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:16:45 2015

@author: henryxiang
"""

import sqlite3
from faker import Factory
from datetime import date

fake = Factory.create()

conn = sqlite3.connect('example.db')
conn.isolation_level = None

c = conn.cursor()

sql = """
    create table students (
        student_id integer primary key,
        first_name varchar(50),
        last_name varchar(50),
        date_of_birth date,
        gpa number(3,2)
    )
"""
c.execute(sql)

sql = "insert into students (first_name, last_name, date_of_birth) values(?, ?, ?)"
d1 = date(2000,1,1)
d2 = date(2006,12,31)
for i in range(20):
    c.execute(sql, \
    (fake.first_name(), fake.last_name(), fake.date_time_between_dates(d1, d2).date().isoformat()))
conn.commit()

sql = "select * from students"
for row in c.execute(sql):
    print(row)
    
conn.close()

    