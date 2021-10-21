# Программа проверяет все четные или не нечетные числа из списка и
#останавливается когда находит заданное число

'''
def chisla():
    A = [int(i) for i in range(1000)]
    B = []
    chetnost = input('Какие числа нужно проверить, четные или нечетные?')
    key = int(input('Введите ключевое число этой четности'))
    if chetnost != 'четные' and chetnost != 'нечетные':
        return 'Неверные данные. Попробуйте еще раз.'
    elif (chetnost == 'нечетные' and key % 2 == 0) or (chetnost == 'четные' and key % 2 == 1):
        return 'Четность ключевого числа не совпадает с введенной. Попробуйте еще раз.'
    elif chetnost == 'четные' and key % 2 == 0:
        print('Вывод четных чисел')
        for i in A:
            if i % 2 == 0:
                B.append(i)
                if i == key:
                    print(*B, 'найдено ключевое число')
                    break
    elif chetnost == 'нечетные' and key % 2 == 1:
        print('Вывод нечетных чисел')
        for i in A:
            if i % 2 == 1:
                B.append(i)
                if i == key:
                    print(*B, 'найдено ключевое число')
                    break
    return 'Программа завершена'



print(chisla())
'''


#Программа проверяет, является ли строка палиндромом

'''
stroka = input()
def palindrom(stroka):
    for i in range(1, len(stroka)):
        if stroka[i - 1] == stroka[-i]:
            continue
        else:
            print('не является палиндромом')
            break
    else:
        print('является палиндромом')
    return 'Программа завершена'
print(palindrom(stroka))
'''