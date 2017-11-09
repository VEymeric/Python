def VerifPartie2(jeu):
    liste = MetTabloSuite(jeu)
    essaiCouleur = identifierCouleur(jeu)
    essaieSuite = identifieSuite(liste)

    if essaiCouleur[0] != 5 and essaieSuite[0] == True :
        return identifieQuinteFlush(essaiCouleur[1])

    if essaiCouleur[0] != 5 :
        carteForte = essaiCouleur[1]
        return [5,carteForte[1]]

    if essaieSuite[0] == True:
        return [4, essaieSuite[1]]

    return [0]


def identifieQuinteFlush(carteCouleur):
    liste = MetTabloSuite(carteCouleur)
    essai = identifieSuite(liste)
    if essai[0] == True :
        if essai[1] == 14:
            return [9]
        else:
            return [8,essai[1]]


def identifierCouleur(mainPoker):
    pique =0 ; trefle = 0 ; coeur = 0 ; carreau = 0
    for c in mainPoker: #COmpte le nombre de carte dans chaque couleur
        if(c[0] == 1):
            pique+=1
        elif(c[0] == 2):
            trefle+=1
        elif(c[0] == 3):
            coeur+=1
        elif(c[0] == 4):
            carreau+=1
    if(pique < 5 and trefle < 5 and coeur < 5 and carreau < 5): #Choisi si 5 carte dans une couleur, passez a la suite.
        return [5, mainPoker]
    elif(pique >= 5):
        liste = TriCouleur(1, mainPoker)
        return [1, liste]
    elif(trefle >= 5):
        liste = TriCouleur(2, mainPoker)
        return [2, liste]
    elif (coeur >= 5):
        liste = TriCouleur(3, mainPoker)
        return [3, liste]
    elif (carreau >= 5):
        liste = TriCouleur(4, mainPoker)
        return [4, liste]


def identifieSuite(liste):
    """Dit si il y aune liste a partir d'un tablo avec nbr carte
    return : list avec [boolean,debutsuite,finsuite]
    """
    cpt = 0
    for i in range(len(liste)-1,-1,-1):
        if liste[i] == 0: #On repars a 0 pour le compte d ecarte de la suite
            cpt =0
        if liste[i] >= 1:
            cpt += 1
        if cpt == 5:
            #print("Il y a une suite qui termine en : \n",i+1," et qui commence en ",i+5)
            return [True,i+5,i+1]
    return [False,0,0]


def MetTabloSuite(liste): #Transforme le jeu du joueur en valeur dans le tablo "grosseur"
    tablo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]
    for i in liste:
        tablo = (TriValeur(tablo, i))
    return tablo


def TriValeur(liste,carte): #place la valeur de la carte dans la liste]
    if carte[1] == 14 :
        liste[0]+=1
    if carte[1] == 2 :
        liste[1]+=1
    if carte[1] == 3 :
        liste[2]+=1
    if carte[1] == 4 :
        liste[3]+=1
    if carte[1] == 5 :
        liste[4]+=1
    if carte[1] == 6 :
        liste[5]+=1
    if carte[1] == 7 :
        liste[6]+=1
    if carte[1] == 8 :
        liste[7]+=1
    if carte[1] == 9 :
        liste[8]+=1
    if carte[1] == 10 :
        liste[9]+=1
    if carte[1] == 11:
        liste[10]+=1
    if carte[1] == 12 :
        liste[11]+=1
    if carte[1] == 13 :
        liste[12]+=1
    if carte[1] == 14:
        liste[13]+=1
    return liste


def TriCouleur(couleur, mainPoker):
    liste = []
    for c in mainPoker:
        if(c[0] == couleur):
            liste.append(c)
        liste.sort(reverse=True) #Tri l liste dans l'oredre decrosiseant

    return liste






def main():
    carte1 = [2, 14]  # As de pique
    carte2 = [4, 4]  # 4 de pique
    carte3 = [1, 10]  # 10 de trèfle
    carte4 = [2, 5]  # Valet de pique
    carte5 = [1, 12]  # Dame de coeur
    carte6 = [1, 3]  # Roi de carreau
    carte7 = [1, 11]  # 7 de coeur

    jeu = [carte1, carte2, carte3, carte4, carte5, carte6, carte7]

    #print(identifierCouleur(jeu))
    print(VerifPartie2(jeu))

if __name__ == '__main__':
    main()