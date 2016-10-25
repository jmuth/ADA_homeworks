import numpy as np 
import pandas as pd 

def sum_by_university(df, name):
    return df.loc[df['University'] == name, 'Approved Amount'].sum()

def sum_by_canton(df, cantons, name):
    total = 0
    for name in cantons[name]:
        total += sum_by_university(df, name) 

    return total