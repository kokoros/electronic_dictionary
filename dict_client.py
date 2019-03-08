#coding:utf-8
#dict client
'''网络电子词典'''

from socket import * 
import sys 
import getpass

#创建网络连接
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return 
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    #创建tcp套接字
    s = socket()
    #试图连接server
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print('Error:',e)
        return 
    #循环发送请求
    while True:
        print('''
        ----------welcome------------
        1-注册
        2-登录
        3-退出
        -----------------------------
        ''')
        try:
            cmd = int(input('请输入选项数字:'))
        except Exception as e:
            print('Error:',e)
            continue 
        if cmd not in [1,2,3]:
            print('请输入1-3的整数')
            continue 
        elif cmd == 1:
            do_register(s)
        elif cmd == 2:
            do_login(s)
        elif cmd == 3:
            s.send(b'E')
            sys.exit('Thanks')

#发送注册请求
def do_register(s):
    #循环输入
    while True:
        name = input('User:')
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Again:')
        #做用户名密码的基本判断
        if (' ' in name) or (' ' in passwd):
            print('用户名密码不能包含空格')
            continue
        if passwd != passwd1:
            print('两次输入密码不同,请重新输入')
            continue
        if (not name) or (not passwd):
            print('用户名密码不能为空,请重新输入')
            continue
        msg = "R %s %s"% (name,passwd)
        #发送注册请求
        s.send(msg.encode())
        #等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            print('register success!')
            #注册成功 进入二级界面
            login(s,name)
        elif data == 'EXISTS':
            print('用户已存在')
        else:
            print('注册失败')
        return
#发送登录请求
def do_login(s):
    name = input('User:')
    passwd = getpass.getpass()
    msg = "L %s %s" % (name,passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        print('Login success!')
        #进入二级界面的函数 记得还要传用户名
        login(s,name)
    else:
        print('Login fail')

#进入二级界面的函数
def login(s,name):
    while True:
        print('''
        ---------welcome %s----------
        1-查单词
        2-历史记录
        3-注销
        ------------------------------
        ''' % name)          
        try:
            cmd = int(input('请输入选项数字:'))
        except Exception as e:
            print('Error:',e)
            continue 
        if cmd not in [1,2,3]:
            print('请输入1-3的整数')
            continue 
        elif cmd == 1:
            do_query(s,name)
        elif cmd == 2:
            do_hist(s,name)
        elif cmd == 3:
            return   
#发送查询请求
def do_query(s,name):
    while True:
        word = input('请输入单词(输入##退出查词):')
        if word == '##':
            break 
        msg = "Q %s %s" % (name,word)
        s.send(msg.encode())
        #返回的可能是单词解释,也可能是找不到单词
        data = s.recv(2048).decode()
        print(data)
#发送查询历史记录请求
def do_hist(s,name):
    #发送用户名
    msg = "H %s" %name 
    s.send(msg.encode())
    #等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        #循环接受服务器发来的历史记录
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('您没有历史记录')


if __name__== '__main__':
    main()
    