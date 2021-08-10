
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:50:22 2021

@author: Ethan Davis
"""

"""Generate figures for the arXIV version"""



import numpy as np
import pandas as pd
from datetime import date
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import json


"""Twitter timeseries figures"""

#load twitter data for 2 and 3grams
three_twitter = pd.read_csv("all_three_grams.csv")
two_twitter = pd.read_csv("all_two_grams.csv", index_col=0)
top_three_twitter = sorted([(three_twitter[three_twitter.proverb ==x].counts.sum(), x) for x in set(three_twitter.proverb)], reverse = True)
top_two_twitter =  sorted([(two_twitter[two_twitter.proverb ==x].counts.sum(), x) for x in set(two_twitter.proverb)], reverse = True)

today = date.today().strftime('%m-%d-%y')

def individual_plot_twitter(proverb, data, res=None, date_range = None, rt = False):
    """
    Plot timeseries for single Twitter ngram
    Takes list of proverbs, timeseries data (df) as arguments
    Plots daily frequency and rolling 30-day average
    """
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 12,
        'axes.labelsize': 14,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
    })
    fig, ax = plt.subplots(figsize=(12, 5.75))

    ax.text(0.04,0.95,"\"{}\"".format(proverb),horizontalalignment='left', transform=ax.transAxes)

    #get data for one proverb
    ts = data[data.proverb ==proverb]

    ts.date = pd.to_datetime(ts.date, format = '%Y-%m-%d', errors='coerce')
    ts.index = ts.date
    ts = ts.sort_index()
    print(ts)
    
    ts2 = ts.copy()[['freq_noRT', 'freq']]
    
    #30 day rolling average
    ts2 = ts2.rolling(30).mean()
    
    #including or excluding retweets
    if rt == False:
        ax.plot(ts.index, ts['freq_noRT'], alpha = 0.5, marker = 'o', fillstyle = 'none', color='gray')
        ax.plot(ts2.index, ts2['freq_noRT'], alpha = 0.9, color='darkorange', linewidth = 2)
    elif rt == True:
        ax.plot(ts.index, ts['freq'], alpha = 0.5, marker = 'o', fillstyle = 'none', color='gray')
        ax.plot(ts2.index, ts2['freq'], alpha = 0.9, color='darkorange', linewidth = 2)
    
    ax.set_xlabel('Year')
    ax.set_yscale('log')
    ax.set_ylabel('Frequency among all {}-grams on Twitter'.format(len(proverb.split())))

    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)


#plot example proverbs
individual_plot_twitter('never say never', three_twitter)
plt.savefig('arxiv_figures/never-twitter-{}.pdf'.format(today))

individual_plot_twitter('enough is enough', three_twitter)
plt.savefig('arxiv_figures/enough-twitter-{}.pdf'.format(today))

individual_plot_twitter('time flies', two_twitter)
plt.savefig('arxiv_figures/time-twitter-{}.pdf'.format(today))



def grid_plot_twitter(proverbs_list, data,dim = (4,4), ylog = False, rt = False):    
    """
    Plot grid of Twitter timeseries (frequency)
    Takes list of proverbs, timeseries data (df), and grid dimension as arguments
    Plots daily frequency and rolling 30-day average
    """    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 14,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'legend.fontsize': 10,
    })
    
    rows, cols = dim[0],dim[1]
    fig = plt.figure(figsize=(12, 5.75))
    gs = gridspec.GridSpec(ncols=cols, nrows=rows)
    gs.update(wspace = 0.2, hspace = 0.2)
  
 
    i = 0
    
    fig.text(0.5, 0.02,'Year' , ha='center', fontsize = 14)
    fig.text(0.02, 0.5, 'Frequency among all {}-grams on Twitter'.format(len(proverbs_list[0].split())), va='center', rotation='vertical', fontsize = 14)
    
    #loop to create each timeseries plot in the grid
    for r in np.arange(0, rows, step=1):
        for c in np.arange(cols):

            ax = fig.add_subplot(gs[r, c])

            ax.text(0.1,0.9,'\"{}\"'.format(proverbs_list[i]),horizontalalignment='left', transform=ax.transAxes)
            ts = data[data.proverb ==proverbs_list[i]]
            ts.date = pd.to_datetime(ts.date, format = '%Y-%m-%d', errors='coerce')
            ts.index = ts.date
            ts = ts.sort_index()
            print(ts)
            ts2 = ts.copy()[['freq_noRT', 'freq']]
            print(ts2)
            ts2 = ts2.rolling(window=30).mean()
            print(ts2)

    
            if ylog == False:
                pass

            elif ylog == True:
                ax.set_yscale('log') 

            if rt == False:
                ax.plot(ts.index, ts['freq_noRT'], alpha = 0.5, color = 'gray')
                ax.plot(ts2.index, ts2['freq_noRT'], alpha = 0.9, color='darkorange')                
            
            elif rt ==True:
                ax.plot(ts.index, ts['freq'], alpha = 0.5, color = 'gray')
                ax.plot(ts2.index, ts2['freq'], alpha = 0.9, color='darkorange')
            i+=1
            
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)


grid_plot_twitter([a[1] for a in top_three_twitter][:16], three_twitter, ylog= True)
plt.savefig('arxiv_figures/twitter-3gram-grid-{}.pdf'.format(today))

grid_plot_twitter([a[1] for a in top_two_twitter][:9], two_twitter, dim = (3,3), ylog= True)
plt.savefig('arxiv_figures/twitter-2gram-grid-{}.pdf'.format(today))


grid_plot_twitter([a[1] for a in top_three_twitter][16:32], three_twitter, ylog= True)
plt.savefig('arxiv_figures/twitter-3gram-grid2-{}.pdf'.format(today))



"""Google n-grams plots"""

two_google = pd.read_csv('google-2-gram-ts-revised_no_tags.csv', index_col=0)

three_google = pd.read_csv('google-3-gram-ts-revised_no_tags.csv', index_col=0)

top_three_google =  sorted([(three_google[three_google.proverb ==x].match.sum(), x) for x in set(three_google.proverb)], reverse = True)
top_two_google =  sorted([(two_google[two_google.proverb ==x].match.sum(), x) for x in set(two_google.proverb)], reverse = True)



def grid_plot_google(proverbs_list, data, dim = (4,4), ylog = False):    
    """
    Plot grid of Google timeseries (frequency)
    Takes list of proverbs, timeseries data (df), and grid dimension as arguments
    Plots yearly frequency and rolling 5-year average
    """   

    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 14,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'legend.fontsize': 10,
    })
        
    rows, cols = dim[0], dim[1]
    fig = plt.figure(figsize=(12, 5.75))
    gs = gridspec.GridSpec(ncols=cols, nrows=rows)
    gs.update(wspace = 0.2, hspace = 0.2)
    
    
    res = None
     
    i = 0
    
    fig.text(0.5, 0.02,'Year' , ha='center', fontsize=14)
    fig.text(0.02, 0.5, 'Frequency among all volumes in Google Books', va='center', rotation='vertical', fontsize=14)
    for r in np.arange(0, rows, step=1):
        for c in np.arange(cols):

            ax = fig.add_subplot(gs[r, c])
            ax.text(0.1,0.9,'\"{}\"'.format(proverbs_list[i].lower()),horizontalalignment='left', transform=ax.transAxes)

            ts = data[data.proverb ==proverbs_list[i]]
            ts = ts[data.year >= 1800]
            ts.year = pd.to_datetime(ts.year, format = '%Y', errors='coerce')
            ts.index = ts.year
            ts = ts.sort_index()
            ts = ts.reindex(pd.date_range('01/01/1800', '01/01/2019', freq = 'AS'), fill_value=0)
            #get 5-year rolling average
            ts2 = ts.copy()
            ts2 = ts2.rolling(window = 5).mean()
            print(ts)

            if res != None:
                ts = ts.resample(res).sum()
    
            if ylog == False:
                pass

            elif ylog == True:
                ax.set_yscale('log')    
                
            ax.plot(ts.index, ts['vol_norm'], alpha = 0.5, color = 'gray')
            ax.plot(ts2.index, ts2['vol_norm'], alpha = 0.9, color='darkorange')
            i+=1
          
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)


grid_plot_google([a[1] for a in top_three_google][1:17], three_google, ylog = False)
plt.savefig('arxiv_figures/google-3gram-grid-{}.pdf'.format(today))


grid_plot_google([a[1] for a in top_two_google][:12] ,two_google,dim = (4,3),  ylog = False)
plt.savefig('arxiv_figures/google-2gram-grid-{}.pdf'.format(today))


grid_plot_google([a[1] for a in top_three_google][17:33], three_google, ylog = False)
plt.savefig('arxiv_figures/google-3gram-grid2-{}.pdf'.format(today))



"""Gutenberg grid plots"""


gutenberg = pd.read_csv('proverb_timeseries.csv', index_col = 'year')
counts = pd.read_csv('proverb_counts.csv')

def grid_plot_gutenberg(proverbs_list, data, counts, begin_at =1800, end_at = 1950, bin_size = 20):
    """
    Plot grid of Gutenberg timeseries (frequency)
    Takes list of proverbs, timeseries data (df), start/end year, bin size, and grid dimension as arguments
    Default plot is in 20-year bins
    """   
    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 14,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'legend.fontsize': 10,
    })
    
    rows, cols = 4, 4
    fig = plt.figure(figsize=(12, 5.75))
    gs = gridspec.GridSpec(ncols=cols, nrows=rows)
    gs.update(wspace = 0.2, hspace = 0.2)  
    
    
    i = 0
    
    fig.text(0.5, 0.02,'Year' , ha='center', fontsize=14)
    fig.text(0.02, 0.5, 'Frequency among all volumes in Gutenberg', va='center', rotation='vertical', fontsize=14)
    
    ts = data.copy()
    ts_bin = ts.groupby(lambda x: (x//bin_size)*bin_size).sum()
    ts_norm = ts_bin.div(ts_bin['num_books'], axis=0)
    ts_norm = ts_norm.fillna(0)
    ts = ts_norm.truncate(before = begin_at, after = end_at)[proverbs_list]

    #loop to create each timeseries plot in the grid
    for r in np.arange(0, rows, step=1):
        for c in np.arange(cols):

            ts2 = ts[proverbs_list[i]].to_frame()

            ax = fig.add_subplot(gs[r, c])

            ax.text(0.1,0.9,'\"{}\"'.format(proverbs_list[i]),horizontalalignment='left', transform=ax.transAxes)

            ax.plot(ts2.index, ts2[proverbs_list[i]], alpha = 0.5)
            i+=1
            
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)


#plot top 16, and 17-32 (#1 "hold your tongue" excluded)            
grid_plot_gutenberg(list(counts[1:17]['proverbs']), gutenberg, counts, bin_size =5)            
plt.savefig('arxiv_figures/gutenberg-grid-{}.pdf'.format(today))
           
grid_plot_gutenberg(list(counts[17:33]['proverbs']), gutenberg, counts, bin_size =5)            
plt.savefig('arxiv_figures/gutenberg-grid2-{}.pdf'.format(today))
               


"""NYT GRID PLOT"""
#data for proverbs in NYT
ts = pd.read_csv('nyt_ts_new.csv', index_col = 0)
ts = ts.set_index(pd.to_datetime(ts.index))
nyt_totals = [(ts.iloc[:,i].name, ts.iloc[:,i].sum()) for i in range(len(ts.columns)) if ts.columns[i] != 'total']
nyt_totals.sort(key = lambda x :x[1], reverse=True)
proverbs_list = [a[0] for a in nyt_totals]


#data for number of articles each day
with open('nyt_date_totals.json', 'r') as fp:
    f = json.load(fp)    
date_totals = pd.Series(f)
date_totals.index = pd.to_datetime(date_totals.index)
ts['total'] = date_totals


def grid_plot_nyt(proverbs_list, data, dim = (4,4), res = '1M'):
    """
    Plot grid of NYT timeseries (frequency over articles)
    Takes list of proverbs, timeseries data (df), and grid dimension as arguments
    Plots monthly and yearly average
    """
    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 14,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'legend.fontsize': 10,
    })
    
    rows, cols = dim[0], dim[1]
    fig = plt.figure(figsize=(12, 5.75))
    gs = gridspec.GridSpec(ncols=cols, nrows=rows)
    gs.update(wspace = 0.3, hspace = 0.2)
    

    i = 0
    
    fig.text(0.5, 0.02,'Year' , ha='center', fontsize=14)
    fig.text(0.02, 0.5, 'Frequency among all articles in NYT', va='center', rotation='vertical', fontsize=14)
    
    #get month resolution
    ts = data.copy()
    resamp = ts.resample(res).sum()
    resamp = resamp.div(resamp['total'], axis =0)
    ts = resamp
    
    #get year resolution
    ts2 = data.copy()
    resamp = ts.resample('1Y').sum()
    resamp = resamp.div(resamp['total'], axis =0)
    ts2 = resamp
    
    #make each plot in the grid
    for r in np.arange(0, rows, step=1):
        for c in np.arange(cols):

            ax = fig.add_subplot(gs[r, c])

            ax.text(0.1,0.9,'\"{}\"'.format(proverbs_list[i]),horizontalalignment='left', transform=ax.transAxes)

            print(ts[proverbs_list[i]])
            ax.plot(ts.index, ts[proverbs_list[i]], alpha = 0.5, color = 'gray')
            ax.plot(ts2.index, ts2[proverbs_list[i]], alpha = 0.9, color = 'orange')
            i+=1
            
    plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.1)


#plot top 16, and 17-32
grid_plot_nyt(proverbs_list[0:16], ts)
plt.savefig('arxiv_figures/nyt-grid-{}.pdf'.format(today))
   

grid_plot_nyt(proverbs_list[16:32], ts)
plt.savefig('arxiv_figures/nyt-grid2-{}.pdf'.format(today))
 

"""Zipf Plots"""

from collections import Counter
from adjustText import adjust_text


"""Gutenberg Zip"""
counts = pd.read_csv('proverb_counts.csv')
gut_counts= counts[['counts', 'proverbs']]
gut_counts = list(zip(list(gut_counts.proverbs), list(gut_counts.counts)))

def Zipf_Gutenberg(data, data_type='obs', fit =False):
    """Zipf (rank/frequency) plot for proverbs in Gutenberg"""
    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 12,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
    })
    

    if data_type == 'obs':
        counts=Counter(data)
        freq = sorted(list(counts.items()), reverse = True, key = lambda x:x[1])
        print(freq[:5])       
    elif data_type == 'freq':
        freq = data
    
    
    x = np.array([x for x in range(1,len(freq)+1)]).reshape(-1,1)
    y = np.array([y[1] for y in freq]).reshape(-1,1)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(x, y, marker = 'o', fillstyle = 'none', linestyle = 'none', mec='lightblue')
    texts = [plt.text(x[i], y[i], freq[i][0], fontsize=9) for i in range(5)]
    adjust_text(texts, arrowprops=dict(arrowstyle='-'))

    
Zipf_Gutenberg(gut_counts, data_type='freq')


     
"""Google Zipf"""

counts =[]
for proverb in set(three_google['proverb']):
    s = three_google[three_google['proverb'] == proverb]['match'].sum()
    counts += [(proverb, s)]

counts.sort(reverse = True, key = lambda x: x[1])

top_three_google =  sorted([(three_google[three_google.proverb ==x].match.sum(), x.lower()) for x in set(three_google.proverb)], reverse = True)[1:]
top_two_google =  sorted([(two_google[two_google.proverb ==x].vol_norm.sum(), x.lower()) for x in set(two_google.proverb)], reverse = True)

def Zipf_Google(data, data_type='obs', fit =False):
    """Zipf (rank/frequency) plot for proverbs in Google books"""
    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 12,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
    })
    

    if data_type == 'obs':
        counts=Counter(data)
        freq = sorted(list(counts.items()), reverse = True, key = lambda x:x[1])
        print(freq[:5])       
    elif data_type == 'freq':
        freq = data

    x = np.array([x for x in range(1, len(freq)+1)])
    y = np.array([y[0] for y in freq])
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(x, y, marker = 'o', fillstyle = 'none', linestyle = 'none', mec='lightblue')
    texts = [plt.text(x[i], y[i], freq[i][1], fontsize=9) for i in range(5)]
    adjust_text(texts, arrowprops=dict(arrowstyle='-'))

    
Zipf_Google(top_three_google, data_type='freq')
Zipf_Google(top_two_google, data_type='freq')


"""Twitter Zipf"""


def Zipf(data, data_type='obs', fit =False):
    """Zipf (rank/frequency) plot for proverbs on Twitter"""
    
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 12,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
    })
    

    if data_type == 'obs':
        counts=Counter(data)
        freq = sorted(list(counts.items()), reverse = True, key = lambda x:x[1])
        print(freq[:5])       
    elif data_type == 'freq':
        freq = data

    x = np.array([x for x in range(1, len(freq)+1)]).reshape(-1,1)
    y = np.array([y[0] for y in freq]).reshape(-1,1)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(x, y, marker = 'o', fillstyle = 'none', linestyle = 'none', mec='lightblue')
    texts = [plt.text(x[i], y[i], freq[i][1], fontsize=9) for i in range(5)]
    adjust_text(texts, arrowprops=dict(arrowstyle='-'))

    
Zipf(top_three_twitter, data_type='freq')
   

"""NYT Zipf"""
import pandas as pd
import matplotlib.pyplot as plt
ts = pd.read_csv('nyt_ts.csv', index_col = 0)
ts = ts.set_index(pd.to_datetime(ts.index))

totals = [(ts.iloc[:,i].name, ts.iloc[:,i].sum()) for i in range(len(ts.columns)) if i != 'total']
totals.sort(key = lambda x :x[1], reverse=True)

def Zipf(data, data_type='obs', fit =False):
    """Zipf (rank/frequency) plot for proverbs in Gutenberg"""
     
    plt.rcParams.update({
        'font.size': 9,
        'axes.titlesize': 8,
        'axes.labelsize': 12,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 10,
    })


    if data_type == 'obs':
        counts=Counter(data)
        freq = sorted(list(counts.items()), reverse = True, key = lambda x:x[1])
        print(freq[:5])       
    elif data_type == 'freq':
        freq = data

    x = np.array([x for x in range(1,len(freq)+1)]).reshape(-1,1)
    y = np.array([y[1] for y in freq]).reshape(-1,1)
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(x, y, marker = 'o', fillstyle = 'none', linestyle = 'none', mec='lightblue')
    print(x[0], y[0], freq[0][0])
    texts = [plt.text(x[i], y[i], freq[i][0], fontsize=9) for i in range(5)]
    adjust_text(texts, arrowprops=dict(arrowstyle='-'))


Zipf(totals, data_type='freq')
        



"""Create frequency tables for each corpus"""

google_50 = pd.DataFrame({'Proverb': [a[1].lower() for a in top_three_google][:50], 'Count': [format(a[0], ',') for a in top_three_google][:50]})
google_50.index = google_50.index+1

google_50.to_latex('thesis_figures/google_50_table.tex')



twitter_50 = pd.DataFrame({'Proverb': [a[1] for a in top_three_twitter][:50], 'Count': [format(int(a[0]), ',') for a in top_three_twitter][:50]})
twitter_50.index = twitter_50.index+1

twitter_50.to_latex('thesis_figures/twitter_50_table.tex')



gut_50 = pd.DataFrame({'Proverb': [a[0] for a in gut_counts][:50], 'Count': [format(int(a[1]), ',') for a in gut_counts][:50]})
gut_50.index = gut_50.index+1

gut_50.to_latex('thesis_figures/gut_50_table.tex')



nyt_50 = pd.DataFrame({'Proverb': [a[0] for a in nyt_totals][:50], 'Count': [format(int(a[1]), ',') for a in nyt_totals][:50]})
nyt_50.index = nyt_50.index+1

nyt_50.to_latex('thesis_figures/nyt_50_table.tex')




"""Table for betweenness centrality in book-proverb network"""

with open('book_btwn_rank.json', 'r') as file:
    btwn = json.load(file)

item = list(btwn.items())
item.sort(reverse=True, key = lambda x: x[1])


df = pd.DataFrame(item, columns = ['book','btwn centrality' ])
df.index+=1


with pd.option_context('display.max_colwidth', -1): 
    df.iloc[:20].to_latex('btwn_top_20_book.tex')
