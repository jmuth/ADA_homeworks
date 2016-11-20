import pandas as pd
import matplotlib.pyplot as plt
# train/test library import
from sklearn.cross_validation import train_test_split
from sklearn import metrics

# these are the features of our dataset
orig_cols = ['height', 
        'weight', 
        'games', 
        'victories', 
        'ties', 
        'defeats', 
        'goals', 
        'yellowCards',
        'yellowReds',
        'redCards',
        'skin_colour', 
        'gravity',
        'meanIAT_yellowCards',
        'meanIAT_yellowReds', 
        'meanIAT_redCards',
        'meanIAT_gravity',
        'meanExp_yellowCards',
        'meanExp_yellowReds', 
        'meanExp_redCards',
        'meanExp_gravity'
       ]

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
    print('df shape: '+str(df.shape))
    data = df.drop(cols, axis=1).as_matrix()
    print('data shape: '+str(data.shape))
    print('target shape: '+str(target.shape))
    labels = [y for y in orig_cols if not (y in cols)]
    return data, target, labels

def impo_graph(imp, labels):
    importance = pd.DataFrame([imp], columns = labels)
    n_col = len(labels)

    # graph
    fig, ax = plt.subplots()
    ax.bar(range(len(imp)), imp)
    ax.set_xticks(range(0, n_col))
    ax.set_xticklabels(importance.columns, rotation=90)

    return ax

def train_test_RF(forest, data, target, holdout_size):
    # n is where the data will be sliced
    n = len(target) - holdout_size

    # slicing the data
    data_holdout = data[n:,]
    target_holdout = target[n:]
    data = data[:n,]
    target = target[:n]

    # train/test split
    data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2)

    # training
    forest.fit(data_train, target_train)
    pred = forest.predict(data_test)
    pred_holdout = forest.predict(data_holdout)

    # printing accuracy
    s = 'Accuracy on test data: %s' % (metrics.accuracy_score(target_test, pred))
    #print(s)
    #print(' ')
    s2 = 'Accuracy on held out data %s' % (metrics.accuracy_score(target_holdout, pred_holdout))
    # print(s2)

    return forest