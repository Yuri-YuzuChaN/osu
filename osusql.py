import sqlite3
import os

def mysql(sql):
osupath = os.path.dirname(__file__)
    db = sqlite3.connect(f'{osupath}/osu.db')
    cursor = db.cursor()
    try:
        cursor.execute('''CREATE TABLE userinfo(
            id      INTEGER         PRIMARY KEY     NOT NULL,
            qqid    INTEGER         NOT NULL,
            osuid   INTEGER         NOT NULL,
            osuname TEXT            NOT NULL,
            osumod  INTEGER         NOT NULL
            )''')
        print('Table created successfully')
    except:
        pass
    for i in ['insert', 'update', 'delete']:
        if i in sql:
            try:
                cursor.execute(sql)
                db.commit()
                print('Operation successfully')
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
