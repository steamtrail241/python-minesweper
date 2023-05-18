mapsize = int(input())
trees = int(input())
listOfTrees = []
for i in range(trees):
    tree = input().split(" ")
    listOfTrees.append([int(tree[0])-1, int(tree[1])-1])
biggest = 1

for i in range(mapsize):
    for i1 in range(mapsize):
        if not [i, i1] in listOfTrees and i+biggest-1<mapsize and i1+biggest-1<mapsize:
            clear = True
            for i3 in listOfTrees:
                if i3[0]>=i and i3[0]<=i+biggest-1 and i3[1]>=i1 and i3[1]<=i1+biggest-1:
                    clear = False
                    break
            count = biggest
            while clear:
                for i2 in range(count):
                    if ((([i+count-1, i1+i2]) in listOfTrees) or (([i+i2, i1+count-1]) in listOfTrees) or i+count-1 >= mapsize or i1+count-1 >= mapsize):
                        clear = False
                        break
                count += 1
            count -= 2
            if count > biggest:
                biggest = count
print(biggest)