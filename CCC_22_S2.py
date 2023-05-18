a = int(input())
same = []
for i in range(a):
    same.append(input().split())
b = int(input())
apart = []
for i in range(b):
    apart.append(input().split())
c = int(input())
errors = 0
for i in range(c):
    thisgroup = input().split()
    for i1 in same:
        if i1[0] in thisgroup and i1[1] in thisgroup:
            errors += 1
            break
    for i1 in apart:
        if (i1[0] in thisgroup and not (i1[1] in thisgroup)) or (i1[1] in thisgroup and not(i1[0] in thisgroup)):
            errors += 1
            break
print(errors)