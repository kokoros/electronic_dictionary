  1.创建数据库
    create database dict default charset=utf8;
  2.创建用户表
    create table user(id int primary key auto_increment,
    name varchar(32) not null,passwd varchar(16) default '000000'
    )default charset=utf8;
  3.创建历史记录表
  create table hist(
      id int primary key auto_increment,
      name varchar(32) not null,
      word varchar(32) not null,
      time varchar(64)
  )default charset=utf8;
  4.创建单词表
  create table words (
      id int primary key auto_increment,
      word varchar(32),
      mean text
  )default charset=utf8;