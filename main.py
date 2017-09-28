import os
import glob

# Definition des deux dictionnaires globaux : "vieux" scan et "nouveau" scan
dict0 = {}
dict1 = {}


def scanToDict(listPath, dict):
    """
    Complète le dictionnaire avec le path de l'objet analysé en key et size, time en data
    """
    for b in listPath:
        key = os.path.join(b)
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
        l = glob.glob(path + '\\*') #glob.glob vas lister le contenu d'un repertoire
        for i in l:
            fichier.append(i)
        return fichier

    else :
        current =0
        aReturn = listdirectory(path,nbrSousDossier-1,current) #-1 a cause d'un coup d'ajustement
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

def scanLaunch(path="G:\Cours ISEN", nbSousDossier = 0):
    """Fonction principale du scan
    Vérifie si il s'agit du premier scan ou si on a déjà scanné avant"""
    listFiles= []
    # Si dict0 est vide : premier scan
    if bool(dict0) == False:
        # Premier scan
        print("Vide !")
        listFiles = scanDoctor(path, nbrSousDossier=0)
        scanToDict(listFiles, dict0)
    else:
        # On a déjà un scan
        print("Second scan")
        listFiles = scanDoctor(path, nbrSousDossier=0)
        scanToDict(listFiles, dict1)
     # à ajouter la fonction de comparaison (dans le else)


def writeScanToFile(path="G:\Cours ISEN"):
    dirs = os.listdir(path)
    # Open and Write on file "PATH  SIZE  TIME"
    fo = open("foo.txt", "w")
    for b in dirs:
        c = os.path.join(path, b)
        fo.write(c)
        fo.write('\t')
        fo.write('%d' % os.path.getsize(c))
        fo.write('\t')
        fo.write('%d' % os.path.getmtime(c))
        fo.write('\n')
    fo.close()


def mymain():
    scanLaunch("G:\Cours ISEN")
    for a in dict0:
        print(a, dict0[a])
    from time import sleep
    sleep(3)
    scanLaunch("G:\Cours ISEN")
    for a in dict1:
        print(a, dict1[a])


if __name__ == "__main__":
    mymain()
