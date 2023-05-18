number = int(input())
no5 = number % 4
no4 = (number-no5)/4
possible = 1
if no4>=no5:
    no4 -= no5
else:
    possible = 0
while no4>=5:
    possible += 1
    no4 -= 5
print(possible)