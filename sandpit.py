from collections import Counter

def quantify(i):
    new = i
    l = []
    for row in new:
        for pixel in row:
            l.append((pixel[0],pixel[1],pixel[2]))
    return Counter(l)

