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


def DetermineMeilleur(jeu):
    v1 = VerifPartie1(jeu)
    v2 = VerifPartie2(jeu)

    if v1[0] > v2[0] :
        return v1
    elif v1[0] == v2[0]:
        tablo = MetTablo(jeu)
        return [0,TrouveCarteHaute(tablo,0,0)]
    else:
        return v2


def VerifPartie1(jeu):
    tablo = MetTablo(jeu)
    resultat = Identifie(tablo)
    return resultat


def TrouveCarteHaute(tablo,max1,max2):
    #print("Trouver :",tablo , max1,max2)
    for i in range(len(tablo) - 1, -1, -1): #Comment a len(tablo)-1, jusqu'a -1 par pas de -1
        if tablo[i] != 0 and i != max1 and i != max2:
            return i


def Identifie(tablo):
    #print(tablo)
    cpt = 0
    brelan = []
    paire = []
    for i in tablo: #recupete la valeur de carte de la figure
        cpt += 1
        if i == 4:
            #print("Carré de : ", cpt+1)
            return [7,cpt+1] # [valeur de la figure, valeur des carte]
        if i == 3:
            brelan.append(cpt+1)
        if i == 2:
            paire.append(cpt+1)
    ###################################### A partir de maintenant, determine les figures
    #print("Liste Paire :",paire,"taille",len(paire))
    if len(brelan) > 0 and len(paire)>0:
        return [6,max(brelan)] # [valeur de la figure, valeur des carte du brelan ]
    if len(brelan) > 0:
        return [3, max(brelan)] # [valeur de la figure, valeur des carte du brelan]
    if len(paire) > 1:
        #print("Liste Paire :",paire)
        max1 = max(paire)
        paire.sort()
        paire.pop()
        max2 = max(paire)
        ch = TrouveCarteHaute(tablo,max1,max2)
        return [2,max1,max2,ch]
    if len(paire)>0:
        max1 = max(paire)
        ch = TrouveCarteHaute(tablo,max1,0)
        return[1,max(paire),ch]

    return[0]


def MetTablo(liste): #Transforme le jeu du joueur en valeur dans le tablo "grosseur"
    tablo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in liste:
        tablo = (TriCarte(tablo, i))
    return tablo


def TriCarte(liste,carte): #place la valeur de la carte dans la liste]
    if carte[1] == 2 :
        liste[0]+=1
    if carte[1] == 3 :
        liste[1]+=1
    if carte[1] == 4 :
        liste[2]+=1
    if carte[1] == 5 :
        liste[3]+=1
    if carte[1] == 6 :
        liste[4]+=1
    if carte[1] == 7 :
        liste[5]+=1
    if carte[1] == 8 :
        liste[6]+=1
    if carte[1] == 9 :
        liste[7]+=1
    if carte[1] == 10 :
        liste[8]+=1
    if carte[1] == 11:
        liste[9]+=1
    if carte[1] == 12 :
        liste[10]+=1
    if carte[1] == 13 :
        liste[11]+=1
    if carte[1] == 14:
        liste[12]+=1
    return liste



def mymain():

    jeu = [[2,8], [1,3], [2,4], [2,5], [2,6], [1,7], [1,8]]
    jeu1 = [[2, 2], [3, 10], [4, 12], [4, 11], [3, 12], [1, 13], [1, 14]]
    print(DetermineMeilleur(jeu))



if __name__ == "__main__":
    mymain()