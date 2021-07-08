from random import randint
from tkinter import *

def closeapp():
    global side
    side = int(e1.get())
    master.destroy()    #lancement de la génération

master = Tk()
master.geometry("300x300")
master.title("LE LABYRINTHIQUE")

Label(master, text="Nombre de cases de côté").place(x=85, y=80)
e1 = Entry(master)
e2 = Button(master, text="Générer", command=closeapp)
e1.place(width=50, x=130, y=100)
e2.place(width=50, height=25, x=130, y=200)
text=Label(master,text="Appuyer sur p pour lancer la résolution")
text.place(x=60,y=160)

master.mainloop()


size = 600 // side
placestart = randint(0, side ** 2 - 1)
placefinish=placestart
while placefinish==placestart:
    placefinish = randint(0, side ** 2 - 1)
sizebis = size // 2
u = 0
b = str(size * side) + 'x' + str(size * side)
track = [placestart]
att = []
numCase = []
check = 1
grouplist = []
#Initialisation des variables

def recreaBis():
    global u
    if u < len(track):
        if track[u] == track[u - 1] + 1:
            can.itemconfig(image, image=ResearchB)
        if track[u] == track[u - 1] - 1:
            can.itemconfig(image, image=ResearchH)
        if track[u] == track[u - 1] + side:
            can.itemconfig(image, image=ResearchD)
        if track[u] == track[u - 1] - side:
            can.itemconfig(image, image=ResearchG)
        ob.case = track[u]
        ob.x = (ob.case // side) * size + sizebis
        ob.y = (ob.case % side) * size + sizebis
        can.coords(image, ob.x, ob.y)
        u = u + 1
        can.after(150, recreaBis)
    else:
        u = 0

def recreate(event):
    recreaBis()

def escape(event):
    win.destroy()

class object():
    def __init__(self, x, y, case):
        self.x = x
        self.y = y
        self.case = case

ob = object(sizebis, sizebis, placestart)

class case:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.murdroite = True
        self.murbas = True
        self.checked = False
#Création de la classe case

class group:
    def __init__(self, value, list):
        self.value = value
        self.list = list#Création des unions de cellules

for p in range(side):
    for i in range(side):  # Création des cases
        numCase.append(case(p, i))


for i in range(side ** 2):
    grouplist.append(group(i, [i])) #Création des listes d'unions


def convertlist(reference):
    for i in grouplist[reference].list:
        grouplist[i].value = grouplist[reference].value
        grouplist[i].list = grouplist[reference].list
#Fonction permettant de remplacer les valeurs des cellules nouvellement fusionnées

def genlab():
    global check
    while check != 0:
        check = 0
        destroy_pos = randint(0, side ** 2 - 1)
        destroy_droite_ou_bas = randint(0, 1)
        if destroy_droite_ou_bas == 0 and destroy_pos + 1 < (side ** 2 - side):
            if grouplist[destroy_pos].value > grouplist[destroy_pos + side].value:
                numCase[destroy_pos].murdroite = False
                grouplist[destroy_pos].value = grouplist[destroy_pos + side].value
                grouplist[destroy_pos + side].list += grouplist[destroy_pos].list
                convertlist(destroy_pos + side)
            elif grouplist[destroy_pos].value < grouplist[destroy_pos + side].value:
                numCase[destroy_pos].murdroite = False
                grouplist[destroy_pos + side].value = grouplist[destroy_pos].value
                grouplist[destroy_pos].list += grouplist[destroy_pos + side].list
                convertlist(destroy_pos)
        elif destroy_droite_ou_bas == 1 and destroy_pos % side != side - 1:
            if grouplist[destroy_pos].value > grouplist[destroy_pos + 1].value:
                numCase[destroy_pos].murbas = False
                grouplist[destroy_pos].value = grouplist[destroy_pos + 1].value
                grouplist[destroy_pos + 1].list += grouplist[destroy_pos].list
                convertlist(destroy_pos + 1)
            elif grouplist[destroy_pos].value < grouplist[destroy_pos + 1].value:
                numCase[destroy_pos].murbas = False
                grouplist[destroy_pos + 1].value = grouplist[destroy_pos].value
                grouplist[destroy_pos].list += grouplist[destroy_pos + 1].list
                convertlist(destroy_pos)
        for i in range(side ** 2 ):
            check += grouplist[i].value
    for i in range((side**2)//10):
        destroy_pos=randint(0,side**2)
        destroy_droite_ou_bas=randint(0,1)
        if destroy_pos % side != side - 1 and destroy_pos + 1 < (side ** 2 - side):
            if destroy_droite_ou_bas==0:numCase[destroy_pos].murdroite=False
            if destroy_droite_ou_bas==1:numCase[destroy_pos].murbas=False
#Génération du labyrinthe

def pathfind():
    global att
    global track
    global size
    global sizebis
    global placestart
    global placefinish
    global finalpath
    reste = 0
    bas,droite,haut,gauche = False,False,False,False
    ob.case = placestart
    ob.x = sizebis
    ob.y = sizebis
    while ob.case != placefinish:
        reste = 0
        if numCase[ob.case].murbas is False and numCase[ob.case + 1].checked is False:
            bas = True
        if numCase[ob.case].murdroite is False and numCase[ob.case + side].checked is False:
            droite = True
        if numCase[ob.case - 1].murbas is False and (ob.case - 1) % side != side - 1 and numCase[
            ob.case - 1].checked is False:
            haut = True
        if numCase[ob.case - side].murdroite is False and ob.case > side - 1 and numCase[
            ob.case - side].checked is False:
            gauche = True
        if bas:
            if droite:
                att = [ob.case + side] + att
                numCase[ob.case + side].checked = True
            if haut:
                att = [ob.case - 1] + att
                numCase[ob.case - 1].checked = True
            if gauche:
                att = [ob.case - side] + att
                numCase[ob.case - side].checked = True
            numCase[ob.case].checked = True
            movebas(0)
            reste = 1
            bas = False
            droite = False
            haut = False
            gauche = False
        if droite:
            if haut:
                att = [ob.case - 1] + att
                numCase[ob.case - 1].checked = True
            if gauche:
                att = [ob.case - side] + att
                numCase[ob.case - side].checked = True
            numCase[ob.case].checked = True
            movedroite(0)
            bas = False
            droite = False
            haut = False
            gauche = False
            reste = 1
        if haut:
            if gauche:
                att = [ob.case - side] + att
                numCase[ob.case - side].checked = True
            numCase[ob.case].checked = True
            movehaut(0)
            bas = False
            droite = False
            haut = False
            gauche = False
            reste = 1
        if gauche:
            numCase[ob.case].checked = True
            movegauche(0)
            bas = False
            droite = False
            haut = False
            gauche = False
            reste = 1
        if reste == 0:
            if not att:
                ob.case = 0
                ob.x = sizebis
                ob.y = sizebis
                can.coords(image, ob.x, ob.y)
                track = []
                break
            if ob.case == placefinish:
                break
            numCase[ob.case].checked = True
            ob.case = att[0]
            del att[0]
            ob.x = (ob.case // side) * size + sizebis
            ob.y = (ob.case % side) * size + sizebis
            can.coords(image, ob.x, ob.y)
        track = track + [ob.case]
    ob.case = placestart
    ob.x = (ob.case // side) * size + sizebis
    ob.y = (ob.case % side) * size + sizebis
    can.coords(image, ob.x, ob.y)
    test = True
    for i in range(len(track) - 1, 0, -1):
        if track[i] != track[i - 1] + 1 and track[i] != track[i - 1] - 1 and track[i] != track[i - 1] + side and track[
            i] != track[i - 1] - side:
            del track[i - 1]
    while test:
        test = False
        for i in range(len(track) - 1, 1, -1):
            check = track[i] - track[i - 1]
            if check == -1 and numCase[track[i]].murbas:
                del track[i - 1]
                test = True
            if check == 1 and numCase[track[i - 1]].murbas:
                del track[i - 1]
                test = True
            if check == -side and numCase[track[i]].murdroite:
                del track[i - 1]
                test = True
            if check == side and numCase[track[i - 1]].murdroite:
                del track[i - 1]
                test = True
        for i in range(len(track) - 1, 0, -1):
            if track[i] != track[i - 1] + 1 and track[i] != track[i - 1] - 1 and track[i] != track[i - 1] + side and \
                    track[i] != track[i - 1] - side:
                del track[i - 1]
    finalpath = []
    for i in range(1, len(track)):
        if track[i] == track[i - 1] + 1:
            finalpath = finalpath + ['Bas']
        if track[i] == track[i - 1] - 1:
            finalpath = finalpath + ['Haut']
        if track[i] == track[i - 1] + side:
            finalpath = finalpath + ['Droite']
        if track[i] == track[i - 1] - side:
            finalpath = finalpath + ['Gauche']
#Résolution du labyrinthe

genlab()

win = Tk()
win.title('LE LABYRINTHIQUE')
win.geometry(b)

can = Canvas(win)
can.focus_set
can.place(x=0, y=0)
can.configure(width=size * side, height=size * side)

carre1 = can.create_rectangle((placestart // side) * size + (size // 15), (placestart % side) * size + (size // 15),
                              (placestart // side) * size + size - (size // 15),
                              (placestart % side) * size + size - (size // 15), fill='green',
                              outline='white')
carre2 = can.create_rectangle((placefinish // side) * size + (size // 15), (placefinish % side) * size + (size // 15),
                              (placefinish // side) * size + size - (size // 15),
                              (placefinish % side) * size + size - (size // 15), fill='red',
                              outline='white')
#Affichage des points de départ et d'arrivée

for i in range(side ** 2):
    if numCase[i].murdroite:
        ligne = can.create_line((numCase[i].posx + 1) * size, (numCase[i].posy) * size, (numCase[i].posx + 1) * size,
                                (numCase[i].posy + 1) * size)
#Affichage des murs verticaux

for i in range(side ** 2):
    if numCase[i].murbas:
        ligne = can.create_line(numCase[i].posx * size, (numCase[i].posy + 1) * size, (numCase[i].posx + 1) * size,
                                (numCase[i].posy + 1) * size)
#Affichage des murs verticaux

ResearchD = PhotoImage(file='Researcher_droite.png')
ResearchG = PhotoImage(file='Researcher_gauche.png')
ResearchH = PhotoImage(file='Researcher_haut.png')
ResearchB = PhotoImage(file='Researcher_bas.png')
image = can.create_image(ob.x, ob.y, image=ResearchB)
#Importation des positions du personnage

def movedroite(event):
    global side
    if not numCase[ob.case].murdroite:
        can.itemconfig(image, image=ResearchD)
        ob.x = ob.x + size
        can.coords(image, ob.x, ob.y)
        ob.case = ob.case + side

def movegauche(event):
    global side
    if numCase[ob.case - side].murdroite == False and ob.case > side - 1:
        can.itemconfig(image, image=ResearchG)
        ob.x = ob.x - size
        can.coords(image, ob.x, ob.y)
        ob.case = ob.case - side

def movehaut(event):
    global side
    if numCase[ob.case - 1].murbas == False and (ob.case - 1) % side != side - 1:
        can.itemconfig(image, image=ResearchH)
        ob.y = ob.y - size
        can.coords(image, ob.x, ob.y)
        ob.case = ob.case - 1

def movebas(event):
    global side
    if not numCase[ob.case].murbas:
        can.itemconfig(image, image=ResearchB)
        ob.y = ob.y + size
        can.coords(image, ob.x, ob.y)
        ob.case = ob.case + 1
#Déplacement du personnage

win.bind('<Right>', movedroite)
win.bind('<Left>', movegauche)
win.bind('<Up>', movehaut)
win.bind('<Down>', movebas)
win.bind('<Escape>', escape)
win.bind('<KeyPress-p>', recreate)
#Assignement des touches

pathfind()
win.mainloop()