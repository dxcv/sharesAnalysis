# -*- coding:utf-8 -*-
import sys
sys.path.append('..')

#import time
import traceback
import pandas as pd

from sharesAnalysis.clcore import Strokes

'''
缠中说禅新笔成立条件：
	用新笔分法，步聚是：
	1，进行包含处理，顶底在内至少4根独立K线。
	2，还原包含关系，顶底在内至少5根K线。
	符合这两项条件，新一笔成立。
	在实际分析中，可能会出现这样一种情况：
	我们考查的区域里的K线不存在包含关系，只有四根独立的K线（即顶底间只有2K线），则这笔仍不成立，因为只满足条件1，不满足条件2。

	注：分2种情况，顶底之间无包含关系，必须5根K线；存在包含处理，顶底在内至少4独立根K线

笔处理逻辑：
	把k线按：
	0. 第一个根k线处理逻辑
	1. 顶分型、底分型、连接线划分
	2. 按笔成立标准判断顶底分型是否有效
	3. 顶底连接成一笔

	  |                      |
	|   |                      |
	      |      |                |        |
	        |   |                    |   | 
	          |                        |
	
k线属性增加: 方向、位置(顶分型的顶、底分型的底、连接线)
包含关系(被包含、包含)在成笔之前已经处理掉

第一笔处理逻辑:
	1. 由first函数处理其他第一根K线的方向
	2. 还有一个办法，
		在选取一段数据时，
		找买点时，从当前数据往前把最高点
		找卖点点时，类似找最低点
	在第二种方法中,存在2种情况
		1. 顶底之间满足一笔条件，这种情况不用多考虑了，暂定为一笔，由后续方向的笔成立而确定
		2. 如果出现双顶双底情况，只要保证这个之间能够构成一笔即可算一笔
			出现条件是第1条不成立，必然出现双顶或者双底情况
'''
# 三个：左包含、右包含、上、下
def k_judge(ld,rd):
	rela=''
	#print( ld['最高价'] < rd['最高价'] , ld['最低价'] < rd['最低价'])
	#print( ld['最高价'] > rd['最高价'] , ld['最低价'] > rd['最低价'])
	#print(ld['最高价'] , rd['最高价'] , ld['最低价'] , rd['最低价'])
	if ld['最高价'] <= rd['最高价'] and ld['最低价'] >= rd['最低价']:
		rela ='右包含'
	# 左包含
	elif ld['最高价'] >= rd['最高价'] and ld['最低价'] <= rd['最低价']:
		rela ='左包含'
	# 上
	elif ld['最高价'] < rd['最高价'] and ld['最低价'] < rd['最低价']:
		rela ='向上'
	# 下
	elif ld['最高价'] > rd['最高价'] and ld['最低价'] > rd['最低价']:
		rela ='向下'
	else: raise('条件未完全包含')

	return  rela

# k线方向、顶、底、包含关系判断
#def k_top():
#def k_bottom():
def k_direction(kdata):
	k0 = kdata.iloc[0]
	k1 = kdata.iloc[1]
	k2 = kdata.iloc[2]
	#print(kdata)
	def k_max(k0,k1,k2):
		if k0['最高价'] < k1['最高价']:
			pass

	# 包含
	r1 = k_judge(k0,k1)
	r2 = k_judge(k1,k2)
	#print (r1,r2)
	#print (r1,r2)

	rela = ''
	dealidx=0

	# 0-1出现包含关系
	if r1 == '左包含' or r1 == '右包含':
		rela=r1
		dealidx = 1

	# 右侧处理
	# 1-2出现包含关系
	if r2 == '左包含' or r2 == '右包含':
		rela=r2
		dealidx = 2
	# 向上/向下 成立
	elif r1 == r2:
		rela = r1
	elif (r1 == '向上' or r1=='右包含') and r2 =='向下':
		rela='顶分型'
	elif (r1 == '向下' or r1=='右包含') and r2 =='向上':
		rela='底分型'
	#print(rela)
	return (rela, dealidx)

#k线包含关系
def k_inclusion_relationship(kdata,relationship, destdata):
	'''
	:param kdata 3根k线:
	:param relationship 来至 k_direction返回值:
	:return:
	'''
	#print(' ---------------- 处理 包含关系 ------')
	#print(relationship)
	# 选择存在包含关系的k线组
	# relationship[1] == 1 时默认值
	km = kdata.iloc[0]
	ks = kdata.iloc[1]
	if relationship[1] == 2:
		km = kdata.iloc[1]
		ks = kdata.iloc[2]

	# 默认为左包含,当为右包含，需要对调km,ks
	if relationship[0] == '右包含':
		kt = km
		km = ks
		ks = kt
	destdata['包含方向'][ks['索引']] = relationship[0]
	#print('begin:')
	#print(km)
	#print(ks)
	# 根据方向进行包含处理
	mx = mm = 0
	if kdata.iloc[1]['方向'] == '向上':
		# 高高原则
		#print( destdata['最低价'][km['索引']]  )
		destdata['最低价'][km['索引']] = max(km['最低价'] , ks['最低价'] )
		destdata['最高价'][km['索引']] = max(km['最高价'] , ks['最高价'] )
	else: #向下
		# 低低原则
		destdata['最低价'][km['索引']] = min(km['最低价'] , ks['最低价'] )
		destdata['最高价'][km['索引']] = min(km['最高价'] , ks['最高价'] )
	# 后续不在处理已经被包含的k线
	destdata['关系'][ks['索引']] = '被包含'

	#print('end:')
	#print(km)
	#print(ks)
	#print('-------------处理结果-------------')
	#print(destdata)
	#print(' ---------------- 处理 包含关系 end ------')

# k线标准化处理
def k_standard(destdata):
	'''
	# 特殊处理情况
	# 1. 第一根K线
	# 	特殊处理为顶底分型,处理完之后，后续不在进入这个处理逻辑
	# 2. 出现分型对第三根K线处理逻辑
	#	顶分型：设置为向下
	#	底分型：设置为向上
	:param kdata:
	:return:
	'''

	idx 		= 0
	first_k = False
	kdata = destdata[ destdata[ '关系'  ] != '被包含' ]

	# 第一笔的方向确定

	# 最后一个根k线单独处理
	cnt = kdata.count()[0]
	while idx<cnt-3 and cnt>=3:
		kdata = destdata[ destdata[ '关系'  ] != '被包含' ]
		k3 = kdata[idx:idx+3]
		if k3.count()[0]<3:break

		print('-----------------------------')
		print(k3)
		r = k_direction(k3)
		print(r)
		if r[1] >1 and r[0]!='顶分型' and r[0]!='底分型':
			#处理包含关系， 调整i的位置
			k_inclusion_relationship(k3, r, destdata)
			destdata['方向'][k3.iloc[2]['索引']] = k3.iloc[1]['方向']
			continue
		DD2RIGHTDIRECTION={ '顶分型':'向下', '底分型': '向上' }
		DD2LEFTDIRECTION={ '顶分型':'向上', '底分型': '向下' }
		DD2DD={ '顶分型':'底分型', '底分型': '顶分型' }
		if r[0] in DD2RIGHTDIRECTION:
			destdata['方向'][k3.iloc[2]['索引']] = DD2RIGHTDIRECTION[r[0]]
			destdata['关系'][k3.iloc[1]['索引']] = r[0]

			# 第一笔前三根处理包含后的k线方向
			if not first_k:
				first_k = True
				destdata['方向'][k3.iloc[0]['索引']] = DD2LEFTDIRECTION[r[0]]
				destdata['方向'][k3.iloc[1]['索引']] = DD2LEFTDIRECTION[r[0]]
				destdata['方向'][k3.iloc[2]['索引']] = DD2RIGHTDIRECTION[r[0]]

		# 第一笔前三根处理包含后的k线方向
		elif not first_k:
			destdata['方向'][k3.iloc[0]['索引']] = r[0]
			destdata['方向'][k3.iloc[1]['索引']] = r[0]
			destdata['方向'][k3.iloc[2]['索引']] = r[0]
			first_k = True
		else:
			destdata['方向'][k3.iloc[2]['索引']] = r[0]

		# 第一笔中
		idx+=1
	# end while

	# 处理第一、二根K线、最后一根K线
	kdata 	= destdata[ destdata[ '关系'  ] != '被包含' ]
	b 		= kdata.iloc[0]['索引']
	e 		= kdata.iloc[kdata.count()[0]-1]['索引']
	edir 	= kdata.iloc[kdata.count()[0]-1]['方向']
	dtdata 	= destdata[(destdata['关系']=='顶分型')|(destdata['关系']=='底分型')]
	#print(dtdata.count())
	if  dtdata.count()[0]>0:
		dd_b 	= dtdata.iloc[0]['关系']
		dd_e 	= dtdata.iloc[dtdata.count()[0]-1]['关系']
		#print(b,dd_b)
		destdata['关系'][b] = DD2DD[dd_b]
		destdata['关系'][e] = DD2DD[dd_e]
	elif edir == '向上': #只有一个方向的数据情况
		destdata['关系'][b] = '底分型'
		destdata['关系'][e] = '顶分型'
	elif edir == '向下': #只有一个方向的数据情况
		destdata['关系'][b] = '顶分型'
		destdata['关系'][e] = '底分型'


	'''
	# 顶底分型数据
	dtdata 	= destdata[(destdata['关系']=='顶分型')|(destdata['关系']=='底分型')]

	# 遍历 顶底分型数据 统计顶底之间的连接线
	idx 		= 0
	dateOrder 	= 'desc'
	if kdata.iloc[0]['日期'] < kdata.iloc[1]['日期']:
		dateOrder = 'asc'

	dd_b = dtdata.iloc[idx]
	while idx < dtdata.count()[0]:
		dd_e = dtdata.iloc[idx]
		if dateOrder == 'desc':
			dd_m = destdata[ (destdata['日期']<=dd_b['日期']) & (destdata['日期'] >= dd_e['日期']) ]
		else:
			dd_m = destdata[ (destdata['日期']>=dd_b['日期']) & (destdata['日期'] <= dd_e['日期']) ]
		print ( dd_m.count()[0] )

		dd_b = dd_e
		idx += 1
	'''

	#print('end standard')

def ranging_top2bottom(destdata):
	kdata 	= destdata[ destdata[ '关系'  ] != '被包含' ]
	# 顶底分型数据
	dtdata 	= destdata[(destdata['关系']=='顶分型')|(destdata['关系']=='底分型')]

	# 遍历 顶底分型数据 统计顶底之间的连接线
	idx 		= 0
	dateOrder 	= 'desc'
	if kdata.iloc[0]['日期'] < kdata.iloc[1]['日期']:
		dateOrder = 'asc'


	# 计算顶底距离
	dtcnt 	= dtdata.count()[0]
	dd_b 	= dtdata.iloc[idx]
	while idx < dtdata.count()[0]:
		dd_e = dtdata.iloc[idx]
		if dateOrder == 'desc':
			dd_m = destdata[ (destdata['日期']<=dd_b['日期']) & (destdata['日期'] > dd_e['日期']) ]
		else:
			dd_m = destdata[ (destdata['日期']>=dd_b['日期']) & (destdata['日期'] < dd_e['日期']) ]
		destdata['顶底距离'][dd_e['索引']] 				= dd_m.count()[0] + 1
		destdata['顶底距离.标准化处理'][dd_e['索引']]	= dd_m[dd_m['关系'] !='被包含'].count()[0] + 1
		dd_b = dd_e
		idx += 1

'''
			if dd_e['顶底距离.标准化处理'] >=4 and dd_e['顶底距离'] >=5:
				# 判断是正常新笔成立还是双顶双底情况
				if pre.end['日期'] == dd_b['日期']: # 新笔成立
					pre.status 	= True
					stokesList.append( Strokes(pre.end, dd_e) )
				else: #双顶双底 笔是否延伸:采用 低低高高原则
					# 底分型 情况下笔延伸
					if   dd_e['关系'] == '底分型' and pre.end['关系'] == '底分型':
						if dd_e['最低价'] <= pre.end['最低价'] : pre.end = dd_e
					# 顶分型 情况下笔延伸
					elif dd_e['关系'] == '顶分型' and pre.end['关系'] == '顶分型':
						if dd_e['最高价'] >= pre.end['最高价'] : pre.end = dd_e
					# 新笔成立
					else: #当前pre.end 与 dd_e 之间存在偶数个顶底分型(分别各一个以上)
						# 这种情况新笔吗？
						pre.status 	= True
						stokesList.append( Strokes(pre.end, dd_e) )
			elif pre.end['日期'] == dd_b['日期']:
				# 新笔不成立,暂不用处理
				pass
			else:
				# 这种情况下，需要考察: 1. 是否是双底双顶情况；2. 当前pre.end 与 dd_e 之间存在偶数个顶底分型(分别各一个以上)
				pass
				
'''
'''
	kdata 	= destdata[ destdata[ '关系'  ] != '被包含' ]
	# 顶底分型数据
	dtdata 	= destdata[(destdata['关系']=='顶分型')|(destdata['关系']=='底分型')]

	# 遍历 顶底分型数据 统计顶底之间的连接线
	idx 		= 0
	dateOrder 	= 'desc'
	if kdata.iloc[0]['日期'] < kdata.iloc[1]['日期']:
		dateOrder = 'asc'


	# 计算顶底距离
	dtcnt 	= dtdata.count()[0]
	dd_b 	= dtdata.iloc[idx]
	while idx < dtdata.count()[0]:
		dd_e = dtdata.iloc[idx]
		if dateOrder == 'desc':
			dd_m = destdata[ (destdata['日期']<=dd_b['日期']) & (destdata['日期'] > dd_e['日期']) ]
		else:
			dd_m = destdata[ (destdata['日期']>=dd_b['日期']) & (destdata['日期'] < dd_e['日期']) ]
		destdata['顶底距离'][dd_e['索引']] 				= dd_m.count()[0] + 1
		destdata['顶底距离.标准化处理'][dd_e['索引']]	= dd_m[dd_m['关系'] !='被包含'].count()[0] + 1
		dd_b = dd_e
		idx += 1
'''
def draw_strokes(destdata):
	'''
	功能:画笔
	画笔逻辑：
		笔成立(顶底之间是否成立),则前面的笔被确定，
		后一个顶(底)与前底(顶)不成立则去除，去除之后，必然出现双顶双底情况，采取处理方式如下，
			双顶:顶高保留
			双底:底低保留
	:param destdata:
	:return:
	'''
	print ("----------------------draw_strokes--------------------")
	dtdata 	= destdata[(destdata['关系']=='顶分型')|(destdata['关系']=='底分型')]
	dtcnt 	= dtdata.count()[0]
	dateOrder 	= 'desc'
	if dtdata.iloc[0]['日期'] < dtdata.iloc[1]['日期']:
		dateOrder = 'asc'

	# 处理第一笔
	idx 	= 2 # 正常情况下第三个顶/底分型就是为第二笔,如果出现特殊情况，idx将会后移
	# 如果第1,2顶底分型之间的笔不成立，需要加入更多顶底分型来完成第一笔
	# 如果 一段数据中少于3线段（至少9笔）的情况，这种数据不具备参考价值
	try: #
		# 笔起始位置
		b_b = dt0 = dtdata.iloc[0]
		b_e = dt1 = dtdata.iloc[1]
		#第一笔成立标准降低, 笔标准定义参考缠中说禅新笔定义
		if not ( dt1['顶底距离.标准化处理'] >=3 or dt1['顶底距离'] >=4 ):
			# 如果以上笔不成立，必然出现双顶/双底情况
			# 先考察 dt1 dt2 之间是否成立一笔
			dt2 = dtdata.iloc[2]
			dt3 = dtdata.iloc[3]
			if dt2['顶底距离.标准化处理'] >=3 or dt2['顶底距离'] >=4:
				b_b = dt1
				b_e = dt2
				idx = 2
			else: # 如果不成立，则假定dt0-dt3成立为一笔,后续处理从dt4开始
				b_b = dt0
				b_e = dt3
				idx = 3
			#加入下一个顶底关系进来
		#设置第一笔情况
		print("----------------------第一笔--------------------")
		# 确定方向 与 起止点
		print(b_b)
		print(b_e)

	except:
		print("----------------------第一笔 处理失败--------------------")
		traceback.print_exc(5)
		return None

	'''
	class Strokes:
		#def __init__(self, begin, end, status=False, status='正常一笔', isContinue=False):
		def __init__(self, begin, end, status='正常一笔', isContinue='未延笔', reDeal='未重处理'):
			self.begin 	= begin
			self.end	= end
			self.status	= status
			self.isContinue= isContinue# 是否被下一笔破坏而确定
			self.reDeal = reDeal
			#self.status	= status# 是否被下一笔破坏而确定
		def __str__(self):
			return ( '%s-%s, %s, %s' %
				(self.begin['日期'], self.end['日期'], self.status, self.isContinue ) )
	'''

	stokesList = [Strokes(b_b, b_e)]

	'''
	pre = stokesList[-1]
	dd_b = pre.end
	dd_e = pre.end
	def pre3redeal():
		prepre = stokesList[-3]
		prepre.end 			= pre.end
		dd_e 				= pre.end
		prepre.isContinue 	= '延笔'
		prepre.reDeal 		= '重新处理'
		stokesList 			= stokesList[:-2]
		pre  =  prepre
	def pre2real():
		prepre.end 			= dd_e
		prepre.isContinue 	= '延笔'
		prepre.reDeal 		= '重新处理'
		stokesList 			= stokesList[:-1]
		pre  =  prepre
	'''


	# 以下从第二笔开始处理
	# 1. 双顶双底情况
	# 2. 笔破坏，上一笔成立，本笔待定
	print('dtcnt:',dtcnt, idx+1)
	#q_idx = 0
	if dtcnt >idx:
		#dd_b = dtdata.iloc[idx]
		dd_b = b_e
		idx += 1
		while idx < dtdata.count()[0]:
			dd_e = dtdata.iloc[ idx]
			pre  = stokesList[-1]
			print('while in:\n\t',pre.begin['日期'], pre.end['日期'], pre.end['关系'], pre.status)
			print('\t',dd_e['日期'], dd_e['关系'])

			# 1. 新笔成立，前一笔确定
			if pre.end['日期'] == dd_b['日期']:
				print('1. 新笔成立，前一笔确定')
				# 弱一笔优先处理,双顶双底情况
				if pre.status == '弱一笔' and pre.isContinue !='延笔':
					print('1.1 弱一笔特殊处理')
					# 前一笔为弱一笔，并且不延续情况下
					if len(stokesList)>1:
						prepre = stokesList[-2]
						if   dd_e['关系'] == '底分型' and dd_e['最低价'] <= prepre.end['最低价']:
							# 先判断被丢弃的这一笔与前两笔是否构成延续
							if len(stokesList)>2 and  pre.end['最高价'] >= stokesList[-3].end['最高价']:
								#pre3redeal()
								prepre = stokesList[-3]
								prepre.end 			= pre.end
								dd_e 				= pre.end
								prepre.isContinue 	= '延笔'
								prepre.reDeal 		= '重新处理'
								stokesList 			= stokesList[:-2]
								pre  =  prepre
								print ('here 1', prepre.status)
							else:
								#pre2real()
								prepre.end 			= dd_e
								prepre.isContinue 	= '延笔'
								prepre.reDeal 		= '重新处理'
								stokesList 			= stokesList[:-1]
								pre  =  prepre
								print ('here 2', prepre.status)
						elif dd_e['关系'] == '顶分型' and dd_e['最高价'] >= prepre.end['最高价'] :
							if len(stokesList)>2 and  pre.end['最低价'] <= stokesList[-3].end['最低价']:
								#pre3redeal()
								prepre = stokesList[-3]
								prepre.end 			= pre.end
								dd_e 				= pre.end
								prepre.isContinue 	= '延笔'
								prepre.reDeal 		= '重新处理'
								stokesList 			= stokesList[:-2]
								pre  =  prepre
								print ('here 3', prepre.status)
							else:
								prepre.end 			= dd_e
								prepre.isContinue 	= '延笔'
								prepre.reDeal 		= '重新处理'
								stokesList 			= stokesList[:-1]
								pre  =  prepre
								print ('here 4', prepre.status)
						else:
							print('弱一笔未处理')
				elif dd_e['顶底距离.标准化处理'] >=4 and dd_e['顶底距离'] >=5:
					#pre.status 	= '正常一笔'
					stokesList.append( Strokes(pre.end, dd_e, '正常一笔') )



			# 2, 笔延续
			# 当日期 不相等 且 出现双顶双底情况下
			# 后面的顶高于或者等于前面的顶，底一样
			elif dd_e['关系'] == pre.end['关系']:
				print('2. 笔延续')
				if   dd_e['关系'] == '底分型':
					print(dd_e['日期'],pre.end['日期'], "dd_e['最低价'] <= pre.end['最低价']",
						  dd_e['最低价'] <= pre.end['最低价'], dd_e['最低价'] , pre.end['最低价']  )
				else:
					print(dd_e['日期'],pre.end['日期'], "dd_e['最高价] >= pre.end['最高价']",
						  dd_e['最高价'] >= pre.end['最高价'], dd_e['最高价'] , pre.end['最高价']  )

				if   dd_e['关系'] == '底分型' and dd_e['最低价'] <= pre.end['最低价']:
					pre.end = dd_e
					pre.isContinue = '延笔'
				elif dd_e['关系'] == '顶分型' and dd_e['最高价'] >= pre.end['最高价'] :
					pre.end = dd_e
					pre.isContinue = '延笔'
				#else: 除此之外跳过这个分型

			# 3.跨过2个以上的顶底情况
			# 当日期不相等，未出现双顶双底情况，这种情况是由于双顶双底判断不能够构成笔延续情况下
			# 强一笔、弱一笔
			elif dd_e['关系'] != pre.end['关系'] and pre.end['日期'] != dd_b['日期']:
				# 这种情况是最不稳定的情况，属于强制一笔,由于双顶双底已经保证当前的顶底逻辑不会出现相悖情况，
				# 不用判断前顶比后底高, 前底比后顶底
				# 如果下一个顶(底)比强制的一笔的起点顶(底)要低(高)，则前面一笔不成立

				# 需要思考的问题是，如果连续多次出现强制一笔怎么处理？

				# 强制一笔情况，如果出现起止之间少于多少根有效k线则认为不能够强制一笔呢？
				# 暂定为9根未处理包关系的k线数为 5 根
				# 暂定为9根处理包关系之后的k线数为 10 根
				# 统计强制一笔之间的k线

				#顶底之间如果出现中间的顶比顶高，或者中间的底比底低
				#这种情况一笔不成立
				dds = destdata[ (destdata['日期']>pre.end['日期']) & \
								(destdata['日期']<dd_e['日期']) & \
								(destdata['关系']!='被包含') ]
				dm_max = dds.sort_values(['最高价'],ascending=False).iloc[0]
				dm_min = dds.sort_values(['最低价'],ascending=True).iloc[0]
				print('dmax dmin............................')
				print(dm_max['日期'],dm_max['最高价'])
				print(dm_max['日期'],dm_min['最低价'])
				print( dd_e['关系'], dm_max['最高价'], pre.end['最高价'] , dm_min['最低价'], dd_e['最低价'] )
				print( dd_e['关系'] =='底分型' ,
					   dm_max['最高价']> pre.end['最高价'] , dm_min['最低价']< dd_e['最低价'] )
				isOk = True
				if dd_e['关系'] =='顶分型' and \
						( dm_max['最高价']>=dd_e['最高价'] or dm_min['最低价']<=pre.end['最低价'] ):
					isOk = False
				if dd_e['关系'] =='底分型' and \
						( dm_max['最高价']>=pre.end['最高价'] or dm_min['最低价']<=dd_e['最低价'] ):
					isOk = False
				#isOk = True
				print('dmax dmin............................', isOk)

				cnt1 = destdata[ (destdata['日期']>=pre.end['日期']) & \
								(destdata['日期']<=dd_e['日期']) & \
								(destdata['关系']!='被包含')
					].count()[0]
				cnt2 = destdata[ (destdata['日期']>=pre.end['日期']) & \
								(destdata['日期']<=dd_e['日期'])
					].count()[0]


				print('3.跨过2个以上的顶底情况 cnt:', cnt1, cnt2)
				print(pre.end['日期'], dd_b['日期'], dd_e['关系'], pre.end['关系']  )
				if cnt1 >=6 and cnt2>=7 and isOk:
					#pre.status 	= True
					stokesList.append( Strokes(pre.end, dd_e, '强一笔') )

				elif cnt1 >=4 and cnt2>=5 and isOk: # 满足笔最低要求
					# 按高高低低原则判断
					if (dd_e['关系'] == '底分型' and dd_e['最低价'] <= pre.begin['最低价']) \
						or (dd_e['关系'] == '顶分型' and dd_e['最高价'] >= pre.begin['最高价']) :
						#pre.status 	= True
						stokesList.append( Strokes(pre.end, dd_e, '弱一笔') )
					else:
						print('弱一笔不成立:')
						print('dd_e', dd_e)
						print('dd_e', pre.begin)

				#if dd_e['顶底距离.标准化处理'] >=4 and dd_e['顶底距离'] >=5:
				#	pre.status 	= True
				#	stokesList.append( Strokes(pre.end, dd_e) )
				#else:
					#if   dd_e['关系'] == '底分型' and dd_e['最低价'] <= pre.end['最低价']:
					#elif dd_e['关系'] == '顶分型' and dd_e['最高价'] >= pre.end['最高价'] :

			else:
				pass

			pre = stokesList[-1]
			print(pre.end['日期'] , dd_e['日期'])
			if pre.end['日期'] == dd_e['日期']: print("处理结果:",pre)

			# 笔修正，可以考虑在单独循环中处理 或者放在弱一笔、强一笔成立时处理
			# 除正常笔/且未延续 之外情况(弱一笔、强一笔),并且是当前循环处理后参数的新笔
			#if pre.status !='正常一笔' and not pre.isContinue and pre.end['日期'] == dd_e['日期']:
			#	print ('####################################')
			#	print (pre.end)


			#
			#if pre.reDeal == '重新处理'and pre.end['日期'] == dd_e['日期']:
			#	print ("当前为重新处理的时间点:",pre.end['日期'])


			dd_b 		= dd_e
			idx += 1

			'''
			# 底分型 情况下笔延伸
			if   dd_e['关系'] == '底分型' and pre.end['关系'] == '底分型':
				print(dd_e['日期'],pre.end['日期'], "dd_e['最低价'] <= pre.end['最低价']",
					  dd_e['最低价'] <= pre.end['最低价'], dd_e['最低价'] , pre.end['最低价']  )
				if dd_e['最低价'] <= pre.end['最低价'] : pre.end = dd_e
			# 顶分型 情况下笔延伸
			elif dd_e['关系'] == '顶分型' and pre.end['关系'] == '顶分型':
				print(dd_e['日期'],pre.end['日期'], "dd_e['最高价] >= pre.end['最高价']",
	  			dd_e['最高价'] >= pre.end['最高价'], dd_e['最高价'] , pre.end['最高价']  )
				if dd_e['最高价'] >= pre.end['最高价'] : pre.end = dd_e
			# 新笔成立
			elif pre.end['日期'] != dd_b['日期']: # 新笔成立
				#当前pre.end 与 dd_e 之间存在偶数个顶底分型(分别各一个以上)
				# 这种情况新笔吗？ 有2种情况：笔成立，笔强制成立
				pre.status 	= True
				stokesList.append( Strokes(pre.end, dd_e) )

			# 新笔成立
			elif pre.end['日期'] == dd_b['日期'] and dd_e['顶底距离.标准化处理'] >=4 and dd_e['顶底距离'] >=5:
				pre.status 	= True
				stokesList.append( Strokes(pre.end, dd_e) )

			dd_b 		= dd_e
			idx += 1
			'''

			#除此之外的情况，不在进行笔处理，需要考察后续的分型进行处理
			#else: pass



	return stokesList

# 处理第一根k线、第一个顶底分型
# 找到第一个分型即可
# 在整个k线系统中第一笔不是特别重要
def k_first(kdata):
	# 假定当前起点向上
	'''
	:param kdata:
	:return:
	i = 0
	while True:
		r = k_direction(kdata[i+0:i+3])
		if r[1] >0:
			#处理包含关系， 调整i的位置
			pass
		else:
			break
	if r[0] == '向下': pass
	'''
	#kdata[0:30][:]
	#处理目标数据的前面一笔情况
	#决定第一、二根K线的方向
	print('-------------at first-------------------')
	k_standard(kdata)
	ranging_top2bottom(kdata)
	#print(kdata)
	strokesList = draw_strokes(kdata)
	print('-------------at first-------------------')
	return  strokesList

def draw(kdata, strokesdata, htmlname):
	#kdata['开盘价'] = 0
	from pyecharts import Kline, EffectScatter, Line, Overlap
	#[open, close, lowest, highest] （即：[开盘值, 收盘值, 最低值, 最高值]）

	kdata
	dt = kdata[(kdata['关系']=='顶分型')|(kdata['关系']=='底分型')]
	es =EffectScatter('分型图')
	v = []

	#点图
	for i in dt['索引']:
		v1 = 0
		print (i)
		if dt['关系'][i]=='底分型':
			v1 = dt['最低价'][i]
		else:
			v1 = dt['最高价'][i]
		v.append(v1)
	#]
	es.add("effectScatter", dt['日期'], v,
			symbol = "pin",
		   )

	print(kdata.columns)
	v1 = kdata[[ '开盘价',  '收盘价',  '最低价',    '最高价']].as_matrix()
	v1 = v1.tolist()
	kline = Kline("名称")
	kline.add(
		"日K",
		kdata['日期'],
		v1,
		mark_point=["max"],
		is_datazoom_show=True,
	)

	attr = [ s.begin['日期'] for s in strokesdata ]
	attr.append(strokesdata[-1].end['日期'])
	v1 = []
	for s in strokesdata:
		if s.begin['关系'] == '顶分型':
			v1.append(s.begin['最高价'])
		else:
			v1.append(s.begin['最低价'])
	e = strokesdata[-1]
	if e.end['关系'] == '顶分型':
		v1.append(e.end['最高价'])
	else:
		v1.append(e.end['最低价'])

	line = Line("折线图示例")
	line.add("笔画", attr, v1, is_stack=True, is_label_show=True)
	line.add(
		"日K",
		attr,
		v1,
		mark_point=["max"],
		is_datazoom_show=True,
	)

	overlap = Overlap()
	overlap.add(kline)
	overlap.add(line)
	overlap.add(es)
	overlap.render(htmlname)

	print('here ok')



def k2strokes(srcdata):
	'''
	功能: 对数据进行包含处理后计算出顶底数据，以及笔连接
	:param srcdata:  源数据
	:return(经过包含顶底处理的数据，笔队列):
	'''
	kdata = srcdata.copy()
	k_standard(kdata)
	ranging_top2bottom(kdata)
	strokesList = draw_strokes(kdata)
	return (kdata, strokesList)

def k_init_data(kdata):
	kdata['索引'] 	= kdata.index
	kdata['方向'] 	= '向上'
	kdata['关系'] 	= '连接线'
	kdata['包含方向'] 	= ''
	kdata['顶底距离'] 	= 0
	kdata['顶底距离.标准化处理'] 	= 0
	# 去除停牌的数据
	kdata.drop(kdata[kdata['最高价']==0.00].index, inplace=True)

#顶底
def test_right_in():
	print('-------------------test1-------------------')
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.96,22.5 ],
		['2018-07-18','000002','万 科Ａ',23.05,22.42],
		['2018-07-17','000002','万 科Ａ',23.28,22.65],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47]
						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)
def test_left_in():
	print('-------------------test1-------------------')
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',23.05,22.42],
		['2018-07-18','000002','万 科Ａ',22.96,22.5 ],
		['2018-07-17','000002','万 科Ａ',23.28,22.65],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47]
						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)

def test_first_top():
	print('-------------------test1-------------------')
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.55,22.42],
		['2018-07-18','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-17','000002','万 科Ａ',22.68,22.35],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47]
						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)

def test_first_bottom():
	print('-------------------test1-------------------')
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.55,22.42],
		['2018-07-18','000002','万 科Ａ',21.96,21.5 ],
		['2018-07-17','000002','万 科Ａ',22.68,22.35],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47]
						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)

def test_relay_1():
	# 中继 笔 延续
	print('-------------------test1-------------------')
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.55,22.42],
		['2018-07-18','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-17','000002','万 科Ａ',22.68,22.35],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47],

		['2018-07-11','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-10','000002','万 科Ａ',22.68,22.35],
		['2018-07-09','000002','万 科Ａ',23.66,22.81],
		['2018-07-08','000002','万 科Ａ',24.35,23.64],
		['2018-07-07','000002','万 科Ａ',25.22,25.47],

						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)
def test_relay_2():
	# 中继 笔 延续
	sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.55,22.42],
		['2018-07-18','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-17','000002','万 科Ａ',22.68,22.35],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47],
		['2018-07-11','000002','万 科Ａ',23.98,23.22],

		['2018-07-10','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-09','000002','万 科Ａ',22.68,22.35],
		['2018-07-08','000002','万 科Ａ',23.66,22.81],
		['2018-07-07','000002','万 科Ａ',24.35,23.64],
		['2018-07-06','000002','万 科Ａ',25.22,25.47],

		['2018-07-05','000002','万 科Ａ',23.96,22.5 ],
		['2018-07-04','000002','万 科Ａ',22.68,22.35],
		['2018-07-03','000002','万 科Ａ',23.66,22.81],
		['2018-07-02','000002','万 科Ａ',24.35,23.64],
		['2018-07-01','000002','万 科Ａ',25.22,25.47],


						  ], columns=['日期','股票代码','名称','最高价','最低价'])
	k_init_data(sdata)
	k2strokes(sdata)

#左包含
def test2():
		sdata = pd.DataFrame([
		['2018-07-19','000002','万 科Ａ',22.96,22.5 ],
		['2018-07-18','000002','万 科Ａ',23.05,22.42],
		['2018-07-17','000002','万 科Ａ',23.28,22.65],
		['2018-07-16','000002','万 科Ａ',23.66,22.81],
		['2018-07-13','000002','万 科Ａ',24.35,23.64],
		['2018-07-12','000002','万 科Ａ',24.22,23.47]
						  ], columns=['日期','股票代码','名称','最高价','最低价'])

def test3():
	sdata = pd.DataFrame([
		['2018-06-26', '000005', '世纪星源', 2.95, 2.96, 2.88, 2.91, 2.93],
		['2018-06-25', '000005', '世纪星源', 2.93, 2.98, 2.93, 2.93, 2.93],
		['2018-06-22', '000005', '世纪星源', 2.93, 2.96, 2.82, 2.85, 2.91],
		['2018-06-21', '000005', '世纪星源', 2.91, 3.05, 2.9, 2.93, 2.9],
		['2018-06-20', '000005', '世纪星源', 2.9, 3.05, 2.9, 2.79, 2.8],
		['2018-06-19', '000005', '世纪星源', 2.8, 3.09, 2.9, 3.08, 3.11],
		['2018-06-15', '000005', '世纪星源', 3.11, 3.18, 3.06, 3.16, 3.17],
		['2018-06-14', '000005', '世纪星源', 3.17, 3.2, 3.15, 3.19, 3.18],
		['2018-06-13', '000005', '世纪星源', 3.18, 3.28, 3.16, 3.28, 3.28],
		['2018-06-12', '000005', '世纪星源', 3.28, 3.31, 3.25, 3.3, 3.29],
		['2018-06-11', '000005', '世纪星源', 3.29, 3.33, 3.28, 3.33, 3.33],
		['2018-06-08', '000005', '世纪星源', 3.33, 3.39, 3.3, 3.39, 3.38],
		['2018-06-07', '000005', '世纪星源', 3.38, 3.42, 3.38, 3.42, 3.39],
		['2018-06-06', '000005', '世纪星源', 3.39, 3.42, 3.38, 3.42, 3.42],
		['2018-06-05', '000005', '世纪星源', 3.42, 3.42, 3.38, 3.39, 3.4],
		['2018-06-04', '000005', '世纪星源', 3.4, 3.45, 3.39, 3.43, 3.44],
		['2018-06-01', '000005', '世纪星源', 3.44, 3.46, 3.39, 3.42, 3.44],
		['2018-05-31', '000005', '世纪星源', 3.44, 3.45, 3.38, 3.42, 3.4],
		['2018-05-30', '000005', '世纪星源', 3.4, 3.45, 3.37, 3.52, 3.6],

		['2018-05-29', '000005', '世纪星源', 3.6, 3.65, 3.57, 3.63, 3.68],
		['2018-05-28', '000005', '世纪星源', 3.68, 3.72, 3.66, 3.7, 3.71],
		['2018-05-25', '000005', '世纪星源', 3.71, 3.72, 3.66, 3.68, 3.66],
		['2018-05-24', '000005', '世纪星源', 3.66, 3.74, 3.66, 3.67, 3.66],
		['2018-05-23', '000005', '世纪星源', 3.66, 3.71, 3.65, 3.69, 3.69],
		['2018-05-22', '000005', '世纪星源', 3.69, 3.71, 3.67, 3.7, 3.7],
		['2018-05-21', '000005', '世纪星源', 3.7, 3.73, 3.69, 3.7, 3.68],
		['2018-05-18', '000005', '世纪星源', 3.68, 3.74, 3.69, 3.66, 3.68],
		['2018-05-17', '000005', '世纪星源', 3.68, 3.7, 3.66, 3.67, 3.7],
		['2018-05-16', '000005', '世纪星源', 3.7, 3.7, 3.64, 3.7, 3.72],
		['2018-05-15', '000005', '世纪星源', 3.72, 3.76, 3.69, 3.76, 3.75],
		['2018-05-14', '000005', '世纪星源', 3.75, 3.75, 3.68, 3.72, 3.76],
		['2018-05-11', '000005', '世纪星源', 3.76, 3.75, 3.66, 3.73, 3.75],
		['2018-05-10', '000005', '世纪星源', 3.75, 3.9, 3.69, 3.68, 3.68],
		['2018-05-09', '000005', '世纪星源', 3.68, 3.72, 3.67, 3.7, 3.7]
						  ],
		columns=['日期','股票代码','名称','收盘价','最高价','最低价','开盘价','前收盘'])
	k_init_data(sdata)

	#k3 = sdata[sdata.count()[0]-3:]
	#print(k3)
	#r = k_direction(k3)
	#print(r)
	#k3 = sdata[sdata.count()[0]-6:]
	#k_standard(k3)
	#print(k3)

	k2strokes(sdata)
def test4():
	sdata = pd.DataFrame([
		['2018-05-29', '000005', '世纪星源', 3.6, 3.65, 3.57, 3.63, 3.68],
		['2018-05-28', '000005', '世纪星源', 3.68, 3.72, 3.66, 3.7, 3.71],
		['2018-05-25', '000005', '世纪星源', 3.71, 3.72, 3.66, 3.68, 3.66],
		['2018-05-24', '000005', '世纪星源', 3.66, 3.74, 3.66, 3.67, 3.66],
		['2018-05-23', '000005', '世纪星源', 3.66, 3.71, 3.65, 3.69, 3.69],
		['2018-05-22', '000005', '世纪星源', 3.69, 3.71, 3.67, 3.7, 3.7],
		['2018-05-21', '000005', '世纪星源', 3.7, 3.73, 3.69, 3.7, 3.68],
		['2018-05-18', '000005', '世纪星源', 3.68, 3.74, 3.69, 3.66, 3.68],
		['2018-05-17', '000005', '世纪星源', 3.68, 3.7, 3.66, 3.67, 3.7],
		['2018-05-16', '000005', '世纪星源', 3.7, 3.7, 3.64, 3.7, 3.72],
		['2018-05-15', '000005', '世纪星源', 3.72, 3.76, 3.69, 3.76, 3.75],
		['2018-05-14', '000005', '世纪星源', 3.75, 3.75, 3.68, 3.72, 3.76],
		['2018-05-11', '000005', '世纪星源', 3.76, 3.75, 3.66, 3.73, 3.75],
		['2018-05-10', '000005', '世纪星源', 3.75, 3.9, 3.69, 3.68, 3.68],
		['2018-05-09', '000005', '世纪星源', 3.68, 3.72, 3.67, 3.7, 3.7]
		],
		columns=['日期','股票代码','名称','收盘价','最高价','最低价','开盘价','前收盘'])
	k_init_data(sdata)

	k3 = sdata[sdata.count()[0]-3:]
	#print(k3)
	#r = k_direction(k3)
	#print(r)
	#k3 = sdata[sdata.count()[0]-6:]
	k_standard(k3)
	print(k3)

	#k2strokes(sdata)

def draw_test():
	v1 = pd.DataFrame([['2018/7/1',8.75, 8.73, 8.69, 8.81], ['2018/7/2',8.75, 8.7, 8.69, 8.85]],
			columns=['日期','开盘价',  '收盘价',  '最低价',    '最高价'] )
	#draw(v1)

if __name__ == '__main__':
	import os
	import sys
	code=sys.argv[1]
	# read_csv文件读取方法:必须把读取路径转到文件路径下，再读取
	# 读取时指定编码
	pwd = os.getcwd()
	os.chdir(os.path.dirname('F:\\data\\股票日数据\\'))
	sdata = pd.read_csv("%s.csv" % code, encoding="GBK")
	k_init_data(sdata)
	sdata = sdata.sort_values(by=['日期'], ascending=True)
	sdata = sdata[sdata['日期'] >= '2018-01-01']
	kdata,strokesList = k2strokes(sdata)
	draw(sdata, strokesList, htmlname='F:\\data\\log\\src.html')
	import pickle

	output = open('F:\\data\\log\\sdata.pk', 'wb')
	pickle.dump(sdata,output,-1)
	output.close()
	output = open('F:\\data\\log\\strokesList.pk', 'wb')
	pickle.dump(strokesList,output,-1)
	output.close()
	output = open('F:\\data\\log\\kdata.pk', 'wb')
	pickle.dump(sdata,output,-1)
	output.close()

	#d = srcdata[[ '日期', '最低价',    '最高价', '方向','关系' , '顶底距离', '顶底距离.标准化处理']]
	#d.to_excel('F:\\data\\log\\src.000036.xls','w')
	#kdata.to_excel('F:\\data\\log\\000036.xls','w')


	#test_left_in()
	#test_right_in()
	#test_first_top()
	#test_first_bottom()

	#test_relay_1()
	#test_relay_2()
	#sdata = sdata[sdata['日期'] >= '2018-01-01']
	#k2strokes(sdata)
	#rdata = onebyone(sdata)

	#k_init_data(sdata)
	#k2strokes(sdata)
	#test3()
	pass
