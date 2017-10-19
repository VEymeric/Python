import os
from time import sleep


def scan_to_dict(path, list_path, dictio):
    """
    Complète le dictionnaire avec le path de l'objet analysé en key et size, time en data
    """
    for b in list_path:
        key = os.path.join(path, b)
        size = os.path.getsize(key)
        time = os.path.getmtime(key)
        dictio[key] = [size, time]  # path = "G:\Cours ISEN"


def scan_doctor(path, nbr_sous_dossier=0):
    """
    :param path: chemin d'acces du Document a analyser
    :param nbr_sous_dossier: nbr de sous dossier que l'on veux analyser.
    :return: une liste avec le chemin de tout les sous-dossier/fichier
    """
    current = 0
    value = listdirectory(path, nbr_sous_dossier-1, current)  # -1 a cause d'un coup d'ajustement
    return value


def listdirectory(path, maximum, valeur_actuelle):
    mylist = []
    fichier = []
    temp = os.listdir(path)
    for i in temp:
        chemin = path + '\\' + i
        mylist.append(chemin)
    for i in mylist:
        if os.path.isdir(i) and (valeur_actuelle <= maximum):
            # Valeur actuelle Permet de delimiter le nombre de recurrence de la recusivité
            fichier.extend(listdirectory(i, maximum, valeur_actuelle + 1))
        else:
            fichier.append(i)
    return fichier


def check_maj_scan(dico1, dico2):
    """
    this function will compare dico2 to dico1 to see if any file has been modified or created
    then compare dico1 to dico2 to see if some file has been deleted
    return: true if detect a modif
    """
    modification = False
    for key in dico2:
        if key in dico1:
            if dico1[key][1] != dico2[key][1]:
                modification = True
                print("file has been modify", key)
        else:
            modification = True
            print("file has been created ", key)
    for key in dico1:
        if key not in dico2:
            modification = True
            print("file has been removed ", key)
    if not modification:
        print("This path hasn't been modify")
    return modification


def tracker(timer, nb_scan, path, limit):
    if nb_scan <= 0:
        return
    list_files = scan_doctor(path, limit)
    dico1 = {}
    dico2 = {}
    scan_to_dict(path, list_files, dico1)
    for fichier in dico1:
        print(fichier, dico1[fichier])
    i = 1

    while i <= nb_scan:
        sleep(timer)
        print("CHECK", i)
        list_files2 = scan_doctor(path, limit)
        scan_to_dict(path, list_files2, dico2)
        check_maj_scan(dico1, dico2)
        dico1 = dico2
        dico2 = {}
        i += 1


if __name__ == "__main__":
    mytimer = 5
    mynbScan = 10
    mypath = "D:\Images"
    mymax_subfolder = 2
    tracker(mytimer, mynbScan, mypath, mymax_subfolder)
    print("~ end ~")
