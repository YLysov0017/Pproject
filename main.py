#a = [4, 8, 5]
#b = [7, 8, 7]
#res = []
#for c in a:
#        res.append(c*d)
#print(res)
import random
a = []
for v in range(11):
    k = random.randint(0, 500)
    a.append(k)
summa = 0
ss = 0
for i in a:
    summa += i
    ss += 1
avg = summa / ss
print(a)  
print(ss, avg, summa)