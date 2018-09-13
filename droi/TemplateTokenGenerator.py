#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import hashlib


class TemplateTokenGenerator():
    md5 = hashlib.md5()
    salt = "freemelite"

    def generateTemplateToken(self, type):
        str = (self.salt + type).encode(encoding='utf-8')
        self.md5.update(str)
        return self.md5.hexdigest()


if __name__ == '__main__':
    generaotor = TemplateTokenGenerator()
    print (generaotor.generateTemplateToken("BodyTemplate1"))
    print (generaotor.generateTemplateToken("ListTemplate1"))
    print (generaotor.generateTemplateToken("ListTemplate2"))
    print (generaotor.generateTemplateToken("ListTemplateItem"))
    pass
