carte1 = [1, 14] # As de pique
carte2 = [4, 4] # 4 de pique
carte3 = [1, 10] # 10 de trèfle
carte4 = [2, 11] # Valet de pique
carte5 = [1, 12] # Dame de coeur
carte6 = [1, 13] # Roi de carreau
carte7 = [1, 7] # 7 de coeur

mainPoker = [carte1, carte2, carte3, carte4, carte5, carte6, carte7]

def identifierCouleur(mainPoker):
    mainPoker = sortMainPoker(mainPoker)
    pique =0
    trefle = 0
    coeur = 0
    carreau = 0
    for c in mainPoker:
        if(c[0] == 1):
            pique+=1
        elif(c[0] == 2):
            trefle+=1
        elif(c[0] == 3):
            coeur+=1
        else:
            carreau+=1
    if(pique < 5 & trefle < 5 & coeur < 5 & carreau < 5):
        return -1
    elif(pique >= 5):
            return [5, troncatureTriCouleur(1, mainPoker)]
    elif(trefle >= 5):
        return [5, troncatureTriCouleur(2, mainPoker)]
    elif (coeur >= 5):
        return [5, troncatureTriCouleur(3, mainPoker)]
    elif (carreau >= 5):
        return [5, troncatureTriCouleur(4, mainPoker)]

def identifierSuite(mainPoker):
    mainPoker = sortMainPoker(mainPoker)
    liste = []
    for i in range(0, len(mainPoker)-1):
        suite = True
        nombre = 1
        c = i
        liste.append(mainPoker[i])
        while (suite == True) & (nombre < 5) & (c < len(mainPoker)-1):
            a = mainPoker[c+1][1]
            b = mainPoker[c][1]
            if (a-b) == 1:
                nombre+=1
                c+=1
                liste.append(mainPoker[c])
            else:
                liste = []
                suite=False
        if nombre == 5:
            break



def troncatureTriCouleur(couleur, mainPoker):
    liste = []
    for c in mainPoker:
        if(c[0] == couleur):
            liste.append(c[1])
        liste.sort(reverse=True)
    if(len(liste)>5):
        for i in range (5,len(liste)):
            liste.pop()
    return liste

#Retourne une liste triée selon la valeur des cartes
def sortMainPoker(mainPoker):
    return sorted(mainPoker, key= lambda colonnes: colonnes[1])

def main():
    print(identifierCouleur(mainPoker))
    identifierSuite(mainPoker)

if __name__ == '__main__':
    main()