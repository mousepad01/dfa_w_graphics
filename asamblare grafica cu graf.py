from graphics import *
import random
import math


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
        output = Text(Point(1300, 80), 'Acceptat')
        output.setTextColor(color_rgb(255, 0, 0))
        output.draw(win)
        win.getMouse()
        quit()
    elif not string and node not in lfin:
        return

    if node in d.keys():

        lv = ls[d[node]].getvecini()

        for v in range(len(lv)):
            if string[0] == ls[d[node]].gettranz(v):
                check(string[1:], lv[v])

    output = Text(Point(1300, 80), 'Neacceptat')
    output.setTextColor(color_rgb(255, 0, 0))
    output.draw(win)
    win.getMouse()
    quit()


def drawnode(p, val):

    st = Circle(p, 20)
    st.setFill(color_rgb(255, 255, 0))

    st.draw(win)

    txt = Text(p, val)
    txt.setTextColor(color_rgb(0, 0, 255))
    txt.draw(win)


def markendstate(p):

    mark = Circle(p, 28)
    mark.setOutline(color_rgb(255, 255, 0))
    mark.setWidth(3)

    mark.draw(win)


def drawarc(p1, p2, h, hredrate,  hrec, stack_points, concav):

    if hrec < 5:
        x1 = p1.getX()
        x2 = p2.getX()
        y1 = p1.getY()
        y2 = p2.getY()

        xm = (x1 + x2) // 2
        ym = (y1 + y2) // 2

        if x2 != xm:
            k = (ym - y2) / concav * (x2 - xm)
            const = math.sqrt((h * h) / (k * k + 1))

            y = ym - const
            x = xm - k * const
        else:
            y = ym
            x = xm - h

        pnew = Point(x, y)

        stack_points = drawarc(p1, pnew, h * hredrate, hredrate / 2, hrec + 1, stack_points, concav)
        stack_points.append(pnew)
        stack_points = drawarc(pnew, p2, h * hredrate, hredrate / 2, hrec + 1, stack_points, concav)

    return stack_points


def drawtransition(p1, p2, narcs, val):

    if narcs == 0:

        tr = Line(p1, p2)

        xm = (p1.getX() + p2.getX())//2
        ym = (p1.getY() + p2.getY())//2

        txt = Text(Point((p1.getX() + xm)//2 + 10, (p1.getY() + ym)//2 + 10), val)
        txt.setTextColor(color_rgb(0, 0, 255))
        txt.draw(win)

        tr.setOutline(color_rgb(0, 0, 255))

        tr.draw(win)

        draw_arrow(p1, p2)

    elif narcs > 0:

        stack_points = drawarc(p1, p2, 30 * narcs, 0.4, 1, [p1], 1)
        stack_points.append(p2)

        for ip in range(len(stack_points) - 1):

            if ip == (len(stack_points) - 1) / 2:
                txt = Text(stack_points[ip], val)
                txt.setTextColor(color_rgb(0, 0, 255))
                txt.draw(win)

            dx = Line(stack_points[ip], stack_points[ip + 1])
            dx.setOutline(color_rgb(0, 0, 255))

            dx.draw(win)
        '''tr = Line(p1, Point())
        tr.setOutline(color_rgb(0, 0, 255))

        tr.draw(win)'''


def draw_arrow(p1, p2):

    x1 = p1.getX()
    y1 = p1.getY()
    x2 = p2.getX()
    y2 = p2.getY()

    xm = (x1 + x2) // 2
    ym = (y1 + y2) // 2

    if x2 <= x1 and y2 >= y1:
        arrow = Polygon(Point(xm, ym), Point(xm, ym - 15), Point(xm + 15, ym))

    elif x2 <= x1 and y2 <= y1:
        arrow = Polygon(Point(xm, ym), Point(xm + 15, ym), Point(xm, ym + 15))

    elif x2 >= x1 and y2 <= y1:
        arrow = Polygon(Point(xm, ym), Point(xm - 15, ym), Point(xm, ym + 15))

    elif x2 >= x1 and y2 >= y1:
        arrow = Polygon(Point(xm, ym), Point(xm - 15, ym), Point(xm, ym - 15))

    arrow.setFill(color_rgb(0, 0, 255))

    arrow.draw(win)


def check_drawn(p):

    global already_state_set

    for state in already_state_set:

        if 400 > (p.getX() - state.getX()) ** 2 + (p.getY() - state.getY()) ** 2:  # verificarea distantei intre puncte < raza fixa a starii == 20 px
            return True, state

    return False, p


def check_trans(p1, p2):

    for v in range(len(already_trans_set[p1][0])):

        if already_trans_set[p1][0][v] == p2:

            return already_trans_set[p1][1][v]

    return 0


# global


win = GraphWin("test grafica", 1400, 800)

win.setBackground(color_rgb(0, 0, 0))

textEntry = Entry(Point(1300, 50), 60)
textEntry.draw(win)

already_state_set = set()  # multime ce retine daca intr o anumita raza exista deja o stare

already_trans_set = {}  # dictionar ce retine daca deja exista o tranzitie intre doua stari

st_to_point = {}  # dictionar de legatura intre numele starii si punctul grafic corespunzator

win.getMouse()
s = textEntry.getText()
n = int(s)
print("n introdus. introduceti perechile de stari")

ls = []  # lista starilor
d = {}  # dictionar de forma nume: indicele din lista starilor pt starea cu acel nume

for i in range(n):

    win.getMouse()
    s = textEntry.getText()
    l = s.split()
    print("perechea", i, " de stari introdusa")

    if l[0] in d.keys():
        ls[d[l[0]]].update(l[1], l[2])
    else:
        ob = Stare(l[0], [l[1]], [l[2]])
        ls.append(ob)
        d.update({l[0]: len(ls) - 1})

    initial_state = win.getMouse()
    end_state = win.getMouse()

    check_init = check_drawn(initial_state)
    check_end = check_drawn(end_state)

    #print(check_init, check_end)

    if check_init[0]:
        initial_state = check_init[1]

    if check_end[0]:
        end_state = check_end[1]

    if l[0] not in st_to_point.keys():
        st_to_point.update({l[0]: initial_state})

    if l[1] not in st_to_point.keys():
        st_to_point.update({l[1]: end_state})

    if initial_state not in already_trans_set.keys():
        already_trans_set.update({initial_state: [[], []]})

    if end_state not in already_trans_set.keys():
        already_trans_set.update({end_state: [[], []]})

    #print(already_trans_set)

    narcs = max(check_trans(initial_state, end_state), check_trans(end_state, initial_state))

    #print(narcs)

    if not check_init[0]:

        drawnode(initial_state, l[0])

        already_state_set.add(initial_state)

    if not check_end[0]:

        drawnode(end_state, l[1])

        already_state_set.add(end_state)
        already_trans_set[initial_state][0].append(end_state)
        already_trans_set[initial_state][1].append(1)
    else:
        count_trans = False
        for j in range(len(already_trans_set[initial_state][0])):

            if already_trans_set[initial_state][0][j] == end_state:

                already_trans_set[initial_state][1][j] += 1
                count_trans = True

        if not count_trans:
            already_trans_set[initial_state][0].append(end_state)
            already_trans_set[initial_state][1].append(1)

    if check_end[0] and check_init[0] and narcs > 0:
        drawtransition(initial_state, end_state, narcs, l[2])
    else:
        drawtransition(initial_state, end_state, 0, l[2])

win.getMouse()
s = textEntry.getText()
lfin = s.split()
print("starile finale introduse")

for i in range(len(lfin)):
    markendstate(st_to_point[lfin[i]])

win.getMouse()
startnodename = textEntry.getText()
print("stare initiala introdusa")

win.getMouse()
cuv = textEntry.getText()
print("cuvant de verificat introdus")

if not cuv and startnodename in lfin:
    output = Text(Point(1300, 80), 'Acceptat')
    output.setTextColor(color_rgb(255, 0, 0))
    output.draw(win)
    win.getMouse()
    quit()
elif not cuv and startnodename not in lfin:
    output = Text(Point(1300, 80), 'Neacceptat')
    output.setTextColor(color_rgb(255, 0, 0))
    output.draw(win)
    win.getMouse()
    quit()

check(cuv, startnodename)

win.getMouse()
win.getMouse()




