# Import Libraries
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import STOPWORDS
import nltk
import pycountry
from sklearn.feature_extraction.text import CountVectorizer
import random
import requests
import json
import nltk.sentiment
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from nltk.corpus import opinion_lexicon
from nltk.tokenize import treebank
from matplotlib import cm

def isolate_line(s, n, marker):
    start = s[:n].rfind(marker) + len(marker)
    if start < 0:
        start = 0
    sub_s = s[start:]
    end = sub_s.find(marker)
    if end < 0:
        end = len(s)
    final = sub_s[:end]
    return final

def make_frame(key, value):
    n_mention = int(len(value['mention']))
    pos = sum(value['pos'])/float(len(value['pos']))
    neg = sum(value['neg'])/float(len(value['neg']))
    df = pd.DataFrame([[key, n_mention, pos, neg]], columns=['country', 'n_mention', 'pos', 'neg'])
    return df

def demo_vader_instance(text):
    vader_analyzer = SentimentIntensityAnalyzer()
    #print(vader_analyzer.polarity_scores(text))
    return vader_analyzer

def sentiment_process(emails, countries, method):
	stopwords = list(STOPWORDS)
	cited_countries = {}

	for i in range(0, len(emails)):
	    #print(i)
	    # preparing the body text
	    body = str(emails.iloc[i].ExtractedBodyText)
	    body_lower = body.lower()
	    #subject = str(emails.iloc[i].ExtractedSubject).lower()
	    
	    # slitting it into an array and considering the lowercase version
	    body_array = body.split(" ")
	    body_array.extend(body_lower.split(" "))
	    
	    #subject = subject.split(" ")
	    
	    if body_array != "nan":  
	        for ctr in countries:
	            # for each way of mentioning the country, checking if in body
	            for mention in countries[ctr]:
	                #if (mention in body_array or mention in subject):
	                if (mention in body_array):
	                    #print('m: '+mention)
	                    # finding all mentions
	                    mentions = [m.start() for m in re.finditer(mention, body+body_lower)]
	                    #print('mentions: '+str(mentions))
	                    for start in mentions:
	                        # isolating sentence and running senti. analysis
	                        sentence = isolate_line(body+body_lower, start, '.')
	                        if method == 'vader':
		                        v = demo_vader_instance(sentence)
		                        senti = v.polarity_scores(sentence)
	                        elif method == 'liu':
	                            senti = demo_liu_hu_lexicon(sentence, plot=False)

	                        # storing the results in a dict
	                        if ctr in cited_countries:
	                            cited_countries[ctr]["nbr_mention"] += 1
	                            cited_countries[ctr]["mention"].append(mention)
	                            if method == 'vader':
		                            cited_countries[ctr]['pos'].append(senti['pos'])
		                            cited_countries[ctr]['neg'].append(senti['neg'])
	                            elif method == 'liu':
	                                cited_countries[ctr]['sentiment'] += senti
	                        else:
	                            subdic = {}
	                            if method == 'vader':
		                            subdic["pos"] = [senti['pos']]
		                            subdic['neg'] = [senti['neg']]
	                            elif method == 'liu':
	                                subdic["sentiment"] = senti
	                            subdic["nbr_mention"] = 1
	                            subdic["mention"] = [mention]
	                            cited_countries[ctr] = subdic
	                            subdic['sentence'] = sentence
	                        
	                        #print(sentence)
	                        #print(v.polarity_scores(sentence))
	                        #print(' ')
	                    break

	return cited_countries

def plot_frame(polarity, countries, n_mention, title):
	plt.figure(figsize=(15,5))
	# Set up colors : red to green
	y = np.array(n_mention)
	colors = cm.Blues(y / float(max(y)))
	plot = plt.scatter(y, y, c=y, cmap = 'Blues')
	plt.clf()
	clb = plt.colorbar(plot)
	clb.ax.set_title("Sentiment")

	plt.plot((-0.5, 38.5), (0, 0), 'grey', lw=1)
	plt.bar(range(len(countries)), polarity, align='center', tick_label=countries, width=0.5, color=colors)
	plt.xticks(rotation=45, ha='right');
	plt.title(title, fontsize=18, loc='left')
	plt.ylabel('Polarity')
	plt.xlabel('Countries')
	plt.show()