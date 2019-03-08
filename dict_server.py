#coding:utf-8
#dict_server.py
'''网络电子词典
dict project
'''

from socket import *
import pymysql
import os,sys 
import time 
import signal 

#设置全局变量 让用户自己从命令行输入网络地址和端口号
if len(sys.argv) < 3:
    print('''Start as:
    python3 dict_server.py 0.0.0.0 9553
    ''')
    #退出进程
    sys.exit(0)

HOST = sys.argv[1]
PORT = int(sys.argv[2])
ADDR = (HOST,PORT)
DICT_TEXT = "./dict.txt"

#建立网络连接
def main():
    #连接数据库
    conn = pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    sockfd = socket()
    #重置端口
    # sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定网络地址
    sockfd.bind(ADDR)
    #设置为监听套接字
    sockfd.listen(5)
    #处理僵尸进程 忽略信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    #循环等待client连接
    while True:
        try:
            connfd,addr = sockfd.accept()
            print('Connect from:',addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('server exit')
        except Exception as e:
            print('Error:',e)
            continue
        #创建子进程
        pid = os.fork()
        #子进程
        if pid == 0:
            sockfd.close()
            #传入c套接字和数据库
            do_child(connfd,conn)
            sys.exit()
        #父进程或未创建进程成功,关闭c后继续循环
        else:
            connfd.close()

#处理client请求
def do_child(c,db):
    #循环接受client请求
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        #如果客户端退出
        if not data or data[0] == 'E':
            c.close()
            #退出子进程
            sys.exit()
        #如果接到了注册请求
        elif data[0] == 'R':
            do_register(c,db,data)
        #如果接到了登录请求
        elif data[0] == 'L':
            do_login(c,db,data)
        #如果接到了查词请求
        elif data[0] == 'Q':
            do_query(c,db,data)
        #如果接到了查询历史记录请求
        elif data[0] == 'H':
            do_hist(c,db,data)

#处理注册请求
def do_register(c,db,data):
    l = data.split(' ')
    #剥离出用户名和密码
    name = l[1]
    passwd = l[2]
    #建立游标 先判断是否重名
    cursor = db.cursor()
    sql = '''select * from user where name = '%s'
    ''' % name 
    #执行语句
    cursor.execute(sql)
    #只读第一项 没找到会返回None
    r = cursor.fetchone()
    #如果r读出了数据 证明数据库中有这个名字了 
    if r != None:
        c.send(b'EXISTS')
        return
    #如果r为None 数据库插入语句
    else:
        sql = '''insert into user(name,passwd) values("%s","%s")''' % (name,passwd)
        try:
            cursor.execute(sql)
            #连接对象提交commit
            db.commit()
            c.send(b'OK')
        except:
            db.rollback()
            #送随意字符
            c.send(b'FAIL')
#处理client登录请求
def do_login(c,db,data):
    l = data.split(' ')
    #剥离出用户名和密码
    name = l[1]
    passwd = l[2]
    #建立游标 查看用户名和密码在不在数据库中
    cursor = db.cursor()
    sql = '''select * from user where name = "%s" and passwd = "%s"
    ''' % (name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r == None:
        c.send(b'FAIL')
    else:
        c.send(b'OK')
#处理client查词请求
def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    #插入历史记录
    #开启游标
    cursor = db.cursor()
    #当前时间
    tm = time.ctime()
    sql = '''insert into hist(name,word,time) values ('%s','%s','%s') 
    ''' % (name,word,tm)
    #试图插入数据
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    #单词本查找
    f = open(DICT_TEXT)
    for line in f:
        #提取单词
        tmp = line.split(' ')[0]
        if tmp > word:
            break 
        elif tmp == word:
            c.send(line.encode())
            f.close()
            return 
    #防止用户输入zzzz
    c.send('没有找到该单词'.encode())
    f.close()
#处理client查询历史记录请求
def do_hist(c,db,data):
    #获取用户名
    name = data.split(' ')[1]
    #开启游标
    cursor = db.cursor()
    sql = '''select * from hist where name = '%s' order by id desc limit 10
    ''' % name 
    cursor.execute(sql)
    #取得所有查询结果
    r = cursor.fetchall()
    if not r:
        #送的信息随意
        c.send(b'Fail')
        return
    else:
        c.send(b'OK')
        time.sleep(0.1)
        #r是一个元组套元祖
    for i in r:
        #取出name word time三个字段
        msg = "%s   %s    %s" % (i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    c.send(b'##')


if __name__ == '__main__':
    main()
