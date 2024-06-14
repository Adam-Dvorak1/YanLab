import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import seaborn as sns
import importlib
import helpers
import os
importlib.reload(helpers)
from helpers import check_if_folder

'''The purpose  is to assemble the PL data into tables which can then be 
turned into plots on origin. Each column will have a name. I want a table for all the data,
and for each condition'''
def assemble_all_PL_files(name):
    '''This will create a df of all of '''
    df = pd.DataFrame()

    np.arange(650, 902, 2)
    for file in glob.glob('Data/PL data/' + name + '/*.txt'):
        tempdf = pd.read_csv(file, header = 20) #Note: CHECK THE NUMBER OF POINTS. skipfooter should be the # of points (rows) plus 1. Add this in next time
        #We can make a dataframe of just the characteristic data, which is in the 'header'. 
        # However the IV data is in a different dimension and should be saved separately
        o = file[0:8]
        tempdf['name'] = o
        df = pd.concat([tempdf, df])
    