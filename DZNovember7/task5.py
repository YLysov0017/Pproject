def dicts(spisok1, spisok2):
    result = []
    if len(spisok1) == len(spisok2):
        for keys in zip(spisok1, spisok2):
            result.append(keys)
    else:
        return 'Списки имеют разную длину'
    return dict(result)

spisok1 = list(input().rsplit())
spisok2 = list(input().rsplit())
print(dicts(spisok1, spisok2))

