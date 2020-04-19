import random
import numpy as np
import time
import os
import signal


print('Введите количество каналов n')
n = int(input())
#print('n=',n)
l = [] ## Нумерация каналов с нуля

for i in range(n):
	print('Введите интенсивность канала №',i)
	lambda_temp = int(input())
	l.append(lambda_temp)
#print('Интенсивности каналов:',l)



print('Введите интенсивность потока заявок')
nu = int(input())
#print('Она равна: ',nu)



k = 10 # ограничение на количество клиентов



Y = [] # генерируем поток клиентов

for i in range(k):
	Y.append(random.expovariate(1/nu))
print('Y= ',Y)

#X = []
#for i in range(n):
#	x_temp = []
#	for j in range(k):
#		x_temp.append(random.expovariate(1/l[i]))				
#	X.append(x_temp)
#
#
#print('X= ',X)










def minus2(list1,list2,list3):

	list_eic_e = list2+list3
	i = 0
	n= len(list1)
	res = []
	while i<n:
		res.append(list1[i]-list_eic_e[i])
		i+=1
	return res


def minus_f(list1,list2):
	if len(list1)!=len(list2):
		print('ERROR')
	i = 0
	n= len(list1)
	res = []
	while i<n:
		res.append(list1[i]-list2[i])
		i+=1
	return res


def workers_check(x): # проверка свободных РАБотников 
	flag = 0
	for element in x:
		if element == 0:
			flag = 1
	return(flag)	


def indexes(list,value):
	i = 0
	res = []
	while i<len(list):
		if list[i] == value:
			res.append(i) 
		i+=1

	return res

def workers_select(list):
	random_worker = np.random.choice(list)
	return(random_worker)


def zero_indexes(list):
	i=0
	res = []
	for i in range(len(list)):
		if list[i]<0.00001 and list[i]>-0.00001:
			res.append(i)
			i+=1
		else:
			i+=1
	return res
















que=[] # входящий поток клиентов - очередь

workers = [] 

w_time_e = []
w_tic = []
for i in range(n):
	workers.append(0)  # флаги работников.  0 - свободен. 1 - занят
	w_time_e.append(0) # список со временем через сколько секунд работник отпустит клиента
	w_tic.append(0)	   # список в котором оставляем время начала работы определенного работника

i = 0
tic = time.perf_counter() # для того чтобы засекать промежутки времени через которые приходит клиент Y
global_time_tic = time.perf_counter() # не нужно

client_num = 0


while True:
	signal.signal(signal.SIGINT, lambda *_: os._exit(1))  # выход Ctrl+C если не хочется ждать 10к человек
	toc = time.perf_counter()

	w_toc = [time.perf_counter() for i in range(n)]	
	minus = minus_f(w_toc,w_tic)	
	zero_indexes = []		


	for j in range(len(minus)):
		if minus[j]>=w_time_e[j] and w_time_e[j]>0:
			zero_indexes.append(j)
			#print('w_tic',w_tic)
			#print('w_toc',w_toc)
			#print('w_time_e',w_time_e)
			#print('zero_indexes',zero_indexes)

	if len(zero_indexes)>0:
		for el in zero_indexes:
			workers[el] = 0
			w_time_e[el] = 0
			w_tic[el] = 0
			print('====================')
			print('Работник №',el,'освободился')
			print('Клиент',client_num,'ушел') 
			print('Работники: ',workers)
			print('Очередь  : ',que)
			#print('w_time_e',w_time_e)
			client_num+=1                    
			print('====================')			
			#time.sleep(10)	



	elif i<=k-1 and toc - tic >= Y[i]:
		#print('I ====',i)
		print('====================')			
		print('Прошло : ',Y[i])
		print('Пришел клиент номер: ',i)
		que.append(1)
		print('Очередь: ',que)
		print('====================')
		i+=1
		tic = time.perf_counter()
	

	elif len(que)>0:
		#print('Очередь :',que)

		if workers_check(workers) == 1:
			avaible_workers = indexes(workers,0)	

			if len(avaible_workers)>1:
				print('====================')
				print('Работников >1, случайно выбираем')
				rand_index = workers_select(avaible_workers)
				workers[rand_index] = 1
				w_time_e[rand_index]= random.expovariate(1/l[rand_index])
				w_tic[rand_index] = time.perf_counter()
				que.pop()
				print('Выбран',rand_index,'работник')
				print('Работники: ',workers)
				print('Очередь  : ',que)
				print('Должен отпустить через: ',w_time_e[rand_index])
				print('====================')				
				#time.sleep(10)			

	
			elif len(avaible_workers)==1: 
				print('====================')
				print('Работников == 1')
				indx = indexes(workers,0)[0]
				workers[indx] = 1 
				w_time_e[indx]= random.expovariate(1/l[indx])
				w_tic[indx] = time.perf_counter()
				que.pop()
				print('Выбран',indx,'работник')
				print('Работники: ',workers)
				print('Очередь  : ',que)	
				print('Должен отпустить через: ',w_time_e[indx])			
				print('====================')
				#time.sleep(10)
