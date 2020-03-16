import time
import pymysql
def get_sys_time():
    dt = time.strftime("%Y-%m-%d %X")
    return dt

def link_conn():
    conn=pymysql.connect(
        host='127.0.0.1', port=3306,
        user='root', password='heyong728350858',
        database='cov', charset='utf8'
    )
    curs=conn.cursor()
    return conn,curs

def close_conn(conn,curs):
    conn.close()
    curs.close()

def sele_conn(curs,sql,*args):
    curs.execute(sql,args)
    res=curs.fetchall()
    return res

def get_center1():
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal)," \
          "sum(dead) " \
          "from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    conn,curs=link_conn()
    res=sele_conn(curs,sql)
    close_conn(conn,curs)
    return res[0]

def get_center2():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    conn, curs = link_conn()
    res = sele_conn(curs, sql)
    close_conn(conn, curs)
    return res

def get_left1():
    sql = "select ds,confirm,suspect,heal,dead from history"
    conn, curs = link_conn()
    res = sele_conn(curs, sql)
    close_conn(conn, curs)
    return res

def get_left2():
    sql="select ds,confirm_add,suspect_add from history"
    conn, curs = link_conn()
    res = sele_conn(curs, sql)
    close_conn(conn, curs)
    return res

def get_right1():
    sql='SELECT city,confirm FROM ' \
          '(select city,confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province not in ("湖北","北京","上海","天津","重庆") ' \
          'union all ' \
          'select province as city,sum(confirm) as confirm from details  ' \
          'where update_time=(select update_time from details order by update_time desc limit 1) ' \
          'and province in ("北京","上海","天津","重庆") group by province) as a ' \
          'ORDER BY confirm DESC LIMIT 5'
    conn, curs = link_conn()
    res = sele_conn(curs, sql)
    close_conn(conn, curs)
    return res

def get_right2():
    sql="select content from hotsearch order by id desc"
    conn, curs = link_conn()
    res = sele_conn(curs, sql)
    close_conn(conn, curs)
    return res

if __name__=="__main__":
    get_right2()