import numpy as np 
import pandas as pd 

def coucou():
	print('COUCOU')


def sum_by_university(df, name):
    return df.loc[df['University'] == name, 'Approved Amount'].sum()


def sum_by_canton(df, canton):
    total = 0
    for name in cantons['AG']:
        total += sum_by_university(df, name) 

    return total