# -*- coding:utf-8 -*-
import sys
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')


class DatabaseHelper():
    datas = [[u'\u70df', u'\u4e2d\u534e', u'\u8f6f\u4e2d\u534e', u'65\n'],
             [u'\u70df', u'\u4e2d\u534e', u'\u786c\u4e2d\u534e', u'45\n'],
             [u'\u70df', u'\u5357\u4eac', u'\u5357\u4eac\u4e5d\u4e94\u4e4b\u5c0a', u'100\n'],
             [u'\u70df', u'\u5357\u4eac', u'\u5357\u4eac\u8f6f\u4e5d\u4e94', u'100\n'],
             [u'\u70df', u'\u5357\u4eac', u'\u5357\u4eac\u4e94\u661f', u'20\n'],
             [u'\u70df', u'\u5357\u4eac', u'\u5357\u4eac\u7cbe\u54c1', u'22\n'],
             [u'\u70df', u'\u5229\u7fa4', u'\u5229\u7fa48mg\u65b0\u7248', u'14\n'],
             [u'\u70df', u'\u5229\u7fa4', u'\u5229\u7fa4\u65b0\u7248', u'14\n'],
             [u'\u70df', u'\u5229\u7fa4', u'\u5229\u7fa4\u8f6f', u'15\n'],
             [u'\u70df', u'\u5229\u7fa4', u'\u5229\u7fa4\u957f\u5634', u'22\n'],
             [u'\u70df', u'\u7ea2\u53cc\u559c', u'\u7ea2\u53cc\u559c\u9f99\u51e4', u'9\n'],
             [u'\u70df', u'\u7ea2\u53cc\u559c', u'\u7ea2\u53cc\u559c\u8f6f', u'5\n'],
             [u'\u70df', u'\u7ea2\u53cc\u559c', u'\u7ea2\u53cc\u559c\u786c', u'3\n'],
             [u'\u70df', u'\u957f\u767d\u5c71', u'\u957f\u767d\u5c71\u539f\u5473', u'55\n'],
             [u'\u70df', u'\u957f\u767d\u5c71', u'\u957f\u767d\u5c715mg', u'33\n'],
             [u'\u70df', u'\u957f\u767d\u5c71', u'\u957f\u767d\u5c71\u786c\u7ea2', u'8\n'],
             [u'\u70df', u'\u957f\u767d\u5c71', u'\u957f\u767d\u5c71\u8f6f\u7ea2', u'11\n'],
             [u'\u70df', u'\u957f\u767d\u5c71', u'\u957f\u767d\u5c71\u9e3f\u8fd0', u'16\n'],
             [u'\u70df', u'\u8299\u84c9\u738b', u'\u8299\u84c9\u738b\u786c', u'25\n'],
             [u'\u70df', u'\u8299\u84c9\u738b', u'\u8299\u84c9\u738b\u94bb\u77f3', u'100\n'],
             [u'\u70df', u'\u8299\u84c9\u738b', u'\u8299\u84c9\u738b\u8f6f\u84dd', u'60\n'],
             [u'\u70df', u'\u8299\u84c9\u738b', u'\u8299\u84c9\u738b\u786c\u7ec6\u652f', u'26\n'],
             [u'\u70df', u'\u7389\u6eaa', u'\u7389\u6eaa\u786c\u548c\u8c10', u'42\n'],
             [u'\u70df', u'\u7389\u6eaa', u'\u7389\u6eaa\u8f6f\u548c\u8c10', u'42\n'],
             [u'\u70df', u'\u7389\u6eaa', u'\u7389\u6eaa\u786c\u91d1\u9ec4', u'24\n'],
             [u'\u70df', u'\u7389\u6eaa', u'\u7389\u6eaa\u8f6f', u'23\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c\u96c5\u9999\u91d1', u'16\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c\u541b\u4e34\u5929\u4e0b', u'230\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c\u5927\u5e86', u'100\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c\u65b0\u96c5\u97f5', u'26\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c\u786c\u84dd', u'20\n'],
             [u'\u70df', u'\u9ec4\u9e64\u697c', u'\u9ec4\u9e64\u697c1916', u'100\n'],
             [u'\u6c34', u'\u519c\u592b\u5c71\u6cc9', u'\u519c\u592b\u5c71\u6cc9380ml', u'1.5\n'],
             [u'\u6c34', u'\u519c\u592b\u5c71\u6cc9', u'\u519c\u592b\u5c71\u6cc9550ml', u'2\n'],
             [u'\u6c34', u'\u519c\u592b\u5c71\u6cc9', u'\u519c\u592b\u5c71\u6cc91.5L', u'3.5\n'],
             [u'\u6c34', u'\u519c\u592b\u5c71\u6cc9', u'\u519c\u592b\u5c71\u6cc95L', u'8.5\n'],
             [u'\u6c34', u'\u6021\u5b9d', u'\u6021\u5b9d350ml', u'1.5\n'],
             [u'\u6c34', u'\u6021\u5b9d', u'\u6021\u5b9d555ml', u'2\n'],
             [u'\u6c34', u'\u6021\u5b9d', u'\u6021\u5b9d1.555L', u'3.5\n'],
             [u'\u6c34', u'\u6021\u5b9d', u'\u6021\u5b9d4.5L', u'8\n'],
             [u'\u6c34', u'\u767e\u5c81\u5c71', u'\u767e\u5c81\u5c71348ml', u'2\n'],
             [u'\u6c34', u'\u767e\u5c81\u5c71', u'\u767e\u5c81\u5c71570ml', u'3\n'],
             [u'\u6c34', u'\u767e\u5c81\u5c71', u'\u767e\u5c81\u5c711L', u'5\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u888b\u88c5\u7ea2\u70e7\u725b\u8089\u9762', u'2.8\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u4e94\u8fde\u5305\u7ea2\u70e7\u725b\u8089\u9762', u'12.5\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u6876\u88c5\u7ea2\u70e7\u725b\u8089\u9762', u'4\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u888b\u88c5\u8001\u575b\u9178\u83dc\u725b\u8089\u9762', u'2.8\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u4e94\u8fde\u5305\u8001\u575b\u9178\u83dc\u725b\u8089\u9762', u'12.8\n'],
             [u'\u65b9\u4fbf\u9762', u'\u5eb7\u5e08\u5085',
              u'\u5eb7\u5e08\u5085\u6876\u88c5\u8001\u575b\u9178\u83dc\u725b\u8089\u9762', u'4']]

    def createDatabase(self):
        conn = sqlite3.connect('things.db')
        print("Opened database successfully");
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS things
               (_id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
               category         TEXT    NOT NULL,
               brand            TEXT    NOT NULL,
               name             TEXT    NOT NULL,
               price            INTEGER);''')
        print("Table created successfully");
        conn.commit()
        conn.close()

    def insertData(self):
        conn = sqlite3.connect('things.db')
        print("Opened database successfully")
        cursor = conn.cursor()

        with open("simple_things.csv", 'r') as file:
            items = file.readlines()[0].split('\r')
            for item in items:
                item = item.decode('utf-8')
                (category, brand, name, price) = item.split(',')
                print(category, brand, name, price,)
                cursor.execute("INSERT INTO things(category, brand, name, price) VALUES (?, ?, ?, ?)",
                               [category, brand, name, price])
        print("Records created successfully")

        conn.commit()
        conn.close()

    def calculatePrice(self, thing, num):
        price = '1'
        # conn = sqlite3.connect('things.db')
        # c = conn.cursor()
        # cursor = c.execute("SELECT price  from things where name = '" + thing + "'");
        # item = cursor.fetchall()[0]
        # conn.close()
        # if item:
        #     price = item[0]
        for data in self.datas:
            if thing == data[2]:
                price = data[3]
                break

        return str(num * int(price))


def calculatePrice(thing, num):
    conn = sqlite3.connect('things.db')
    c = conn.cursor()
    cursor = c.execute("SELECT price  from things where name = '" + thing + "'");
    item = cursor.fetchall()[0]
    conn.close()
    price = 1
    if item:
        price = item[0]

    return str(num * int(price))


if __name__ == '__main__':
    helper = DatabaseHelper()
    # helper.createDatabase()
    # helper.insertData();

    price = helper.calculatePrice("硬中华",5)

    print (price)
    pass
