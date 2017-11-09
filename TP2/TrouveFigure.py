

def VerifPartie2(jeu):
    """
    :param jeu: Carte
    :return: liste classique en fonction de Suite Couleur Quint flush et quint flush royale
    """
    liste = MetTabloSuite(jeu)
    essaiCouleur = identifierCouleur(jeu) #Verifie si on a une couleur
    essaieSuite = identifieSuite(liste) #Verififie si on a une suite

    if essaiCouleur[0] != 5 and essaieSuite[0] == True : #Si on a une Couleur ET une suite on verife QFR
        return identifieQuinteFlush(essaiCouleur[1])

    if essaiCouleur[0] != 5 : #On renvoie couleur
        carteForte = essaiCouleur[1]
        return [5,carteForte[0][1]]

    if essaieSuite[0] == True: #On renovi suite
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
    """
    :param mainPoker: les 7 Carte
    :return: [num couleur, carte le plus forte
    """
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
    #La "liste" est les carte de la couleur concerné et seulement celle la
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
    """Dit si il y a une liste a partir d'un tablo avec nbr carte
    return : list avec [boolean,debutsuite,finsuite]
    """
    cpt = 0
    for i in range(len(liste)-1,-1,-1):#On prend le InRange pour avoir pas de -1
        #LA flemme de corriger le range(len(liste)) par un enumerate(liste[::-1]
        if liste[i] == 0: #On repars a 0 pour le compte d ecarte de la suite
            cpt =0
        if liste[i] >= 1:
            cpt += 1
        if cpt == 5:
            #print("Il y a une suite qui termine en : \n",i+1," et qui commence en ",i+5)
            return [True,i+5,i+1]
    return [False,0,0]


def MetTabloSuite(liste):
    """
    :param liste: les 7 cartes
    :return: LE tablo adapté au fct suite
    """
    tablo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in liste:
        tablo[i[1]-2] += 1

    valeurAs = tablo[12]
    tablo.insert(0,valeurAs)
    return tablo


def TriCouleur(couleur, mainPoker):
    """
    :param couleur:
    :param mainPoker:
    :return: renvoi la liste des carte de la couleur trié
    """
    liste = []
    for c in mainPoker:
        if(c[0] == couleur):
            liste.append(c)
        liste.sort(reverse=True) #Tri l liste dans l'oredre decrosiseant

    return liste


def DetermineMeilleur(jeu):
    """
    :param jeu: Les 2 carte du jOueur + les 5 carte public
    :return: return une liste de plusieur element en fonction de ce que la main as
    """

    v1 = VerifPartie1(jeu) #2 verification car on as bossé a 2 dessus
    v2 = VerifPartie2(jeu) #l'une Verifie les Suite/couleur l'autre les paire/brelan/carré ect ...
    print(v1,v2)
    if v1[0] > v2[0] :
        return v1
    elif v1[0] < v2[0]:#Egalité ou il n'y a pas de figure.
        return v2
    else:
        return v1


def VerifPartie1(jeu):
    """
    :param jeu: Carte
    :return: Retrun la liste classique pour ce qui concerne Pair/Brelan/Carré/full/Rien
    """
    tablo = MetTablo(jeu)
    resultat = Identifie(tablo)
    #print("###############" , resultat)
    TrouveCarteHaute(tablo,resultat)
    #print("-----------------" , resultat)
    return resultat


def TrouveCarteHaute(tablo,resultat):
    x = resultat[0]
    if x == 7 or x == 1 or x == 3:
        for pos, i in enumerate(tablo[::-1]):  # Parcours tablo a l'envers
            position = len(tablo) - pos + 1
            if (i>0) and (position !=resultat[1]):
                resultat.append(position)
                return
                #print("pos : " , position , "Valeur : ", i)
        print(tablo)
    if x == 2:
        for pos, i in enumerate(tablo[::-1]):  # Parcours tablo a l'envers
            position = len(tablo) - pos + 1
            if (i>0) and (position !=resultat[1] and position !=resultat[2]):
                resultat.append(position)
                return
    if x == 0:
        for pos, i in enumerate(tablo[::-1]):  # Parcours tablo a l'envers
            position = len(tablo) - pos + 1
            if (i>0):
                resultat.append(position)
                return


def Identifie(tablo):
    """
    PErme de definir ce qu'il y a dans le eju
    :param tablo: tablo classique du prgm
    :return: return la liste adapté en fonction des carte pour Brelan/paire/full/carre/rien
    """
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
    if len(brelan) > 0 and len(paire)>0: #Est ce qu'on a Un breln ET une paire
        return [6,max(brelan)] # [valeur de la figure, valeur des carte du brelan ]
    if len(brelan) > 0: #Est ce qu'on a un brelan ?
        return [3, max(brelan)] # [valeur de la figure, valeur des carte du brelan]
    if len(paire) > 1:
        max1 = max(paire)
        paire.sort()
        paire.pop()
        max2 = max(paire)
        return [2,max1,max2]
    if len(paire)>0:
        max1 = max(paire)
        return [1,max(paire)]
    return[0]


def MetTablo(liste):
    """
    :param liste: LEs 7 cartes
    :return: tablo classique pour les fonction
    """
    tablo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in liste:
        tablo[i[1]-2] += 1
    return tablo


def mymain():

    jeu = [[2,2], [1,3], [2,4], [2,8], [2,6], [1,7], [1,14]]
    jeu1 = [[2, 10], [2, 14], [4, 12], [1, 11], [1, 3], [1, 13], [1, 4]]
    jeu2 = [[2, 14], [1, 14], [4, 14], [1, 11], [1, 3], [1, 13], [1, 4]]
    print(DetermineMeilleur(jeu2))



if __name__ == "__main__":
    mymain()