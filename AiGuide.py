#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

import sys
import json
from droi.MySqlDatabaseHelper import MysqlDatabaseHelper as DbHelper
from dueros.Bot import Bot
from dueros.card.TextCard import TextCard
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.ListTemplate2 import ListTemplate2
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem

reload(sys)
sys.setdefaultencoding('utf8')


class AiGuide(Bot):
    TITLE = "智能导购"
    WELLCOM_TIPS = "欢迎进入智能导购"
    ICON_URL = "http://dbp-resource.gz.bcebos.com/ed4f7f94-fee0-cecf-344e-f4792d94406a/ai_guide_icon.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-09-06T06%3A07%3A01Z%2F-1%2F%2F16927c417355bb40cb810fe87afbcf2634f94a386781003d8ce93090fa036262"
    BODY_TEMPLATE1_TOKEN = "1e4750ff9eb44d3339e9af33ba2b071a"
    LIST_TEMPLATE1_TOKEN = "9db6240b1bc3794fbc4d6a2159467214"
    LIST_TEMPLATE2_TOKEN = "98a02ffa253f7d05c8c0e1bfdd62ae32"
    LIST_TEMPLATE_ITEM_TOKEN = "92f1478981a2ec1d1e3612c729de2b70"
    dbHelper = DbHelper()

    def __init__(self, request_data):
        super(AiGuide, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('buy_things', self.getTaxSlot)

    def launch_request(self):
        """
        打开调用名
        """
        self.wait_answer()
        content = self.WELLCOM_TIPS
        template = BodyTemplate1()
        template.set_title(self.TITLE)
        template.set_plain_text_content(content)
        template.set_background_image(self.ICON_URL)
        template.set_token(self.BODY_TEMPLATE1_TOKEN)
        renderTemplate = RenderTemplate(template)

        card = self.getCard(self.WELLCOM_TIPS)
        card.set_anchor(self.ICON_URL, self.TITLE)

        return self.getResponse(content, card, renderTemplate)

    def getTaxSlot(self):
        """
        获取槽位及逻辑处理
        """
        actionBuy = self.get_slots('buy')
        num = self.get_slots('sys.number')
        quantifier = self.get_slots('quantifier')
        thingsCategory = self.get_slots('things_caterory')
        thingsBrand = self.get_slots('things_brand')
        things = self.get_slots('things')

        if things:
            if not quantifier:
                self.nlu.ask('quantifier')
                content = r'请问你购买多少' + things + '?'
                renderTemplate = self.getBodyTemplate1(content)
                card = self.getCard(content)

                return self.getResponse(content, card, renderTemplate)
            else:
                if not num:
                    num = 1
                price = self.calculatePrice(things, num)
                contentTxt = "请您支付%s元" % price
                content = self.getReponseJson(contentTxt, num, price, things, thingsCategory, thingsBrand)
                outputSpeech = '<speak>请您支付<say-as type="number">%s</say-as>元</speak>' % price
                renderTemplate = self.getBodyTemplate1(content)
                card = self.getCard(content)

                return self.getResponse(contentTxt, card, renderTemplate, outputSpeech)
        else:
            if thingsBrand:
                self.nlu.ask('things')
                content = r'请问您购买' + thingsBrand + '的什么商品呢?'
                recommendThings = self.dbHelper.recommendThings()
                renderTemplate = self.getListTemplate(content, recommendThings)
                card = self.getListCard(content, recommendThings)

                return self.getResponse(content, card, renderTemplate)
            else:
                if thingsCategory:
                    self.nlu.ask('things_brand')
                    content = r'请问您购买%s的什么品牌呢?' % thingsCategory
                    recommendBrands = self.dbHelper.recommendBrands()
                    renderTemplate = self.getListTemplate(content, recommendBrands)
                    card = self.getListCard(content, recommendBrands)

                    return self.getResponse(content, card, renderTemplate)
                else:
                    self.nlu.ask('things_caterory')
                    content = r'请问您购买什么分类的商品呢?'
                    recommendCategorys = self.dbHelper.recommendCategorys()
                    renderTemplate = self.getListTemplate(content, recommendCategorys)
                    card = self.getListCard(content, recommendCategorys)
                    return self.getResponse(content, card, renderTemplate)

    def getCard(self, content):
        card = TextCard(content)
        return card

    def getListCard(self, content, datas):
        card = ListCard()
        #card.setContent(content)
        for data in datas:
            item = ListCardItem()
            item.set_title(data)
            # item.set_url("http://www.baidu.com")
            item.set_image(self.ICON_URL)
            #item.set_content(data)
            card.add_item(item)

        return card

    def getBodyTemplate1(self, content):
        template = BodyTemplate1()
        template.set_title(self.TITLE)
        template.set_plain_text_content(content)
        template.set_token(self.BODY_TEMPLATE1_TOKEN)
        renderTemplate = RenderTemplate(template)
        return renderTemplate

    def getListTemplate(self, content, items):
        template = ListTemplate2()
        template.set_token(self.LIST_TEMPLATE2_TOKEN)
        # template.set_background_image('')
        template.set_title(content)

        for item in items:
            template.add_item(self.getListTemplateItem(item))
        renderTemplate = RenderTemplate(template)
        return renderTemplate

    def getListTemplateItem(self, item):
        template = ListTemplateItem()
        template.set_token(self.LIST_TEMPLATE_ITEM_TOKEN)
        template.set_image(self.ICON_URL)
        template.set_plain_primary_text(item)
        #template.set_plain_secondary_text(item)
        return template

    def getResponse(self, content, card, renderTemplate, outputSpeech=None):
        if not card:
            card = self.getCard(content)

        return {
            'card': card,
            'directives': [renderTemplate],
            'reprompt': content,
            'outputSpeech': outputSpeech if outputSpeech != None else content
        }

    def getReponseJson(self, content, num, price, things, thingsCategory=None, thingsBrand=None):
        data = [{'content': content, 'num': num, 'price': price, 'things': things, 'thingsCategory': thingsCategory,
                 'thingsBrand': thingsBrand}]
        jsonstr = json.dumps(data)
        return jsonstr

    def calculatePrice(self, thing, num):
        price = self.dbHelper.getPrice(thing)
        if not price:
            price = 1

        return str(int(num) * float(price))

    def errorCallBack(self):
        def __call__(data):
            print (data)
