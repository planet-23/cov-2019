import requests
import pymysql
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import json
import time

def get_hot():           #获取热搜
        url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1#tab2"
        brower = Chrome()
        brower.get(url)
        html = brower.page_source
        hotdata = []
        btn = brower.find_element_by_xpath('//*[@id="ptab-2"]/div[1]/div/p/a')
        btn.click()
        time.sleep(1)

        btn = brower.find_element_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/div')
        btn.click()
        time.sleep(1)
        content = brower.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
        for item in content:
            hotdata.append(item.text)
        return hotdata
def linkconn():
    try:
        conn=pymysql.connect(host="127.0.0.1",
                             port=3306,
                             user="root",
                             password="heyong728350858"
                             ,database="cov",charset="utf8")
        curs=conn.cursor()
        return conn,curs
    except:
        print("连接失败")
def closeconn(conn,curs):
    try:
        conn.close()
        curs.close()
    except:
        print("关闭失败")




def get_history():
    #https://view.inews.qq.com/g2/getOnsInfo?name=disease_other
    url="https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    jsondata=requests.get(url)
    jsondata=jsondata.text
    datas=json.loads(jsondata)
    datas=json.loads(datas["data"])
    history=dict()
    for data in datas["chinaDayList"]:
        dt = '2020.' + data['date']
        tup = time.strptime(dt, "%Y.%m.%d")
        dt = time.strftime("%Y-%m-%d", tup)
        history[dt]={"confirm":data["confirm"],"suspect":data["suspect"],"heal":data["heal"],"dead":data["dead"]}
    for data in datas["chinaDayAddList"]:
        dt = '2020.' + data['date']
        tup = time.strptime(dt, "%Y.%m.%d")
        dt = time.strftime("%Y-%m-%d", tup)
        history[dt].update({"confirm_add": data["confirm"], "suspect_add": data["suspect"], "heal_add": data["heal"],
                       "dead_add": data["dead"]})
    return history


def get_details():
    # https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    jsondata = requests.get(url)
    jsondata = jsondata.text
    datas = json.loads(jsondata)
    datas = json.loads(datas["data"])
    updata_Time=datas['lastUpdateTime']
    details=[]

    for item in datas['areaTree'][0]['children']:
        province=item['name']
        for city in item['children']:
            details.append((updata_Time,province,
                            city["name"],
                            city['total']['confirm'],
                            city['today']['confirm'],
                            city['total']['heal'],
                            city['total']['dead']))
    return details

def rw_sql():
    history=get_history()
    details=get_details()
    hot=get_hot()
    conn, curs = linkconn()
    sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for k, v in history.items():
        sql_query="select * from history where ds=%s"
        curs.execute(sql_query,k)
        if not curs.fetchone():
            curs.execute(sql, (k, v.get("confirm"), v.get("confirm_add"),
                               v.get("suspect"), v.get("suspect_add"),
                               v.get("heal"), v.get("heal_add"),
                               v.get("dead"), v.get("dead_add")))
            conn.commit()
    dt = time.strftime("%Y-%m-%d %X")

    sql = "insert into hotsearch(dt,content) values (%s,%s)"
    try:
        for data in hot:
            curs.execute(sql, (dt, data))
            conn.commit()
    except:
        pass

    sql = 'insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)'
    sql_query = 'select %s=(select update_time from details order by id desc limit 1)'
    curs.execute(sql_query, details[0][0])
    if not curs.fetchone()[0]:
            for item in details:
                curs.execute(sql, item)
                conn.commit()
    else:
            print("已经是最新数据，不需要更新！")

    closeconn(conn, curs)

if __name__=="__main__":
    rw_sql()