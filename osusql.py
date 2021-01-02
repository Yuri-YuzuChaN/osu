import pymysql
import json
import os

def mysql(sql):
    ''' 处理SQL语句 '''
    osupath = os.path.dirname(__file__)
    with open(f'{osupath}/config.json', encoding='utf-8') as d:
        jsondata = json.load(d)
        host = jsondata['sql_host']
        user = jsondata['sql_user']
        pwd = jsondata['sql_pwd']
        db = jsondata['sql_name']

    db = pymysql.Connect(host, user, pwd, db)
    cursor = db.cursor()
    for i in ['insert', 'update', 'delete']:
        if i in sql:
            try:
                cursor.execute(sql)
                db.commit()
                return True
            except:
                db.rollback()
        elif 'select' in sql:
            try :
                cursor.execute(sql)
                results = cursor.fetchall()
                if results:
                    return results
                else:
                    return False
            except:
                db.rollback()
    db.close()