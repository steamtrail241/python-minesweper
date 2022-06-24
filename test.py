

class thigy():
    mylist = []

    def __init__(self) -> None:
        self.a = 1
        self.b = 2

mylist2 = []

for i in range(10):
    mylist3 = []
    for i1 in range(10):
        new1 = thigy()
        mylist3.append(new1)
    mylist2.append(mylist3)
    mylist3[0].mylist.append(mylist3)

print(mylist2[0][0].mylist)