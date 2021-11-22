from math import log
from math import e

def ln(n):
    result = []
    for i in range(len(n)):
        if n[i] <= 0:
            result.append(None)
        else:
            result.append(log(n[i], e))
    return result

n = [float(i) for i in input().split()]
print(ln(n))






