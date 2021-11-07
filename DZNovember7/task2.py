def spisokchisel(n):
    a = []
    a.append(n - 1)
    a.append(n + 1)
    return(a)

n = int(input())
print(spisokchisel(n))
