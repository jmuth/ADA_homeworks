import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

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