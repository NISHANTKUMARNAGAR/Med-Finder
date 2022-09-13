import pymysql

def make_connection():
    conn=pymysql.connect(host="localhost",port=3306,user="root",db="medfinder",passwd="",autocommit=True)
    cur=conn.cursor()
    return cur

def checkphoto(email):
    cur=make_connection()
    cur.execute("select * from photodata where email='"+email+"'")
    n=cur.rowcount
    photo="no"
    if(n>0):
        row=cur.fetchone()
        photo=row[1]
    return photo

def getadminname(email):
    cur=make_connection()
    cur.execute("select * from admindata where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if(n>0):
        row=cur.fetchone()
        name=row[0]
    return name

def getmedicalname(email):
    cur=make_connection()
    cur.execute("select * from medicaldata where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if(n>0):
        row=cur.fetchone()
        name=row[0]
    return name
