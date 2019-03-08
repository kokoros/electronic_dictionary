#coding=utf-8
'''一个把单词表插入数据库的小程序'''
import pymysql 

HOST = 'localhost'
USER = 'root'
PASSWD = '123456'
DBNAME = 'dict' 

#建立数据库连接
conn = pymysql.connect(HOST,USER,PASSWD,DBNAME)
#获取游标对象
cursor = conn.cursor()
#打开单词文件
f = open('./dict.txt')
#直接每行开读,因为文件可迭代,line就是每一行的内容
for line in f:
    tmp = line.split(' ')
    #剥离出单词和意思
    word = tmp[0]
    #去除意思前面的空格
    mean = ' '.join(tmp[1:]).strip()
    #执行sql语句
    sql = '''insert into words(word,mean) values ("%s","%s")''' % (word,mean)
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        conn.rollback()
f.close()
cursor.close()
conn.close()