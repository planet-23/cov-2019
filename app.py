from flask import Flask
from flask import render_template
from flask import request     #request.values.get()
from flask import jsonify
import utils
import update_data
import string
from jieba.analyse import extract_tags
app = Flask(__name__)


@app.route('/',methods=["post","get"])
def hello_world():
    return render_template("index.html")

@app.route('/get_sys_time',methods=["get","post"])
def get_tiem():
    dt=utils.get_sys_time()
    return dt

@app.route('/get_center1',methods=["get","post"])
def get_center1():
    res=utils.get_center1()
    return jsonify({"confirm":str(res[0]),"suspect":str(res[1]),"heal":str(res[2]),"dead":str(res[3])})

@app.route('/get_center2',methods=['get','post'])
def get_center2():
    datas = []
    res = utils.get_center2()
    for item in res:
        datas.append({"name": item[0], "value": str(item[1])})
    return jsonify({"data": datas})

@app.route('/get_left1',methods=['get','post'])
def get_left1():
    res = utils.get_left1()
    day, confirm, suspect, heal, dead = [], [], [], [], []

    for tup in res:
        day.append(tup[0].strftime("%m-%d"))
        confirm.append(tup[1])
        suspect.append(tup[2])
        heal.append(tup[3])
        dead.append(tup[4])
    return jsonify({"day": day, "confirm": confirm,
                    "suspect": suspect, "heal": heal,
                    "dead": dead})

@app.route('/get_left2',methods=['get','post'])
def get_left2():
    res = utils.get_left2()
    day, confirm_add, suspect_add= [], [], []
    for tup in res:
        day.append(tup[0].strftime("%m-%d"))
        confirm_add.append(tup[1])
        suspect_add.append(tup[2])
    print(confirm_add)
    return jsonify({"day": day, "confirm_add": confirm_add,
                    "suspect_add": suspect_add})

@app.route('/get_right1',methods=['get','post'])
def get_right1():
    res = utils.get_right1()
    city, confirm= [], []
    for tup in res:
        city.append(tup[0])
        confirm.append(str(tup[1]))
    return jsonify({"city": city, "confirm": confirm})

@app.route('/get_update',methods=['get','post'])
def get_update():
    update_data.rw_sql()
    return 200

@app.route('/get_right2',methods=['get','post'])
def get_right2():
    res = utils.get_right2()
    content = []
    for item in res:
        # 移除数字只取文本
        str = item[0].rstrip(string.digits)
        # 只取数据
        num = item[0][len(str):]
        # 从字符串中提取关键字
        str = extract_tags(str)
        for data in str:
            if not data.isdigit():
                content.append({"name": data, "value": num})
    return jsonify({"data": content})

if __name__ == '__main__':
    app.run()
    #get_right2()