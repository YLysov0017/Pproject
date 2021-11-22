def sort(a):
    b = []
    c = 0
    for i in range(len(a)):
        if a[i] != ' ' and a[i] != ',':
            if a[i] == '-':
                c = -(int(a[i + 1]))
                b.append(c)
            else:
                c = int(a[i])
                b.append(c)
    b = sorted(b)
    return b


a = input()
print(sort(a))
