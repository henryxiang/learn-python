#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:16:45 2015

@author: henryxiang
"""

import pymysql as db
from faker import Faker
from datetime import date

fake = Faker()

dbURL = {
    'host': 'localhost',
    'user': 'root',
    'db': 'test'
}
conn = db.connect(**dbURL)
# conn.isolation_level = None

c = conn.cursor()

sql = """
create table if not exists students (
    id integer primary key auto_increment,
    first_name varchar(50),
    last_name varchar(50),
    date_of_birth date,
    gpa decimal(3,2)
)
"""
c.execute(sql)

sql = """
insert into students (first_name, last_name, date_of_birth) values(%s, %s, %s)
"""
d1 = date(2000, 1, 1)
d2 = date(2006, 12, 31)
for i in range(20):
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_time_between('-20y', '-6y').strftime("%Y-%m-%d")
    # dob = fake.date_time_between('-20y', '-6y')
    c.execute(sql, (first_name, last_name, dob))
    conn.commit()

sql = "select * from students"
c.execute(sql)
for row in c.fetchall():
    print(row)

conn.close()
