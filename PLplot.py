import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import seaborn as sns
import importlib
import scipy.optimize as opt
import helpers
import os
importlib.reload(helpers)
from helpers import check_if_folder

'''The purpose  is to assemble the PL data into tables which can then be 
turned into plots on origin. Each column will have a name. I want a table for all the data,
and for each condition'''

experimental_conditions = {9: '5000 rpm', 10: '5000 rpm', 11: '7000 rpm', 12: '7000 rpm', 13: '8000 rpm', 14: '8000 rpm',15: '9000 rpm', 16: '9000 rpm',}

def read_PL_file(name):
    '''This will read a PL file'''
    df = pd.DataFrame()
    for file in glob.glob('Data/PL data' + name + '/*.txt'):
        tempdf = pd.read_csv(name, header = 20)


def read_PL_files(name):

    '''This will take in all of the PL data files and get it in a '''
    df = pd.DataFrame()
    for file in glob.glob('Data/PL data/' + name + '/*.txt'):
        # print(file)
        tempdf = pd.read_csv(file, usecols=[0, 1], names = ['wavelength', 'signal strength'], header = 20) #Note: CHECK THE NUMBER OF POINTS. skipfooter should be the # of points (rows) plus 1. Add this in next time
        #We can make a dataframe of just the characteristic data, which is in the 'header'. 
        # However the IV data is in a different dimension and should be saved separately
    
        sample = file.split('/')[-1] #the actual name is in the file name, after the last slash of the path
        sample = sample[:-4] #we don't care about the .txt
        # print(tempdf)
        # tempdf['signal strength'] = pd.to_numeric(tempdf['signal strength'])
        tempdf['normalized signal'] = tempdf['signal strength'] / tempdf['signal strength'].max()
        tempdf['name'] = sample
        tempdf['sample number'] = sample[-2:]
        tempdf['sample number'] = pd.to_numeric(tempdf['sample number'])
        tempdf['exp condition'] = tempdf['sample number'].map(experimental_conditions)
        df = pd.concat([tempdf, df])
    
    df = df.sort_values('sample number')

    return df



def save_PL_files(name):
    df = read_PL_files(name)
    df.to_csv('Data/PL data/PL_csvs/'+ name + '_allPL.csv')

def gauss(x, p): # p[0]==mean, p[1]==stdev
    return 1.0/(p[1]*np.sqrt(2*np.pi))*np.exp(-(x-p[0])**2/(2*p[1]**2))

def plot_PL_graph(path):
    substrate = 11
    df = pd.read_csv(path)
    ax = sns.lineplot (x = 'wavelength', y = 'normalized signal', data = df.loc[df['sample number'] == substrate])
    print(df)
    df = df.loc[df['sample number'] == substrate]
    print(df)
    xline = df['wavelength'].loc[df['normalized signal'] == df['normalized signal'].max()].values[0]
    print(xline)
    plt.axvline(xline)


    # ax = sns.lineplot(x = 'Vmeas', y = 'Jmeas (mA/cm2)', hue = 'substrate', style = 'position', data = df, palette=substrate_palette, dashes = position_dashes)
    # ax.set(xlabel = 'Voltage (V)', ylabel = 'Current density (mA/cm2)', title = 'All IV curves')
    # plt.show()
    # plt.close('all')

    plt.show()
