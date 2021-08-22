#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/5 20:43
# @Author : Henry
import pymysql


class Db:
    def __init__(self, user, password, host, database, port=3306):
        self.conn = pymysql.connect(user=user, password=password,
                                    host=host, database=database, port=port)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def execute_sql(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def commit(self):
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


init_db = Db(user='root', password='root', host='localhost', database='first')


def print_menu():
    """打印菜单"""
    print('******* 菜单 ********')
    print('【1】: 添加图书')
    print('【2】: 修改图书')
    print('【3】: 删除图书')
    print('【4】: 查询图书')
    print('【5】: 图书列表')
    print('【6】: 出借图书')
    print('【7】: 归还图书')
    print('【8】: 退出')


class Books:

    def __init__(self):
        self.db = init_db

    def add_book(self):
        """添加"""
        print('************add book**********')
        name = input('input the book name: ')
        position = input('input the book position: ')
        if name and position:
            sql = 'insert into books(name, position) values("{}", "{}")'.format(name, position)
            self.db.execute_sql(sql)
            self.db.commit()
            print('add successfully')
        else:
            print('You should input name and position')
        again = input('input 1 to continue, or return to menu: ')
        if again == '1':
            self.add_book()

    def modify_book(self):
        """修改 """
        print('************modify book**********')
        book_id = input('input the book id: ')
        sql = 'select * from books where id = {}'.format(book_id)
        result = self.db.execute_sql(sql)
        if result:
            print(result[0])
            # 按回车传递的时空字符串，使用逻辑运算符
            name = input('input the book name: Enter to skip') or result[0]['name']
            position = input('input the book position: Enter to skip') or result[0]['position']
            # 执行一条update sql语句，需求说明输入回车时不进行更新， 那一般情况下需要判断输入的是否为空来进行sql语句执行
            # 如何简化代码，使之灵活？ 保持以下sql语句不变， 当用户输入为空时，如果获取到字段的原始数据，
            # 则填入以下sql语句执行，不会出现异常，也能保证更新操作。
            # 那我又要得到用户的输入，在其为空时又要拿到原始输入，则想到使用or逻辑运算符，利用其短路逻辑
            sql = 'update books set name = "{}", position = "{}" where id = {}'.format(name, position, book_id)
            self.db.execute_sql(sql)
            self.db.commit()
            print('update success')
        else:
            print('The book does not exist.')
        again = input('Want to modify book? 1 to continue')
        if again == '1':
            self.modify_book()

    def delete_book(self):
        """删除"""
        print('****** delete book*******')
        n = input('input the book id to delete:')
        enquiry = 'select * from books where id = {} '.format(n)
        if self.db.execute_sql(enquiry):
            sql = 'delete from books where id = {} '.format(n)
            confirm = input('input y to confirm')
            if confirm == 'y' or confirm == 'Y':
                self.db.execute_sql(sql)
                self.db.commit()
                print('delete successfully')
            else:
                print('cancel')
        else:
            print('No such book')
        again = input('Want to delete book? 1 to continue')
        if again == '1':
            self.delete_book()

    def query_book(self):
        print('****** query book*******')
        n = input('input the book id to query:')
        enquiry = 'select * from books where id = {} '.format(n)
        each = self.db.execute_sql(enquiry)
        if each:
            print(f'编号: {each[0]["id"]}', f'书名: {each[0]["name"]}', f'位置: {each[0]["position"]}',
                  f'状态: {each[0]["status"]}', f'借阅人: {each[0]["borrower"]}')
        else:
            print('No such book')
        again = input('Want to query book? 1 to continue')
        if again == '1':
            self.query_book()

    def book_list(self):
        sql = 'select * from books'
        result = self.db.execute_sql(sql)
        for each in result:
            print(f'编号: {each["id"]}', f'书名: {each["name"]}', f'位置: {each["position"]}',
                  f'状态: {each["status"]}', f'借阅人: {each["borrower"]}')

    def lend_book(self):
        print('****** lend book*******')
        n = input('input the book id to lend:')
        enquiry = 'select status from books where id = {} '.format(n)
        each = self.db.execute_sql(enquiry)
        if each:
            if each[0]['status'] == '在库':
                user = input('input the user:')
                sql = 'update books set status = "出借", borrower = "{}" where id ={}'.format(user, n)
                self.db.execute_sql(sql)
                self.db.commit()
                print('Lend successful')
            else:
                print('The book is not at library')
        else:
            print('No such Book')
        again = input('Want to lend book? 1 to continue')
        if again == '1':
            self.lend_book()

    def return_book(self):
        print('****** return book*******')
        n = input('input the book id to return:')
        enquiry = 'select status from books where id = {}'.format(n)
        each = self.db.execute_sql(enquiry)
        if each:
            if each[0]['status'] == '出借':
                sql = 'update books set status = "在库", borrower = "" where id ={}'.format(n)
                self.db.execute_sql(sql)
                self.db.commit()
                print('Return successful')
            else:
                print('The book is at library')
        else:
            print('No such Book')
        again = input('Want to return book? 1 to continue')
        if again == '1':
            self.return_book()

    def run(self):
        while True:
            print_menu()
            n = input('input the number: ')
            if n == '1':
                self.add_book()
            elif n == '2':
                self.modify_book()
            elif n == '3':
                self.delete_book()
            elif n == '4':
                self.query_book()
            elif n == '5':
                self.book_list()
            elif n == '6':
                self.lend_book()
            elif n == '7':
                self.return_book()
            elif n == '8':
                print('Over')
                break
            else:
                print('please input the correct number')


if __name__ == '__main__':
    book = Books()
    book.run()
