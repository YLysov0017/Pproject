'''
все четные или не нечетные числа из списка и

программа останавливается когда находит заданное число
'''
'''
программа прверяет, является ли строка палиндромом
'''
'''
import random
listik = [random.randint(0, 1000) for i in range(100)]
print('Вывод нечетных чисел')
for i in listik:
    if i % 2 == 1:
        print(i)
        if i == 195:
            print(i, 'найдено ключевое число')
            break
'''

stroka = input()
def is_palindrom(stroka):
    for i in range(1, len(stroka)):
        if stroka[i - 1] == stroka[-i]:
            continue
        else:
            print('не является палиндромом')
            break
    else:
        print('является палиндромом')
    return 'the end'
print(is_palindrom(stroka))
