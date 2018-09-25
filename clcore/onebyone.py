# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
'''
1. 逐根处理包含关系
2. 确定顶分型、底分型
3. 划线
4. 定走势、中枢
5. 背驰
6. 买点、卖点
'''

def onebyone(sdata):

	sdata = sdata[sdata['日期']>='2018-01-01']
	#rdata = sdata.sort_values(by=['日期'], inplace=True)
	rdata = sdata.sort_values(by=['日期'])
	rdata['处理标志'] = True
	rdata['保留标志'] = True
	rdata['顶底上下标志'] = 0 # -2:底， -1:下降， 0:待定 ， 1:上升,  2:顶

	#print(rdata)
	cnt = len(rdata)
	print('len:',cnt)

	# while 循环中
	# 	i 会因为包含关系成立，但是上升、下降不能够判断时，需要往后再看一根k线,直到不为包含关系
	# 特殊处理逻辑
	# 3根k线处于包含关系，不能够确定上升、下降方向时，向后再看一根k线，直到能够确定方向，再从第一根k线处理包含关系
	i = 0
	while i < cnt:
		i+=1

	#for i in range(cnt):
	i = 0
	while i < cnt:

		# 先后看3根
		if i==0:continue
		print('--------------------', i)
		d3 = rdata[ rdata['保留标志'] ][:][i-1:i+2]
		print(d3)
		print(d3.index)

		# 判断3根 走势(上、下)/顶底分类

		# 判断3根是否存在包含关系
		# 处理包含关系


		# 回调包含关系

		i+=1
		break


	return rdata

if __name__=='__main__':


	import os
	# read_csv文件读取方法:必须把读取路径转到文件路径下，再读取
	# 读取时指定编码
	pwd = os.getcwd()
	os.chdir(os.path.dirname('F:\\data\\股票日数据\\'))
	sdata = pd.read_csv("000001.csv", encoding="GBK")

	rdata = onebyone(sdata)
	pass