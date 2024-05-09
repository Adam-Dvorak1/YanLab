import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import seaborn as sns


substrate_palette = {1: sns.color_palette()[0], 2: sns.color_palette()[1], 3: sns.color_palette()[2], 
                     4: sns.color_palette()[3], 5: sns.color_palette()[4], 6: sns.color_palette()[5]}

position_dashes = {1: (5, 0), 2: (6, 4), 3: (3, 1), 4: (2, 1), 5: (4, 2)}

def read_characteristic_data(exp_date):
    '''The purpose of this program is to extract the efficiency, V_oc, I_sc, FF, etc'''
    df = pd.DataFrame()
    for file in glob.glob('Data/IV_data/' + exp_date + '/*'):
        tempdf = pd.read_csv(file, header = 4, skipfooter = 102, sep = '\t') #Note: CHECK THE NUMBER OF POINTS. skipfooter should be the # of points (rows) plus 1. Add this in next time
        #We can make a dataframe of just the characteristic data, which is in the 'header'. 
        # However the IV data is in a different dimension and should be saved separately
        o = file.split('_')[-2].split('/')[-1]
        tempdf['name'] = o
        df = pd.concat([tempdf, df])
        df['substrate'] = df.apply(lambda row: row['name'][-3], axis = 1) #Want color based on substrate
    df['position'] = df.apply(lambda row: row['name'][-1], axis = 1)#Want style based on sample position on substrate
    df = df.sort_values(by = ['substrate', 'position'])
    print(df)
    df.index = range(len(df))
    return df


def save_characteristic_data(exp_date):
    '''The purpose of this function is to store the IV data as a single csv file.
    This means that the program will save time as it does not need to recreate the
    df from scratch every time'''
    df = read_characteristic_data(exp_date)
    df.to_csv('Data/IV_data/characteristic_data_csvs/' + exp_date + '_char_data.csv', index = False)#make sure you change the date and folder of these things

def plot_char_data(path, fig_o_merit):
    '''The purpose of this function is to plot the many points
    The fig_o_merit can be 'Voc V', 'Isc A', 'Fill Factor', 'Efficiency', etc'''
    df = pd.read_csv(path)
    o = path.split('/')[-1].split('_')[0]
    ax = sns.catplot(x = 'substrate', y = fig_o_merit, hue = 'position', data = df)
    ax.set(title = fig_o_merit + ' by position')
    plt.savefig('Figures/char_data/'+ o + '/' + fig_o_merit + '.pdf')
    plt.close('all')

def plot_many_char_data(path):
    plot_char_data(path, 'Voc V')
    plot_char_data(path, 'Isc A')
    plot_char_data(path, "Efficiency")
    plot_char_data(path, 'Fill Factor')


def read_IV_data(exp_date):
    df = pd.DataFrame()
    for file in glob.glob('Data/IV_data/' + exp_date + '/*'):
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

def save_IV_data(exp_date):
    '''The purpose of this function is to store the IV data as a single csv file.
    This means that the program will save time as it does not need to recreate the
    df from scratch every time'''
    df = read_IV_data(exp_date)
    df.to_csv('Data/IV_data/IV_csvs/' + exp_date + '_all_IV.csv', index = False)


def plot_IV_data_all(path):
    df = pd.read_csv(path)
    o = path.split('/')[-1].split('_')[0]
    df['Imeas'] *= 1000
    
    
    print(df)
    # fig, ax = plt.subplots()
    # ax.plot(df['Vmeas'], df['Imeas'], color = df['color'])
    
    ax = sns.lineplot(x = 'Vmeas', y = 'Imeas', hue = 'substrate', style = 'position', data = df, palette=substrate_palette, dashes = position_dashes)
    ax.set(xlabel = 'Voltage (V)', ylabel = 'Current (mA)', title = 'All IV curves')
    plt.savefig('Figures/' + o + '/all_IVdata.pdf')
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

    
