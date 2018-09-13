#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/4/15

"""
    desc:pass
"""


class _Constants(object):
    # mysql配置
    HOST_NAME = "192.168.0.52"
    TEST_HOST_NAME = "127.0.0.1"
    DATABASE_USER_NAME = "greg"
    DATABASE_USER_PASSWORD = "Droi*#2018"
    DATABASE_CHARSET = "utf8"
    # 数据库信息
    DATABASE_NAME = "things"
    TABLE_NAME = "things"

    ITEM_ID = "_id"
    ITEM_CATEGORY = "category"
    ITEM_BRAND = "brand"
    ITEM_NAME = "name"
    ITEM_PRICE = "price"
    ITEM_IMG_URL = "imgurl"

    RECOMMEND_ITEM_NUM = 5

    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


import sys

sys.modules[__name__] = _Constants()

if __name__ == '__main__':
    pass
