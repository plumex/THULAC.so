#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import cdll, c_char, c_char_p, cast, POINTER
import os.path
import re

class Thulac:
    def __init__(self, model_path='', user_dict_path='', pre_alloc_size=1024*1024*16, t2s=False, just_seg=False):
        path = os.path.dirname(os.path.realpath(__file__))
        if len(model_path) == 0:
            model_path = path+'/models'

        self.lib = cdll.LoadLibrary(path+'/libthulac.so')
        self.lib.getResult.restype = POINTER(c_char)
        self.lib.init(c_char_p(model_path), c_char_p(user_dict_path), pre_alloc_size, int(t2s), int(just_seg)) 

    def cut(self, text):
        text = re.sub("\s+", " ", text)
        r = self.lib.seg(c_char_p(text))
        p = self.lib.getResult()
        s = cast(p,c_char_p)
        d = '%s'%s.value
        self.lib.freeResult();
        return d.split(' ')


if __name__ == '__main__':
    thu = Thulac()
    print thu.cut('我爱北京天安门。\n天安门上太阳升')
