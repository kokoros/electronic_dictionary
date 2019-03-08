Project:electronic_dictionary(英汉电子词典)
===================

Getting Started
--------------
* 进入目录:   
     cd dict_list
* 按照sql_word.sql文件中sql语句,在数据库创建库和表  
* 打开dict.py文件,修改以下数据库设置:  
USER = 'root'  
PASSWD = '123456'   

* 将字典导入mysql数据库中,运行:  
  python3 dict.py


* 开启服务端:  
     python3 file_system_server.py IP地址 端口号
     ### 注:IP地址和端口号要自己在命令端输入  
     ### 如:可以输入
     python3 file_system_server.py 127.0.0.1 9553

Prerequisites(先决条件)
----------------------
* python3
* mysql
* pip3 pymysql 

Running the tests
-----------------
* 开启服务端后再开启客户端:
  python3 dict_server.py
* fork多进程模式,可以开启多个客户端

Function
------------------
英汉词典
>>功能:
1.注册登录注销  
    2.查询英文单词意思      
    3.查询历史记录   
    4.退出系统

Built With
------
* python3
* socket
* MySQL

Authors
-----------
* Koro
