# -*- coding:utf-8 -*-
import sys
import MySQLdb
import Constants

reload(sys)
sys.setdefaultencoding('utf8')


class MysqlDatabaseHelper(object):
    def __init__(self):
        pass

    def openDatabase(self):
        db = MySQLdb.connect(host=Constants.HOST_NAME, user=Constants.DATABASE_USER_NAME,
                             passwd=Constants.DATABASE_USER_PASSWORD, db=Constants.DATABASE_NAME,
                             charset=Constants.DATABASE_CHARSET)
        # print("Opened database successfully")
        return db

    def closeDatabase(self, db):
        # print("Closed database successfully")
        if db:
            db.close()

    def createDatabase(self):
        db = MySQLdb.connect(host=Constants.HOST_NAME, user=Constants.DATABASE_USER_NAME,
                             passwd=Constants.DATABASE_USER_PASSWORD,
                             charset=Constants.DATABASE_CHARSET)
        cursor = db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % Constants.DATABASE_NAME)
        db.close()

    def createTable(self):
        db = MySQLdb.connect(host=Constants.HOST_NAME, user=Constants.DATABASE_USER_NAME,
                             passwd=Constants.DATABASE_USER_PASSWORD, db=Constants.DATABASE_NAME,
                             charset=Constants.DATABASE_CHARSET)
        print("Opened database successfully")
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS %s(
                            %s INT UNSIGNED AUTO_INCREMENT,
                            %s VARCHAR(40) NOT NULL,
                            %s VARCHAR(40) NOT NULL,
                            %s VARCHAR(40) NOT NULL,
                            %s INT,
                            PRIMARY KEY (%s));''' % (
            Constants.TABLE_NAME, Constants.ITEM_ID, Constants.ITEM_CATEGORY, Constants.ITEM_BRAND, Constants.ITEM_NAME,
            Constants.ITEM_PRICE, Constants.ITEM_ID))
        print("Table created successfully")
        db.close()

    def insertData(self):
        db = MySQLdb.connect(host=Constants.HOST_NAME, user=Constants.DATABASE_USER_NAME,
                             passwd=Constants.DATABASE_USER_PASSWORD, db=Constants.DATABASE_NAME,
                             charset=Constants.DATABASE_CHARSET)
        print("Opened database successfully")
        cursor = db.cursor()

        with open("simple_things.csv", 'r') as file:
            items = file.readlines()
            for item in items:
                (category, brand, name, price) = item.split(',')
                print(category, brand, name, price,)
                sql = "INSERT INTO %s(%s, %s, %s, %s)" % (
                    Constants.TABLE_NAME, Constants.ITEM_CATEGORY, Constants.ITEM_BRAND, Constants.ITEM_NAME,
                    Constants.ITEM_PRICE)

                sql += " VALUES (%s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (category, brand, name, price))
                    db.commit()
                except:
                    db.rollback()
        db.close()

    def getPrice(self, thing):
        db = self.openDatabase()
        cursor = db.cursor()
        sql = "SELECT %s FROM %s WHERE name = '%s';" % (Constants.ITEM_PRICE, Constants.TABLE_NAME, thing)
        cursor.execute(sql);
        item = cursor.fetchone()
        if item:
            price = item[0]
        self.closeDatabase(db)
        return price;

    def recommendCategorys(self):
        db = self.openDatabase()
        cursor = db.cursor()
        sql = "SELECT DISTINCT %s FROM %s LIMIT %s;" % (
            Constants.ITEM_CATEGORY, Constants.TABLE_NAME, Constants.RECOMMEND_ITEM_NUM)
        cursor.execute(sql)
        items = cursor.fetchall()
        self.closeDatabase(db)
        return items

    def recommendBrands(self):
        db = self.openDatabase()
        cursor = db.cursor()
        sql = "SELECT DISTINCT %s FROM %s LIMIT %s;" % (
            Constants.ITEM_BRAND, Constants.TABLE_NAME, Constants.RECOMMEND_ITEM_NUM)
        cursor.execute(sql)
        items = cursor.fetchall()
        self.closeDatabase(db)
        return items

    def recommendThings(self):
        db = self.openDatabase()
        cursor = db.cursor()
        sql = "SELECT DISTINCT %s FROM %s LIMIT %s;" % (
            Constants.ITEM_NAME, Constants.TABLE_NAME, Constants.RECOMMEND_ITEM_NUM)
        cursor.execute(sql)
        items = cursor.fetchall()
        self.closeDatabase(db)
        return items


if __name__ == '__main__':
    helper = MysqlDatabaseHelper()
    # helper.createDatabase()
    # helper.createTable()
    # helper.insertData()

    thing = '软中华'
    price = str(5 * int(helper.getPrice(thing)))
    print (price)
    assert price == '325'
    print (helper.recommendCategorys())
    print (helper.recommendBrands())
    print (helper.recommendThings())
    pass
