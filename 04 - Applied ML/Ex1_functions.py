def separator(x):
    if x <= 0.25:
        return 0
    elif x <= 0.5:
        return 1
    elif x <= 0.75:
        return 2
    elif x <= 1.:
        return 3

def binary_separator(x):
    if x <= 0.5:
        return 0
    else:
        return 1
    
def prepare_data(df, cols, sep):
    target = df['skin_colour']
    target = target.apply(sep)
    
    data = df.drop(cols, axis=1).as_matrix()
    print('data shape: '+str(data.shape))
    print('target shape: '+str(target.shape))
    return data, target