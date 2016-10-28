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
	
def plot_hist_cantons(dictionnary, title='', labelx='', labely='', size=(15, 4), log=False):
	fig, x, y_sorted, labels_sorted = plot_dict(dictionnary, title, labelx, labely, size)
	
	# Different speaking cantons. The other cantons are german-speaking cantons. 
	# There's not real Rumantsch speaking cantons.
	swiss_french = ['FR', 'NE', 'VS', 'VD', 'JU', 'GE']
	swiss_italian = ['TI']
	
	# Indexes for the legend
	idx_sw_fr = 0
	idx_sw_ge = 0
	idx_sw_it = 0
	
	# Get the color for each cantons
	colors = []
	for idx, cts in enumerate(labels_sorted):
		if cts in swiss_french:
			colors.append('green')
			if idx_sw_fr == 0:
				idx_sw_fr = idx
		elif cts in swiss_italian:
			colors.append('violet')
			if idx_sw_it == 0:
				idx_sw_it = idx			
		else:
			colors.append('orange')
			if idx_sw_ge == 0:
				idx_sw_ge = idx			

	## plt
	if log:
		p = plt.bar(x, np.log10(y_sorted), color=colors)
	else:
		p = plt.bar(x, y_sorted, color=colors)
	plt.legend([p[idx_sw_ge], p[idx_sw_fr], p[idx_sw_it]], ['Swiss-German canton', 'Swiss-French canton', 'Swiss-Italian canton'])	
	plt.show()
	
def plot_hist_regions(dictionnary, title='', labelx='', labely='', size=(15, 4), log=False):
	fig, x, y_sorted, labels_sorted = plot_dict(dictionnary, title, labelx, labely, size)
	
	# With only 4 different regions, we don't have to do a for loop here. We just insert the 
	# colors for each region knowing that Swiss-German is first, Swiss-French is second and 
	# Swiss-Italian is last.
	colors = ['orange', 'green', 'violet', 'blue']
	p = plt.bar(x, y_sorted, color=colors)
	
def plot_dict(dictionnary, title='', labelx='', labely='', size=(15, 4)):
	## variable
	y = list(dictionnary.values())
	x = range(len(y))
	labels = list(dictionnary.keys())
    
	idx_sorted_by_value = sorted(range(len(y)),key=lambda idx:y[idx], reverse=True)
	
	y_sorted = []
	labels_sorted = []
	for i in idx_sorted_by_value:
		y_sorted.append(y[i])
		labels_sorted.append(labels[i])

	fig = plt.figure(figsize=size)
	ax = fig.add_subplot(111)

	## necessary variables
	ind = np.arange(len(y))     # the x locations for the groups
	width = 0.35                # the width of the bars

	## axes label
	ax.set_title(title)
	xTickMarks = labels_sorted
	ax.set_xticks(ind+width)
	xtickNames = ax.set_xticklabels(xTickMarks)
	plt.setp(xtickNames, rotation=45, fontsize=10)
	plt.xlabel(labelx)
	plt.ylabel(labely)

	return fig, x, y_sorted, labels_sorted