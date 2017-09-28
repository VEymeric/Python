import os
import glob

# Definition des deux dictionnaires globaux : "vieux" scan et "nouveau" scan
dict0 = {}
dict1 = {}


def scanToDict(path, listPath, dict):
    """
    Complète le dictionnaire avec le path de l'objet analysé en key et size, time en data
    """
    for b in listPath:
        key = os.path.join(path, b)
        size = os.path.getsize(key)
        time = os.path.getmtime(key)
        dict[key] = [size, time]  # path = "G:\Cours ISEN"

def scanDoctor(path,nbrSousDossier = 0):
    """
    :param path: chemin d'acces du Document a analyser
    :param nbrSousDossier: nbr de sous dossier que l'on veux analyser.
    :return: une liste avec le chemin de tout les sous-dossier/fichier
    """

    fichier = []
    if nbrSousDossier == 0 :
        l = os.listdir(path) #glob.glob vas lister le contenu d'un repertoire
        for i in l:
            fichier.append(i)
        return fichier

    else :
        current =0
        aReturn = maListDirectory(path,nbrSousDossier-1,current) #-1 a cause d'un coup d'ajustement
        return aReturn

def listdirectory(path,max,valeurActuelle):
    fichier = []
    l = glob.glob(path + '\\*')

    for i in l:

        if os.path.isdir(i) and (valeurActuelle <= max) : #Valeur actuelle Permet de delimiter le nombre de recurrence de la recusivité
            fichier.extend(listdirectory(i,max,valeurActuelle+1))

        else:
            fichier.append(i)

    return (fichier)

def maListDirectory(path, max, valeurActuelle):
    list = []
    l = os.listdir(path)
    for i in l:
        if os.path.isdir(i) and (valeurActuelle <= max) : #Valeur actuelle Permet de delimiter le nombre de recurrence de la recusivité
            list.extend(maListDirectory(i,max,valeurActuelle+1))

def scanComparison(dict0, dict1):
    for a in dict1:
        if a in dict0:
            checkSizeTime(dict0[a], dict1[a])
        else:
            print("Do nothing")

def checkSizeTime(a, b):
    if (a[0] == b[0]) & (a[1] == b[1]):
        return False
    else:
        return True

def scanLaunch(path, nbSousDossier = 0):
    """Fonction principale du scan
    Vérifie si il s'agit du premier scan ou si on a déjà scanné avant"""
    listFiles= []
    # Si dict0 est vide : premier scan
    if bool(dict0) == False:
        # Premier scan
        print("Vide !")
        listFiles = scanDoctor(path, nbrSousDossier=0)
        scanToDict(path, listFiles, dict0)
    else:
        # On a déjà un scan
        print("Second scan")
        listFiles = scanDoctor(path, nbrSousDossier=0)
        scanToDict(path, listFiles, dict1)
     # à ajouter la fonction de comparaison (dans le else)


def mymain():
    scanLaunch("C:\\Users\André\PycharmProjects\TP1", 2)
    for a in dict0:
        print(a, dict0[a])
    from time import sleep
    sleep(1)
    scanLaunch("C:\\Users\André\PycharmProjects\TP1", 2)
    for a in dict1:
        print(a, dict1[a])
    scanComparison(dict0,dict1)

if __name__ == "__main__":
    mymain()
