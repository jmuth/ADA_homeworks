import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit

#################### Supervised Learning ####################

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
        return 0.
    elif x <= 0.5:
        return 1.
    elif x <= 0.75:
        return 2.
    elif x <= 1.:
        return 3.

def binary_separator(x):
    if x <= 0.5:
        return 0.
    else:
        return 1.
    
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
    ax.set_xticks(np.arange(0.5, n_col+0.5, 1))
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

    return forest, metrics.accuracy_score(target_holdout, pred_holdout)

def plot_cnf(cnf, classes):
    plt.figure()
    plt.imshow(cnf, interpolation='none', cmap=plt.cm.Blues)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)
    plt.tight_layout()
    plt.ylabel('True')
    plt.xlabel('Predicted')

def whole_process(df, cols, b):
    data, target, labels = prepare_data(df, cols, b)

    # preparing the hold-out data
    n = len(target)-50
    data_holdout = data[n:,]
    target_holdout = target[n:]
    data = data[:n,]
    target = target[:n]

    # we will keep track of the accuracy
    acc = []
    forest = RandomForestClassifier(n_estimators = 100, max_features=0.33, max_depth=10, n_jobs=-1)
    kf = KFold(n_splits=10)

    for train, test in kf.split(data):
        forest.fit(data[train], target[train])
        # keeping track of the accuracy
        predi = forest.predict(data[test])
        acc.append(metrics.accuracy_score(predi, target[test]))

    print(' ')
    print('predicting..')
    print(' ')
    # predictions
    pred = forest.predict(data)
    print('Accuracy details for whole data:')
    details(pred, target)
    predi = forest.predict(data_holdout)
    print(' ')
    print('Accuracy details for holdout data:')
    details(predi, target_holdout)

    # confusion matrices
    cnf1 = metrics.confusion_matrix(target, pred)
    cnf2 = metrics.confusion_matrix(target_holdout, predi)

    return forest, cnf1, cnf2, labels

def details(pred, target):
    # divide into two classes
    target0 = []
    pred0 = []

    target1 = []
    pred1 = []

    for i, t in enumerate(target):
        if t:
            target1.append(t)
            pred1.append(pred[i])
        else:
            target0.append(t)
            pred0.append(pred[i])
    
    print(' ')   
    print('# of people with light skin: %s' % len(target0))
    print('# of people with dark skin: %s' % len(target1))
    print(' ')
    print('accuracy for light skin: %s' % metrics.accuracy_score(target0, pred0))
    print('accuracy for dark skin: %s' % metrics.accuracy_score(target1, pred1))

#################
## the following comes from http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

def make_learning_curve(data, target, title, **kwargs):
    X, y = data, target

    # Cross validation with 100 iterations to get smoother mean test and train
    # score curves, each time with 20% data randomly selected as a validation set.
    cv = ShuffleSplit(n_splits=20, test_size=0.2, random_state=0)

    estimator = RandomForestClassifier(n_estimators=100)
    plot_learning_curve(estimator, title, X, y, ylim=(0.7, 1.02), cv=cv, n_jobs=1)

    plt.show()

#################### Unsupervised Learning ####################

def plot_dict(dictionnary, dictionnary2, base_sil, base_score, title='', labelx='', labely='', size=(15, 4)):
  ## variable
  y = list(dictionnary.values())
  y2 = list(dictionnary2.values())
  x = np.arange(len(y))
  labels = list(dictionnary.keys())

  miny = min(y + y2)
  maxy = max(y + y2)



  fig = plt.figure(figsize=size)
  ax = fig.add_subplot(111)

  ## necessary variables
  ind = np.arange(len(y))     # the x locations for the groups
  width = 0.35                # the width of the bars

  ## axes label
  ax.set_title(title)
  xTickMarks = labels
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)
  plt.bar(x, y, width ,color='r')
  plt.bar(x + width, y2, width, color='y')
  plt.xlabel(labelx)
  plt.ylabel(labely)
  plt.ylim([miny -0.1, maxy + 0.1])

  #vert line
  plt.axhline(y=base_sil,color='r',ls='dashed')
  plt.axhline(y=base_score,color='y',ls='dashed')

  return fig

def plot_array(x_names, y, y2,base_sil, base_score, title='', labelx='', labely='', size=(15, 4)):
  ## variable
  x = np.arange(len(x_names))
  labels = x_names

  miny = min(y + y2)
  maxy = max(y + y2)


  fig = plt.figure(figsize=size)
  ax = fig.add_subplot(111)

  ## necessary variables
  ind = np.arange(len(y))     # the x locations for the groups
  width = 0.35                # the width of the bars

  ## axes label
  ax.set_title(title)
  xTickMarks = labels
  ax.set_xticks(ind+width)
  xtickNames = ax.set_xticklabels(xTickMarks)
  plt.setp(xtickNames, rotation=45, fontsize=10)
  plt.bar(x, y, width ,color='r')
  plt.bar(x + width, y2, width, color='y')
  plt.xlabel(labelx)
  plt.ylabel(labely)
  plt.ylim([miny -0.1, maxy + 0.1])

  #vert line
  plt.axhline(y=base_sil,color='r',ls='dashed')
  plt.axhline(y=base_score,color='y',ls='dashed')

  return fig