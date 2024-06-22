from pathlib import Path
import os
import glob
import dropbox
from dropbox.exceptions import AuthError


def check_if_folder(f_path):
    '''This checks if the desired path is a folder. If not, it creates the folder'''


    if not os.path.exists(f_path):
        os.makedirs(f_path)
        print('Making a folder with the path ' + f'{f_path}')

    return

def remove_result_tables(my_folder):
    '''I don't want results tables out in the open because they will run into other code for chardata'''
    check_if_folder('Data/IV_data/'+ my_folder + '/Results Table')
    for file in glob.glob('Data/IV_data/'+ my_folder + '/Results Table*.txt'):
        o = file.split('/')
        newfile = '/'.join(o[:3]) + '/Results Tables/' + o[-1]
        os.rename(file, newfile)

def create_dropbox_path(name):
    '''I want to save a copy of my csv in dropbox to save some time for syncing as I give it to origin'''
    totpath = os.getcwd()
    o = totpath.split('/')
    parentpath = '/'.join(o[:2])
    dropboxpath = parentpath + '/Dropbox (ASU)/IV/'+ name
    check_if_folder(dropboxpath)
    return dropboxpath

def dropbox_connect():
    """ NOTE: this does not work, and cannot work unless ASU allows me to make an access token for my dropbox app,
    which is required to modify folders in dropbox
    
    Create a connection to Dropbox.
    """
    DROPBOX_ACCESS_TOKEN = 'x'
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx
