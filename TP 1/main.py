import os
from time import sleep

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
        aReturn = listdirectory(path,nbrSousDossier-1,current) #-1 a cause d'un coup d'ajustement
        return aReturn

def listdirectory(path,max,valeurActuelle):
    list = []
    fichier = []
    l = os.listdir(path)
    for ii in l:
        chemin = path + '\\' + ii
        list.append(chemin)
    for i in list:
        if os.path.isdir(i) and (
            valeurActuelle <= max):  # Valeur actuelle Permet de delimiter le nombre de recurrence de la recusivité
            fichier.extend(listdirectory(i, max, valeurActuelle + 1))
        else:
            fichier.append(i)
    return fichier


def checkMajScan(dico1, dico2):
    """
    this function will compare dico2 to dico1 to see if any file has been modified or created
    then compare dico1 to dico2 to see if some file has been deleted
    return: true if detect a modif
    """
    modification = False
    for key in dico2:
        if key in dico1:
            if (dico1[key][1] != dico2[key][1]):
                modification = True
                print ("fichier has been modify", key)
        else:
            modification = True
            print("fichier has been created ", key)
    for key in dico1:
        if key not in dico2:
            modification = True
            print("fichier has been removed ", key)
    if(modification == False):
        print("This path hasn't been modify")
    return modification

def tracker(timer, nbScan, path, limit):
    if(nbScan <= 0):
        return
    listFiles = scanDoctor(path, limit)
    dico1 = {}
    dico2 = {}
    scanToDict(path, listFiles, dico1)
    for fichier in dico1:
        print(fichier, dico1[fichier])
    i = 1

    while(i <= nbScan):
        sleep(timer)
        print("CHECK" , i)
        listFiles2 = scanDoctor(path, limit)
        scanToDict(path, listFiles2, dico2)
        haveChange = checkMajScan(dico1, dico2)
        dico1 = dico2
        dico2 = {}
        i += 1

if __name__ == "__main__":
    timer = 5
    nbScan = 10
    path = "D:\Images"
    maxSubfolder = 2
    tracker(timer,nbScan,path,maxSubfolder)
    print("~ end ~")

