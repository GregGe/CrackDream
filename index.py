#!/usr/bin/env python2
# -*- encoding=utf-8 -*-


import sys
import json
# import sqlite3
from dueros.card import TextCard
from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1

reload(sys)
sys.setdefaultencoding('utf8')


class CrackDream(Bot):
    TITLE = "周公解梦"
    WELLCOM_TIPS = "欢迎进入智能导购"
    ICON_URL = "http://dbp-resource.gz.bcebos.com/ed4f7f94-fee0-cecf-344e-f4792d94406a/ai_guide_icon.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-09-06T06%3A07%3A01Z%2F-1%2F%2F16927c417355bb40cb810fe87afbcf2634f94a386781003d8ce93090fa036262"
    BODY_TEMPLATE1_TOKEN = "1e4750ff9eb44d3339e9af33ba2b071a"
    LIST_TEMPLATE1_TOKEN = "9db6240b1bc3794fbc4d6a2159467214"
    LIST_TEMPLATE2_TOKEN = "98a02ffa253f7d05c8c0e1bfdd62ae32"
    LIST_TEMPLATE_ITEM_TOKEN = "92f1478981a2ec1d1e3612c729de2b70"

    def __init__(self, request_data):
        super(CrackDream, self).__init__(request_data)
        self.add_launch_handler(self.launch_request)
        self.add_intent_handler('buy_things', self.getTaxSlot)

    def launch_request(self):
        """
        打开调用名
        """
        self.wait_answer()
        template = BodyTemplate1()
        template.set_title('智能导购')
        template.set_plain_text_content('欢迎进入智能导购')
        template.set_background_image(
            'http://dbp-resource.gz.bcebos.com/ed4f7f94-fee0-cecf-344e-f4792d94406a/ai_guide_icon.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-09-06T06%3A07%3A01Z%2F-1%2F%2F16927c417355bb40cb810fe87afbcf2634f94a386781003d8ce93090fa036262')
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        renderTemplate = RenderTemplate(template)
        card = self.getCard('欢迎进入智能导购');
        return {
            'card': card,
            'directives': [renderTemplate],
            'outputSpeech': r'欢迎进入智能导购'
        }

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
                renderTemplate = self.getTemplate(content)

                return self.getTemplateAnswer(renderTemplate, content)
            else:
                if not num:
                    num = 1

                price = self.calculatePrice(things, num)
                contentTxt = "请您支付%s元" % price
                content = self.getReponseJson(contentTxt, num, price, things, thingsCategory, thingsBrand)
                outputSpeech = '<speak>请您支付<say-as type="number">%s</say-as>元</speak>' % price
                renderTemplate = self.getTemplate(content)
                return self.getTemplateAnswer(renderTemplate, contentTxt, outputSpeech)
        else:
            if thingsBrand:
                self.nlu.ask('things')
                content = r'请问您购买' + thingsBrand + '的什么商品呢?'
                renderTemplate = self.getTemplate(content)

                return self.getTemplateAnswer(renderTemplate, content)
            else:
                if thingsCategory:
                    self.nlu.ask('things_brand')
                    content = r'请问您购买' + thingsCategory + '的什么品牌呢?'
                    renderTemplate = self.getTemplate(content)

                    return self.getTemplateAnswer(renderTemplate, content)
                else:
                    self.nlu.ask('things_caterory')
                    content = r'请问您购买' + thingsCategory + '的什么分类呢?'
                    renderTemplate = self.getTemplate(content)

                    return self.getTemplateAnswer(renderTemplate, content)

    def getCard(self, content):
        card = TextCard("智能导购")
        card.setContent(content)
        return card

    def getTemplate(self, content):
        template = BodyTemplate1()
        template.set_title('智能导购')
        template.set_plain_text_content(content)
        template.set_token('0c71de96-15d2-4e79-b97e-e52cec25c254')
        renderTemplate = RenderTemplate(template)
        return renderTemplate

    def getTemplateAnswer(self, renderTemplate, content, outputSpeech=None, card=None):
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
        price = '1'
        for data in self.datas:
            if thing == data[2]:
                price = data[3]
                break

        return str(int(num) * float(price))

    def getData(self):
        datas = list()
        with open("droi/simple_things.csv", 'r') as file:
            items = file.readlines()[0].split('\r')
            for item in items:
                item = item.decode('utf-8')
                datas.append(item.split(','))
        return datas


def handler(event, context):
    bot = CrackDream(event)
    result = bot.run()
    return result
