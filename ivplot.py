import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import seaborn as sns
import importlib
import helpers
import os
importlib.reload(helpers)
from helpers import check_if_folder, remove_result_tables, create_dropbox_path



substrate_palette = {1: sns.color_palette()[0], 2: sns.color_palette()[1], 3: sns.color_palette()[2], 
                     4: sns.color_palette()[3], 5: sns.color_palette()[4], 6: sns.color_palette()[5]}

position_dashes = {'A': (5, 0), 'B': (6, 4), 'C': (3, 1), 'D': (2, 1), 'E': (4, 2)}

def read_characteristic_data(name):
    '''The purpose of this program is to extract the efficiency, V_oc, I_sc, FF, etc'''
    df = pd.DataFrame()
    for file in glob.glob('Data/IV_data/' + name + '/*.txt'):
        tempdf = pd.read_csv(file, header = 4, skipfooter = 102, sep = '\t') #Note: CHECK THE NUMBER OF POINTS. skipfooter should be the # of points (rows) plus 1. Add this in next time
        #We can make a dataframe of just the characteristic data, which is in the 'header'. 
        # However the IV data is in a different dimension and should be saved separately
        o = file.split('_')[-2].split('/')[-1]
        tempdf['name'] = o
        tempdf['Experiment'] = file[file.find("(")+1:file.find(")")] #We want to make another category column, which experiment we did
        df = pd.concat([tempdf, df])
    df['substrate'] = df.apply(lambda row: row['name'][:-2], axis = 1) #Want color based on substrate. In 
    df['position'] = df.apply(lambda row: row['name'][-1], axis = 1)#Want style based on sample position on substrate
    # df['batch'] = df.apply (lambda row: row['name'][-5], axis = 1) #
    df = df.sort_values(by = ['substrate', 'position', 'Efficiency']) #We sort by substrate and position to make it orderly. We sort by efficiency to always keep the most efficient, in the next line
    df = df.drop_duplicates(subset = ['substrate', 'position'], keep = 'last')
    print(df)
    df.index = range(len(df))
    return df


def save_characteristic_data(name):
    '''The purpose of this function is to store the IV data (figures of merit) as a single csv file.
    This means that the program will save time as it does not need to recreate the
    df from scratch every time'''
    remove_result_tables(name)# The purpose of this is that sometimes we save results tables, but I want them in their own folder. I will create my own
    df = read_characteristic_data(name)

    chardata_path = 'Data/IV_data/characteristic_data_csvs/' + name + '_char_data.csv'
    df.to_csv(chardata_path, index = False)#make sure you change the date and folder of these things

    
    # dropboxpath = create_dropbox_path(name) #Do not use this unless I receive access to create access key for dropbox
    # df.to_csv(dropboxpath + '/' + 'figs_o_merit.csv') #Though it might be confusing to save twice, I also want to save directly to the dropbox folder

def plot_char_data(path, fig_o_merit):
    '''The purpose of this function is to plot the many points
    The fig_o_merit can be 'Voc V', 'Isc A', 'Jsc mA_cm2', 'Fill Factor', 'Efficiency', etc'''
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams['xtick.labelsize']=10
    plt.rcParams['ytick.labelsize']=10
    
    df = pd.read_csv(path)
    df['Jsc mA_cm2'] = df['Jsc mA/cm2']
    o = path.split('/')[-1].split('_')[0]
    ax = sns.catplot(x = 'substrate', y = fig_o_merit, hue = 'position', data = df, s = 10)
    sns.despine(fig=None, ax=None, top=False, right=False, left=False, bottom=False)
    ax.set(title = fig_o_merit + ' by position')

    savepath = 'Figures/char_data/'+ o
    check_if_folder(savepath)
    plt.tight_layout()
    plt.savefig(savepath + '/' + fig_o_merit + '.pdf')
    plt.close('all')

def plot_many_char_data(path):
    plot_char_data(path, 'Voc V')

    plot_char_data(path, "Efficiency")
    plot_char_data(path, 'Fill Factor')
    plot_char_data(path, 'Jsc mA_cm2') #


def read_IV_data(name):
    df = pd.DataFrame()
    for file in glob.glob('Data/IV_data/' + name + '/*.txt'):
        tempdf = pd.read_csv(file, header = 6, sep = '\t')
        o = file.split("_")[-2].split('/')[-1]
        tempdf['Jmeas (mA/cm2)'] = tempdf.apply(lambda row: row['Imeas']/0.077 * 1000, axis = 1) #Dividing by the area (0.077 cm^2) gives the current density in A/cm^2, and multiplying by 1000 gives the current density in mA/cm^2
        tempdf['name'] = o
        df = pd.concat([tempdf, df])
    df['substrate'] = df.apply(lambda row: row['name'][-3], axis = 1) #Want color based on substrate
    df['position'] = df.apply(lambda row: row['name'][-1], axis = 1)#Want style based on sample position on substrate
    df['batch']= df.apply(lambda row: row['name'][-5], axis = 1)
    
    df = df.sort_values(by = ['substrate', 'position'])
    print(df)
    df.index = range(len(df))
    return df

def save_IV_data(name):
    '''The purpose of this function is to store the IV data as a single csv file.
    This means that the program will save time as it does not need to recreate the
    df from scratch every time'''
    df = read_IV_data(name)
    df.to_csv('Data/IV_data/IV_csvs/' + name + '_all_IV.csv', index = False)


def plot_IV_data_all(path):
    df = pd.read_csv(path)
    o = path.split('/')[-1].split('_')[0] + '_' + path.split('/')[-1].split('_')[1]
    df['Imeas'] *= 1000
    
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Jmeas (mA/cm2)', hue = 'substrate', style = 'position', data = df, palette=substrate_palette, dashes = position_dashes)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current density (mA/cm2)', title = 'All IV curves')
    
    savepath = 'Figures/IV_data/' + o 
    check_if_folder(savepath )

    plt.savefig(savepath+ '/all_IVdata.pdf')
    plt.close('all')


def plot_IV_data_bypos(path, position):
    df = pd.read_csv(path)
    df['Imeas'] *= 1000
    
    o = path.split('/')[-1].split('_')[0]
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df.loc[df['position'] == position], dashes = position_dashes,
                      palette=substrate_palette)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'IV curves for position ' +f'{position}')
    plt.savefig('Figures/' + o + '/IV_data_position_' + f'{position}'+ '.pdf')
    plt.close('all')


def plot_IV_data_bysubstrate(path, substrate):
    df = pd.read_csv(path)
    df['Imeas'] *= 1000
    o = path.split('/')[-1].split('_')[0]
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df.loc[df['substrate'] == substrate],
                      palette = substrate_palette, dashes = position_dashes)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'IV curves for substrate ' +f'{substrate}')
    plt.savefig('Figures/' + o + '/IV_data_substrate_' + f'{substrate}'+ '.pdf')
    plt.close('all')

def plot_many_IV(path):
    '''The purpose of this function is to produce many IV figures at once'''
    for x in list(range(1, 6)):
        plot_IV_data_bypos(path, x)
    for x in [x for x in range (1, 7) if x != 2]: #The second substrate was used on the wrong side
        plot_IV_data_bysubstrate(path, x)
    plot_IV_data_all(path)

    
