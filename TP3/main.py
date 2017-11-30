import begin
import logging
import os

from ftplib import FTP
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)

file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


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


def connexion_ftp(host, user, password):
    connect = FTP(host, user, password)  # on se connecte
    print(connect.getwelcome())
    return connect


def upload_this(ftp_server, path, sub_folder_max):
    upload_this_recurrence(ftp_server, path, 1, sub_folder_max)


def upload_this_recurrence(ftp_server, path, sub_folder, sub_folder_max):
    if sub_folder > sub_folder_max:
        return
    files = os.listdir(path)
    os.chdir(path)
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            fh = open(f, 'rb')
            ftp_server.storbinary('STOR %s' % f, fh)
            fh.close()
        elif os.path.isdir(path + r'/{}'.format(f)):
            try:  # just try to create a folder if didn't exist
                ftp_server.mkd(f)
            except Exception as e:
                pass
            ftp_server.cwd(f)
            upload_this_recurrence(ftp_server, path + r'/{}'.format(f), sub_folder+1, sub_folder_max)
    ftp_server.cwd('..')
    os.chdir('..')

"""
if(i[0] == 'd'): #it's a folder !
            print(str(names_ftp.__len__()) + str(names_ftp[names_ftp.__len__()-1]))
            test = names_ftp[names_ftp.__len__()-1]
            ftp_server.cwd(test)
            destroy_unused_files(ftp_server, ftp_folder+"\\"+test, sub_dir+1, sub_dir_max)
            ftp_server.cwd('..')
            
            
    try:
        names_local = os.listdir(ftp_folder)
    except Exception as e:
        print("WWWWWWWO" +str(names_ftp))
        truc = ftp_folder.split("\\")
        print(truc[len(truc)-1])
        ftp_server.cwd('..')
        print("no error here")
        ftp_server.delete(truc[len(truc)-1])
        return
"""
def destroy_unused_files(ftp_server, ftp_folder, sub_dir, sub_dir_max):
    if sub_dir > sub_dir_max:
        return
    l = []
    names_local = []
    ftp_server.retrlines('LIST ', l.append) ## Listage du repertoire a telecharger
    print(l)
    names_ftp = []
    for i in l:
        names_ftp.append(i.split()[8]) # names now contain all names of files in ftp

    print("names_ftp" + str(names_ftp))
    print("local : " + str(ftp_folder))
    print("names_local" + str(names_local))
    try:
        names_local = os.listdir(ftp_folder)
    except Exception as e:
        pass
    if names_ftp != names_local:
        dif = set(names_ftp) - set(names_local)
        for f in dif:
            print("pls delete :" + f)
            print(ftp_server.pwd())
            ftp_server.delete(f)

    # on a supprimé les fichiers, on passe maintenant dans les dossiers !


@ begin.start(auto_convert=True)
def start(local, ftp_server=connexion_ftp("localhost", "chao", "1234"), frequence=15, sub_dir=3, debug_mode=False, size_max=10):
    print("mdr")
    listOfFiles = ["server_local/test/caca.txt"]
    destroy_unused_files(ftp_server, local, 1, sub_dir)
    #send_folder_to_ftp(ftp_server, "server_local", "server_ftp/alo")


