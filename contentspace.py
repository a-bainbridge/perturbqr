from itertools import combinations

original = 6

def ecc(content):
    ec = content & 3
    return int(threebin(content)+threebin(ec),2)

def threebin(i):
    b = bin(i)[2:]
    b = "0"*(3-len(b)) + b
    return b

def dist(o,n):
    dif = bin(o ^ n)[2:]
    c = 0
    for ch in dif:
        c+=int(ch)
    return c


for combo in combinations(range(len(bin(original)[2:])),2):
    new = original
    for place in combo:
        new ^= (1 << place)
    print(new,threebin(new),dist(ecc(original),ecc(new)))
