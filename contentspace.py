from itertools import combinations

original = 6

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

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

def addsincrement(adds):
    carry = 1
    for i in range(len(adds)-1,-1,-1):
        adds[i]+=carry
        carry = 0
        if adds[i]==51:
            adds[i]=1
            carry = 1
    return adds

def permute(original,evfunc):
    tloc = original.find(".org")
    target = original[:tloc]+".tech/"+original[tloc+6:]
    i = 0
    j = 0
    best = 10**6
    beststr=''
    try:
        while True:
            for combo in combinations(range(len(target)),i):
                #new = target
                good = True
                for place in combo:
                    if alphabet.count(target[place])==0 or place<6 or tloc < place and tloc+6 > place:
                        good = False
                if good:
                    adds = [1]*len(combo)
                    while not adds == [50]*len(combo):
                        new = target
                        for place in range(len(combo)):
                            new = new[:combo[place]]+alphabet[(alphabet.index(target[combo[place]])+adds[place])%52]+new[combo[place]+1:]
                        j+=1
                        scre = evfunc(original,new)
                        if scre < best:
                            best = scre
                            beststr = new
                        print(new,beststr,best,j,end='\r')
                        adds = addsincrement(adds)
            i+=1
    except KeyboardInterrupt:
        print(new,beststr,best,j)
        return beststr

