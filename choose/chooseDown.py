# -*- coding:utf-8 -*-
import sys,os
#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf
from sharesAnalysis.clcore import STROKES_DIRECTION,FX_CLASS,KSL_INCLUDE, Strokes,k2strokes
from sharesAnalysis.clcore import Line,LINE_TYPE,LINE_JUDGE
from dweunit.unit import log_error, log_warning, log_debug, log_info

# 三K重叠为一个平台
def isPlatform():
    pass

def isNewBegin(aa):
    '''
    功能:新的起点
        1. 回到上一个平台
        2. 脱离平台的x%算着新的起点
    :param aa:
    :return:
    '''

    pass

def chooseDown(xx):
    '''
    功能:
    :param xx:
    :return:
    '''
    pass

if __name__ == '__main__':
    pass
