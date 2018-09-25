# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf
from sharesAnalysis.clcore import k2strokes

'''
线段处理逻辑:
	把笔按以下方式进行处理
	0. 起始线段处理，如果不成立即遇到笔破坏,并且其后形成的线段与起笔是相悖的，则起笔不成立
	1. 按至少三笔成线段原则处理
	2. 按奇数笔成线段原则处理
	3. 按两种情况处理
	4. 第一种情况，1,2特征元素之间不存在缺口
	5. 第二种情况，1,2特征元素之间存在缺口
'''
def drawLine():
    pass

def s_standry():
    pass
def s_inclusion():
    pass

def deal_line():
    # 第一线段处理逻辑

    #
    pass

