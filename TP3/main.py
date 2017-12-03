import begin
import logging
import os
import time

from datetime import datetime
from ftplib import FTP
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

is_connected = False


def listdirectory(path, maximum, valeur_actuelle):
    logger.debug("listdirectory()")
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


def get_ftp_file_time(ftp_server, file):
    """
    Demande au serveur FTP la date de modification du fichier donné
    :param ftp_server:
    :param file:
    :return: Date de modification du fichier
    """
    try:
        modified_time = ftp_server.sendcmd('MDTM ' + file)
        modified_time = datetime.strptime(modified_time[4:], "%Y%m%d%H%M%S")
        return modified_time
    except Exception:
        return datetime.min


def get_local_file_time(path, file):
    """
    Cherche la date de dernière modification du fichier local donné
    :param path:
    :param file:
    :return: Date de dernière modification du fichier
    """
    file_time = os.path.getmtime(path + r'\{}'.format(file))
    file_time = time.gmtime(file_time)
    file_time = datetime.fromtimestamp(time.mktime(file_time))
    return file_time


def upload_this(ftp_server, path, sub_folder_max, size_max):
    """
    upload files and folder who are on local but not already on the ftp server
    :param sub_folder_max: limit the search in a maximum subDirectory
    :param size_max: limit the upload with a size file
    :return: void
    """
    try:
        upload_this_recurrence(ftp_server, path, 1, sub_folder_max, size_max)
    except Exception as e:
        global is_connected
        is_connected = False
        logger.error("error when upload_this : " + str(e))


def upload_this_recurrence(ftp_server, path, sub_folder, sub_folder_max, size_max):
    logger.debug("upload_this_recurrence " + str(ftp_server.pwd()) + " " + str(path) + " " + str(sub_folder))
    if sub_folder > sub_folder_max:
        return
    files = os.listdir(path)
    os.chdir(path)
    logger.debug("Debut Traitement de : [" + path + "]")
    for f in files:
        if os.path.isfile(path + r'\{}'.format(f)):
            logger.debug("Traitement [" + f + "]")
            if os.path.getsize(path + r'\{}'.format(f)) > size_max:
                logger.error(
                    "Le fichier " + path + r'\{}'.format(f) + " depasse la limite autorisée et n'a pas été transféré")
            else:
                old_time = get_local_file_time(path, f)
                new_time = get_ftp_file_time(ftp_server, f)
                if old_time > new_time:
                    logger.info("Envoi du fichier : [" + path + r'\{}'.format(f) + "]")
                    fh = open(f, 'rb')
                    ftp_server.storbinary('STOR %s' % f, fh)
                    fh.close()
        elif os.path.isdir(path + r'\{}'.format(f)):
            logger.debug("Traitement sous dossier [" + f + "]")
            try:  # just try to create a folder if didn't exist
                ftp_server.mkd(f)
                logger.info("Folder : " + str(f) + " was created")
            except Exception:
                pass
            ftp_server.cwd(f)
            upload_this_recurrence(ftp_server, path + r'\{}'.format(f), sub_folder + 1, sub_folder_max, size_max)
    ftp_server.cwd('..')
    os.chdir('..')


def destroy_unused_files(ftp_server, ftp_folder, sub_dir_max):
    """
    Remove files and folder who are on the ftp server but not in local
    :param sub_dir_max: limit the search in a maximum subDirectory
    :return: void
    """
    try:
        destroy_unused_files_recurrence(ftp_server, ftp_folder, 1, sub_dir_max)
    except Exception as e:
        global is_connected
        is_connected = False
        logger.error("error when destroy_unused_files : " + str(e))


def destroy_unused_files_recurrence(ftp_server, local_folder, sub_dir, sub_dir_max):
    if sub_dir > sub_dir_max:
        return
    list_files_ftp = []
    ftp_server.retrlines('LIST ', list_files_ftp.append)  # list the directory data from ftp

    names_local = []
    names_ftp = []
    for file in list_files_ftp:
        test = file.split()
        name = test[8]
        for i in range(9, len(test)):  # fix trouble with the name if their is space
            name += " " + test[i]
        names_ftp.append(name)  # names now contain all names of files in ftp

        if file[0] == 'd':  # if it's a folder, do this function in this folder
            ftp_server.cwd(name)
            destroy_unused_files_recurrence(ftp_server, local_folder+"\\"+name, sub_dir+1, sub_dir_max)
            ftp_server.cwd('..')

    try:
        names_local = os.listdir(local_folder)
    except Exception:
        pass

    if names_ftp != names_local:
        dif = set(names_ftp) - set(names_local)
        for f in dif:
            try:  # if it's a file
                ftp_server.delete(f)
                logger.info("The file " + f + " was deleted")
            except Exception:
                pass
            try:  # if it's a folder
                ftp_server.rmd(f)
                logger.info("The folder " + f + " was deleted")
            except Exception:
                pass


@begin.start(auto_convert=True)
def start(local: 'Dossier à synchroniser',
          logs: 'Path logs',
          host: 'Nom d\'hôte',
          user: 'Nom d\'utilisateur',
          password: 'Mot de passe',
          frequency: 'Frequence de raffraichissement'=15,
          sub_dir: 'Nombre de sous-dossier max'=6,
          debug: 'Affiche le debug dans les logs'=False,
          max_size: 'Taille maximale d\'un fichier à envoyer'=10):

    file_handler = RotatingFileHandler(logs, 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if debug:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    size_max = max_size * 1000000
    logger.debug("################RESTART####################################")
    global is_connected
    cycle = 1
    while True:
        try:
            while not is_connected:
                try:
                    server = connexion_ftp(host, user, password)
                    is_connected = True
                except Exception:
                    is_connected = False
                    logger.info("server not found, try to reconnect in " + str(frequency) + "s")
                    time.sleep(frequency)
            upload_this(server, local, sub_dir, size_max)
            destroy_unused_files(server, local, sub_dir)
            logger.debug("Fin de l'envoi : " + str(cycle))
            cycle += 1
            time.sleep(frequency)
        except Exception as e:
            logger.error("In the main : " + str(e))
            time.sleep(frequency)
