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
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def listdirectory(path, maximum, valeur_actuelle):
    logger.debug("fdsfs")
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
    logger.info("Connexion :" + connect.getwelcome())
    return connect


def upload_this(ftp_server, path,tailleMax):
    files = os.listdir(path)
    os.chdir(path)
    logger.debug("Debut Traitement de : ["+path+"]")
    for f in files:

        if os.path.isfile(path + r'\{}'.format(f)):
            logger.debug("Traitement [" + f + "]")
            if (os.path.getsize(path + r'\{}'.format(f)) > tailleMax):
                logger.error("Le fichier " + path + r'\{}'.format(f) + " depasse la limite autorisée et n'a pas été transféré")
                #print(path + r'\{}'.format(f), os.path.getsize(path + r'\{}'.format(f)))
            else :
                #print(os.path.getsize(path))
                #print(path + r'\{}'.format(f))
                logger.debug("Envoi du fichier : ["+path + r'\{}'.format(f)+"]")
                fh = open(f, 'rb')
                ftp_server.storbinary('STOR %s' % f, fh)
                fh.close()
        elif os.path.isdir(path + r'/{}'.format(f)):
            logger.debug("Traitement sous dossier [" + f + "]")
            try:  # just try to create a folder if didn't exist
                ftp_server.mkd(f)
            except Exception as e:
                donothing = True
            ftp_server.cwd(f)
            upload_this(ftp_server, path + r'/{}'.format(f),tailleMax)
    ftp_server.cwd('..')
    os.chdir('..')



@begin.start(auto_convert=True)
def start(local: 'Dossier à synchroniser',
          host: 'Nom d\'hôte',
          user: 'Nom d\'utilisateur',
          password: 'Mot de passe',
          frequence=15, sub_dir=6, debug=False, size_max=10):
    #debug = True
    if (debug==True):
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    tailleMax = size_max * 1000000
    logger.debug("###########################################################")



    #fichier = "test.txt"
    #fichier2 = "test2.txt"
    #file = open(fichier, 'rb')  # ici, j'ouvre le fichier ftp.py
    #file2 = open(fichier2, 'wb')  # ici, j'ouvre le fichier ftp.py

    #ftp_server.storbinary('STOR ' + fichier,file)  # ici (où connect est encore la variable de la connexion), j'indique le fichier à envoyer
    #ftp_server.retrbinary('RETR ' + fichier2, file2.write)
    #ftp_server.retrlines('LIST')
    #ftp_server.mkd("BITE")
    listOfFiles = ["server_local/test/caca.txt"]
    upload_this(ftp_server, local,tailleMax)
    logger.debug("Fin de l'envoi")
    #send_folder_to_ftp(ftp_server, "server_local", "server_ftp/alo")


