class Stare:

    def __init__(self, name, vecini, tranzitii):
        self.__name = name
        self.__vecini = vecini
        self.__tranzitii = tranzitii

    def update(self, nv, nt):
        self.__vecini.append(nv)
        self.__tranzitii.append(nt)

    def getname(self):
        return self.__name

    def getvecini(self):
        return self.__vecini

    def gettranz(self, iv):
        return self.__tranzitii[iv]


def check(string, node):

    global d
    global ls

    if not string and node in lfin:
        print("acceptat")
        quit()
    elif not string and node not in lfin:
        return

    if node in d.keys():

        lv = ls[d[node]].getvecini()

        for v in range(len(lv)):
            if string[0] == ls[d[node]].gettranz(v):
                check(string[1:], lv[v])

    print("neacceptat")
    quit()


n = int(input())

ls = []  # lista starilor
d = {}  # dictionar de forma nume: indicele din lista starilor pt starea cu acel nume

for i in range(n):

    s = input()
    l = s.split()

    if l[0] in d.keys():
        ls[d[l[0]]].update(l[1], l[2])
    else:
        ob = Stare(l[0], [l[1]], [l[2]])
        ls.append(ob)
        d.update({l[0]: len(ls) - 1})

s = input()
lfin = s.split()

startnodename = input()

cuv = input()
if not cuv and startnodename in lfin:
    print("acceptat")
    quit()
elif not cuv and startnodename not in lfin:
    print("neacceptat")
    quit()

check(cuv, startnodename)


