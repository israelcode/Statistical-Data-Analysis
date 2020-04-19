# -*- coding: utf-8 -*-
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from random import randrange
import pylab as p

def gen1(mu,sigma,n):
    i=0
    list = []
    while i<n-1:
        list.append(random.normalvariate(mu, sigma))
        i+=1
    return(list)



def gen2(j,sigma,n):
    i=0
    u = []
    v = []
    w = []
    z = []
    while i<n-1:
        u.append(random.normalvariate(0, 5))
        v.append(random.normalvariate(0, sigma))
        w.append(random.uniform(0, 5))
        i+=1

    i = 0
    for el in w:
        if w[i]>j:
            z.append(u[i])
            i+=1
        elif w[i]<j:
            z.append(v[i]) 
            i+=1

    print(u)
    print(v)
    print(w)
    print(z)




def gen3(thetta,j,sigma,n):
    i=0
    u = []
    v = []
    w = []
    z = []
    while i<n-1:
        u.append(random.normalvariate(thetta, 5))
        v.append(random.normalvariate(thetta, sigma))
        w.append(random.uniform(thetta, 5))
        i+=1

    i = 0
    for el in w:
        if w[i]>j:
            z.append(u[i])
            i+=1
        elif w[i]<j:
            z.append(v[i]) 
            i+=1
    #print(u)
    #print(v)
    #print(w)
    #print(z)

    return(z)


#gen3(0,0.5,1,10)



def stud(X,Y):
    Xm = np.mean(X)
    Ym = np.mean(Y)   

    sum1 = 0
    i = 0
    m = len(X)-1
    while i<=m:
        sum1+=(X[i]-Xm)**2
        i+=1

    sum2 = 0
    i = 0
    n = len(Y)-1
    while i<=n:
        sum2+=(Y[i]-Ym)**2
        i+=1

    S = 1/(m+1+n+1-2)*(sum1+sum2)
    T = (Xm-Ym)/(math.sqrt(S*(1/(m+1)+1/(n+1))))
    print(Xm,Ym,'\n','sum1,2:',sum1,',',sum2,'\n','S:',S,'T:',T)

    if (T>=-2.1) and (T<=2.1): # попадает ли в ДО
        return(1)    
    else:
        return(0)





def wilk(X,Y):
    XX = []
    for el in X:
        XX.append([el,'X'])

    YY = []
    for el in Y:
        YY.append([el,'Y'])

    untd = XX + YY
    untd = sorted(untd, key=lambda untd: untd[0])
    
    W = 0
    i = 1
    for el in untd:
        if el[1]=='Y':
            W+=i
            i+=1
        else:
            i+=1
    
    m = len(X)
    n = len(Y) 

    mw = n/2*(m+n+1)
    dw = (m*n)/12*(m+n+1)
    
    w_final = (W - mw)/(math.sqrt(dw))
    print('m,n',m,n,'\n','mw,dw',mw,dw,'\n','w_final',w_final)

    if (w_final>=-2.4) and (w_final<=2.4): # попадает ли в ДО -2.9 2.9
        return(1)    
    else:
        return(0)

#test1 = [560,580,600,420,530,490,580,740]
#test2 = [692,700,621,640,561,680,630]
#stud(test1,test2)
#wilk(test1,test2)




'''
# сначала без выбросов
# для каждой тетты от 0.1 до 1 с шагом 0.1 
# генерирую по 100 выборок X = gen3(0,0,1,101) Y = gen3(0+t,0,1,101). Y отличается средним 
# далее считаю частоту того, что гипотезу примут(H0: thetta = 0)

# график тетта(прибавляем тетту к М.О. у Y!!) от вероятности попадания в доверит область. Критерий стюдента более точный. Это вероятность ошибки при различных тетта. Чем больше тетта тем меньше ошибка, но стьюдент точнее

P1 = [] # stud
P2 = [] # wilk
T = []
t = 0.1

while t<=1:
    T.append(t)
    res1 = 0
    res2 = 0
    counter = 1
    while counter <=100:

        X = gen3(0,0,1,101) 
        Y = gen3(0+t,0,1,101)  
        stud_res = stud(X,Y)
        #print('stud_res',stud_res)

        wilk_res = wilk(X,Y)
        #print('wilk_res',wilk_res)

        if stud_res == 1:
            res1+=1
        if wilk_res == 1:
            res2+=1
        counter+=1

    print(res1,res1)
    res1=res1/100
    res2 = res2/100
    P1.append(res1) # stud
    P2.append(res2) # wilk
    t+=0.05


plt.xlabel("Thetta")
plt.ylabel("P")
plt.plot(T, P1,'r', label='student')  
plt.plot(T, P2,'g', label='wilcoxon') 
plt.legend()
plt.show()
plt.close()

'''


'''

# зашумленность от вероятности попадание в ДО. при МО 0 и 2
# НЕ ЗАБУДЬ ПОМЕНЯТЬ СИГМУ В ГЕН 3, ЩАС ДЛЯ 3 случая = 5, а должна быть = 3

P1 = [] # stud
P2 = [] # wilk
T = []
t = 0

while t<=1:
    T.append(t)
    res1 = 0
    res2 = 0
    counter = 1
    while counter <=300:

        X = gen3(0,t,10,101) 
        Y = gen3(2,t,10,101)  
        stud_res = stud(X,Y)
        #print('stud_res',stud_res)

        wilk_res = wilk(X,Y)
        #print('wilk_res',wilk_res)

        if stud_res == 1:
            res1+=1
        if wilk_res == 1:
            res2+=1
        counter+=1
# по y - вероятност принять 1
    print(res1,res1)
    res1=res1/250
    rnd = np.random
    res2 = res2/250
    P1.append(res1) # stud
    P2.append(res2) # wilk
    print(P1)
    t+=0.1

p.xlabel("j")
p.ylabel("P")
p.plot(T, P1,'r', label='student') #
p.plot(T, P2,'g', label='wilcoxon')
p.ylim(0, 1)
p.legend()
p.show()
p.close()



'''



# def gen3(thetta,j,sigma,n):


# тоже самое, только, если дсперсию Y увеличивать от 1 до 10(резко) и зашумл 10%. Критерий Вилкоксона меньше реагир на дисперсию

P1 = [] # stud
P2 = [] # wilk
T = []
t = 1

while t<=20:
    T.append(t)
    res1 = 0
    res2 = 0
    counter = 1
    while counter <=300:

        X = gen3(0,0.3,5+t,101) 
        Y = gen3(2,0.3,5+t,101)  
        stud_res = stud(X,Y)
        #print('stud_res',stud_res)0.1
        wilk_res = wilk(X,Y)
        #print('wilk_res',wilk_res)

        if stud_res == 1:
            res1+=1
        if wilk_res == 1:
            res2+=1
        counter+=1

    print(res1,res1)
    res1=res1/300
    res2 = res2/300
    P1.append(res1) # stud
    P2.append(res2) # wilk
    t+=2


p.xlabel("sigma")
p.ylabel("P")
p.plot(T, P1,'r', label='student') 
p.plot(T, P2,'g', label='wilcoxon')
p.ylim(0, 1)
p.legend()
p.show()
p.close()



# сдвиг есть МО 0 и 2
# Попробовать менять силу и шум выбросов на двух графиках



