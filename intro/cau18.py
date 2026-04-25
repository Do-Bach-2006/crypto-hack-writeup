def gcdExtended(a, b):
    global x, y
 
    if (a == 0):
        x = 0
        y = 1
        return b
 
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y
 
    x = y1 - (b // a) * x1
    y = x1
 
    return gcd
 
 
def modInverse(A, M):
 
    g = gcdExtended(A, M)
    if (g != 1):
        print("Inverse doesn't exist")
 
    else:
 
        res = (x % M + M) % M
        return res


M = 5 * 11 * 17
p1 = 5
p2 = 11
p3 = 17
a1 = 2
a2 = 3
a3 = 5
M1 = 11 * 17
M2 = 5 * 17
M3 = 5 * 11

y1 = modInverse(M1,p1)
y2 = modInverse(M2,p2)
y3 = modInverse(M3,p3)

flag = (a1*y1*M1 + a2*y2*M2 + a3*y3*M3) % M
print(flag)
