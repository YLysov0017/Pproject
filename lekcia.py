#замена цикла рекурсией
'''
def sumDigits(X):
    if X > 0:
        return (X % 10 + sumDigits(X//10))
    else:
        return 0
X = int(input())
print(sumDigits(X))
'''

#применение функции к элеентам коллекции
'''
from math import sin
B = list( map(sin, A)) 
'''
#генератор списков
'''
a = [i*i for i in range(N)]
'''
#поиск самой длинной строки в файле
'''
S = max(open("text.txt"), key = len)
'''
#отображение всех элементов массива, кубы которых больше 100
'''
for i in range(len(A)):
    if A[i]**3 > 100:   
        B.append(A[i])
print(B)
'''
#выборка элементов по условию и сортировка
'''
B = [x for x in A if x > 0]
B.sort()
'''
#заполнение массива
'''
A = [0] * N
'''
