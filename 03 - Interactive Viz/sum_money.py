import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

def sum_by_university(df, name):
    return df.loc[df['University'] == name, 'Approved Amount'].sum()

def sum_by_canton(df, cantons, name):
    total = 0
    for name in cantons[name]:
        total += sum_by_university(df, name) 

    return total

def sum_by_region(df, canton_money, region):
	money = 0
	for canton in region:
		money += canton_money[canton]

	return money

def plot_dict(dictionnary, title='', labelx='', labely='', size=(15, 4)):
	## variable
	y = list(dictionnary.values())
	x = range(len(y))
	labels = list(dictionnary.keys())

	fig = plt.figure(figsize=size)
	ax = fig.add_subplot(111)

	## necessary variables
	ind = np.arange(len(y))                # the x locations for the groups
	width = 0.35                      # the width of the bars

	## axes label
	ax.set_title(title)
	xTickMarks = labels
	ax.set_xticks(ind+width)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation=45, fontsize=10)
	plt.xlabel(labelx)
	plt.ylabel(labely)

	## plt
	plt.bar(x, y)


	plt.show()