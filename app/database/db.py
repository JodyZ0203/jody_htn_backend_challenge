import sqlite3
from flask import g

DATABASE = 'app/database/htn.db'

def get_db():
   #db = getattr(g, '_database', None)
    #if db is None:
     #   db = g._database = sqlite3.connect(DATABASE)
    #return db
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    connection = get_db()
    if args:
        results = connection.execute(query, args).fetchall()
    else:
        results = connection.execute(query).fetchall()
    connection.close()
    return [dict(ix) for ix in results][0] if one else [dict(ix) for ix in results]

def execute_query(query, args=(), one=False):
    connection = get_db()
    cur = connection.cursor()
    print(query)
    if args:
        cur.execute(query, args)
    else:
        cur.execute(query)
    connection.commit()
    connection.close()

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()