# -*- coding:utf-8 -*-
import sys,os
sys.path.append('..')

import pandas as pd
import matplotlib.pyplot as plt

from sharesAnalysis.conf import conf


from sharesAnalysis.clcore import k_init_data,k_direction
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
	:param aa
	:return:
	'''

	pass

def chooseDown(sdata:pd.DataFrame):
	'''
	功能:
	:param xx:
	:return:
	'''
	idx = 0
	cnt = sdata.count()[0] -2
	while idx<cnt:
		k3 = sdata[idx:idx+3]
		idx += 1
		r = k_direction(k3)



if __name__ == '__main__':
	from sharesAnalysis.clcore import k_init_data
	code=sys.argv[1]
	# read_csv文件读取方法:必须把读取路径转到文件路径下，再读取
	# 读取时指定编码
	pwd = os.getcwd()
	os.chdir(os.path.dirname('F:\\data\\股票日数据\\'))
	sdata = pd.read_csv("%s.csv" % code, encoding="GBK")
	k_init_data(sdata)
	sdata = sdata.sort_values(by=['日期'], ascending=True)
	sdata = sdata[sdata['日期'] >= '2018-01-01']

	chooseDown(sdata)
