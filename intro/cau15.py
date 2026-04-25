p = 29
numbers = [14,6,11]

for num in numbers:
    for i in range(0, p+1):
        if i ** 2 % p == num:
            print(i)


