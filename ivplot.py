import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import seaborn as sns


substrate_palette = {1: sns.color_palette()[0], 2: sns.color_palette()[1], 3: sns.color_palette()[2], 
                     4: sns.color_palette()[3], 5: sns.color_palette()[4], 6: sns.color_palette()[5]}

position_dashes = {1: (5, 0), 2: (6, 4), 3: (3, 1)}
def read_IV_data():
    df = pd.DataFrame()
    for file in glob.glob('Data/AD_2024_04_18/IV_data/2024-04-18/*'):
        tempdf = pd.read_csv(file, header = 6, sep = '\t')
        o = file.split("_")[-2].split('/')[-1]
        tempdf['name'] = o
        df = pd.concat([tempdf, df])
    df['substrate'] = df.apply(lambda row: row['name'][-3], axis = 1) #Want color based on substrate
    df['position'] = df.apply(lambda row: row['name'][-1], axis = 1)#Want style based on sample position on substrate
    df = df.sort_values(by = ['substrate', 'position'])
    print(df)
    df.index = range(len(df))
    return df

def save_IV_data():
    '''The purpose of this function is to store the IV data as a single csv file.
    This means that the program will save time as it does not need to recreate the
    df from scratch every time'''
    df = read_IV_data()
    df.to_csv('Data/AD_2024_04_18/IV_data/alldata/2024-04-18_all_IV.csv', index = False)


def plot_IV_data_all(path):
    df = pd.read_csv(path)
    df['Imeas'] *= 1000
    
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df, palette=substrate_palette, dashes = position_dashes)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'All IV curves')
    plt.savefig('Figures/2024-04-18/all_IVdata.pdf')
    plt.close('all')


def plot_IV_data_bypos(path, position):
    df = pd.read_csv(path)
    df['Imeas'] *= 1000
    
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df.loc[df['position'] == position], dashes = position_dashes,
                      palette=substrate_palette)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'IV curves for position ' +f'{position}')
    plt.savefig('Figures/2024-04-18/IV_data_position_' + f'{position}'+ '.pdf')
    plt.close('all')


def plot_IV_data_bysubstrate(path, substrate):
    df = pd.read_csv(path)
    df['Imeas'] *= 1000
    
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df.loc[df['substrate'] == substrate],
                      palette = substrate_palette, dashes = position_dashes)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'IV curves for substrate ' +f'{substrate}')
    plt.savefig('Figures/2024-04-18/IV_data_substrate_' + f'{substrate}'+ '.pdf')
    plt.close('all')

def plot_many_IV(path):
    '''The purpose of this function is to produce many IV figures at once'''
    for x in list(range(1, 4)):
        plot_IV_data_bypos(path, x)
    for x in list(range(1, 7)):
        plot_IV_data_bysubstrate(path, x)
    plot_IV_data_all(path)