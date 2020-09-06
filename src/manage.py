# -*- coding: UTF-8 -*-

import pymysql,json,time
from flask import Flask, render_template, request, jsonify
import traceback
import os,sys
import random_code
sys.path.append("./")

app = Flask(__name__)



# 页面元素######################################################
# 预约管理平台
@app.route('/')
def pf():
    return render_template('/platform/platform.html')

# 用户
@app.route('/user')
def user():
    return render_template('/user/user.html')

# 接口#平台部分###################################################
# 增加会议室
@app.route('/add-conference',methods=['POST'])
def add_conference():
    id = request.form.get('id')
    floor = request.form.get('floor')
    roomNumber = request.form.get('room_number')
    seatsNumber = request.form.get('seats_number')
    cursor = db.cursor()
    sql = "INSERT INTO conference_information(ID,floor,room,seats) VALUES (%s, %s, %s, %s);"
    value = (id,floor,roomNumber,seatsNumber)
    msg = {}
    try:
        cursor.execute(sql, value)
        db.commit()
        msg['state'] = "succeed"
        msg['message'] = "成功增加会议室"
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    sql = "INSERT INTO order_manage(ID,week,enable_time,weekid) VALUES (%s, %s, %s,%s);"
    value =((id,'星期一','08:00-20:00',id+'1'),
            (id,'星期二','08:00-20:00',id+'2'),
            (id,'星期三','08:00-20:00',id+'3'),
            (id,'星期四','08:00-20:00',id+'4'),
            (id,'星期五','08:00-20:00',id+'5'),
            (id,'星期六','08:00-20:00',id+'6'),
            (id,'星期日','08:00-20:00',id+'7'),)
    msg = {}
    try:
        cursor.executemany(sql, value)
        db.commit()
        msg['state'] = "succeed"
        msg['message'] = "成功增加会议室"
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    cursor.close()
    return json.dumps(msg)

# 显示会议室信息
@app.route('/show-informations',methods=['POST'])
def show_informations():
    cursor = db.cursor()
    sql = "SELECT * from conference_information;"
    msg = {}
    try:
        cursor.execute(sql)
        data=cursor.fetchall()       
        msg['state'] = "succeed"
        msg['data'] = data
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    cursor.close()
    return json.dumps(msg)

# 获取指定会议室的信息
@app.route('/get-room-information',methods=['POST'])
def get_room_information():
    id = request.form.get('id')
    cursor = db.cursor()
    sql = "SELECT * from conference_information WHERE ID = %s;"
    value = (id)
    msg = {}
    try:
        cursor.execute(sql, value)
        data1=cursor.fetchall()       
        msg['state'] = "succeed"
        msg['data1'] = data1
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    sql = "SELECT * from order_manage WHERE ID = %s;"
    value = (id)
    try:
        cursor.execute(sql, value)
        data2=cursor.fetchall()       
        msg['state'] = "succeed"
        msg['data2'] = data2
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    cursor.close()
    return json.dumps(msg)

# 修改指定会议室信息
@app.route('/change-information',methods=['POST'])
def change_information():
    oid = str(request.form.get('oid'))
    nid = str(request.form.get('nid'))
    floor = request.form.get('floor')
    roomNumber = request.form.get('room_number')
    seatsNumber = request.form.get('seats_number')
    timePeriod = request.form.get('time_period')
    timePeriod = json.loads(timePeriod)
    cursor = db.cursor()
    sql = "UPDATE conference_information SET ID=%s,floor=%s,room=%s,seats=%s WHERE ID=%s;"
    value = (nid,floor,roomNumber,seatsNumber,oid)
    print(value)
    msg={}
    try:
        cursor.execute(sql, value)  
        msg['state'] = "succeed"
        msg['message'] = "succeed"
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    sql = "UPDATE order_manage SET enable_time=%s WHERE weekid = %s;"
    for num in range(0,6):
        value = (timePeriod[str(num)],oid+str(num+1))
        try:
            cursor.execute(sql, value)                      
        except Exception as e:
            db.rollback()
            print(str(e))
    db.commit() 
    cursor.close()
    return json.dumps(msg)

# 查看所有预约信息
@app.route('/get-order-informations',methods=['POST'])
def get_order_information():
    cursor = db.cursor()
    sql = "SELECT * FROM order_information;"
    msg={}
    try:
        cursor.execute(sql)  
        data=cursor.fetchall()       
        msg['state'] = "succeed"
        msg['data'] = data
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    db.commit() 
    cursor.close()
    return json.dumps(msg)

# 接口#用户部分###################################################
# 用户预约
@app.route('/order-conference',methods=['POST'])
def order_conference():
    id = request.form.get('id')
    date = request.form.get('date')
    start = request.form.get('start')
    end = request.form.get('end')
    name = request.form.get('name')
    range = request.form.get('timerange')
    wid = str(request.form.get('wid'))
    print(wid)
    orderid = random_code.generate_random_str(8)
    cursor = db.cursor()
    sql = "INSERT INTO order_information(ID,date,start,end,user,orderid) VALUES (%s,%s,%s,%s,%s,%s);"
    value = (id,date,start,end,name,orderid)
    msg={}
    try:
        cursor.execute(sql, value)  
        msg['state'] = "succeed"
        msg['message'] = "succeed"
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    sql1 = "UPDATE order_manage SET enable_time=%s WHERE weekid = %s;"
    value1 = (range,wid)
    msg={}
    try:
        cursor.execute(sql1, value1)  
        msg['state'] = "succeed"
        msg['message'] = "succeed"
    except Exception as e:
        db.rollback()
        msg['state'] = "failed"
        msg['message'] = str(e)
        print(str(e))
    db.commit() 
    cursor.close()
    return json.dumps(msg)




# 返回页面元素#平台部分###################################################
@app.route('/conference-add.html')
def ca():
    return render_template('/platform/conference-add.html')


@app.route('/conference-list1.html')
def cl1():
    return render_template('/platform/conference-list1.html')


@app.route('/details1.html')
def d1():
    return render_template('/platform/details1.html')


@app.route('/verification-list.html')
def vl():
    return render_template('/platform/verification-list.html')


@app.route('/welcome1.html')
def w1():
    return render_template('/platform/welcome1.html')

# 返回页面元素#用户部分###################################################
@app.route('/conference-list2.html')
def cl2():
    return render_template('/user/conference-list2.html')


@app.route('/details2.html')
def d2():
    return render_template('/user/details2.html')


@app.route('/order-room.html')
def oroom():
    return render_template('/user/order-room.html')

@app.route('/search-conference.html')
def sc():
    return render_template('/user/search-conference.html')


@app.route('/welcome2.html')
def w2():
    return render_template('/user/welcome2.html')


if __name__ == '__main__':
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                     passwd='123456', db='conferenceSys', charset='utf8')
    app.run(debug=True)
