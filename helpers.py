from pathlib import Path
import os
def check_if_folder(f_path):
    '''This checks if the desired path is a folder. If not, it creates the folder'''


    if not os.path.exists(f_path):
        os.makedirs(f_path)
        print('Making a folder with the path ' + f'{f_path}')

    return
