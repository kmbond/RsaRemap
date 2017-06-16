from __future__ import division

import sys
import pandas as pd
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import itertools
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels
import fnmatch
import seaborn as sns
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from sklearn.preprocessing import normalize
import glob
import time
import warnings

os.chdir(os.path.expanduser('~/Dropbox/modmap/behavior/'))
out_path = os.path.expanduser('~/Dropbox/modmap/analysis/')

sns.set_context(context='paper', font_scale=2.0)


#house keeping, delete old files that are no longer needed
for svg in glob.glob(os.path.expanduser('~/Dropbox/modmap/analysis/*.svg')):
    os.remove(svg)
#initialize common group dict of dataframes
group_rts = {}
group_acc= {}
group_acfs = {}
group_dict = {'r':'cue', 'c':'response'}
for group in ['r', 'c']:

    summary_files = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*summary*' + group + '.csv'):
            summary_files.append(file)
    #get unique subjects
    subs = []
    for i in range(0, len(summary_files)):
        subs.append(summary_files[i][:4])
    uniqueSubs = list(set(subs))
    for sub in uniqueSubs:
        Acc = pd.DataFrame(columns=('Day', 'randAcc', 'seqAcc'))
        RT = pd.DataFrame(columns = ('Day', 'zscoredRT'))
        sdRT = pd.DataFrame(columns = ('Day', 'sdRTseq','sdRTrand', 'sdRatio'))
        lag_names = ['lag' + str(i) for i in  range(1,16)]
        chunkSizeSeq = pd.DataFrame(columns=('Day', 'chunkSize'))
        chunkSizeRand = pd.DataFrame(columns=('Day', 'chunkSize'))
        randLags = pd.DataFrame(columns = lag_names)
        seqLags = pd.DataFrame(columns = lag_names)
        df = pd.DataFrame()
        sub_files = []

        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, sub+'*summary*' + '.csv'):
                sub_files.append(file)

        for day in sub_files:
            df = pd.read_csv(day)
            Acc.loc[int(day[day.find('session')+8:-12])] = [int(day[day.find('session')+8:-12]),df['accuracy'][5], df['accuracy'][6]]
            zscoreRT = (df['rt_all'][5] - df['rt_all'][6])/df['sdRT'][5]
            RT.loc[int(day[day.find('session')+8:-12])] = [int(day[day.find('session')+8:-12]), zscoreRT]
            sdRT.loc[int(day[day.find('session')+8:-12])] = [int(day[day.find('session')+8:-12]), df['sdRT'][6],df['sdRT'][5], df['sdRT'][6]/df['sdRT'][5]]
            randLags.loc[int(day[day.find('session')+8:-12])] = df[lag_names].loc[5]
            seqLags.loc[int(day[day.find('session')+8:-12])] = df[lag_names].loc[6]

        #chunkSizeSeq.loc[int(day[day.find('session')+8:-12])] = [int(day[day.find('session')+8:-12]), df['chunkSize'][6]]
        #chunkSizeRand.loc[int(day[day.find('session')+8:-12])] = [int(day[day.find('session')+8:-12]), df['chunkSize'][5]]
        randLags = randLags.sort_index(axis=0)
        seqLags = seqLags.sort_index(axis=0)

        # Generate autocorrelation plots
        sns.set_context(context='paper', font_scale=2.0)
        sns.set_style("ticks")
        fig = plt.figure(figsize=(8,12))
        ax1 = fig.add_subplot(321)
        ax2 = fig.add_subplot(322)

        #Generate Accuracy Plots for the Sequence
        plt.subplot(321)
        Acc.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'seqAcc',data=Acc, fit_reg=False, ax=ax1, scatter_kws={'s':40})
        plt.axis([0,11,.5,1])
        plt.xticks(np.arange(1,11,1))
        plt.ylabel('Accuracy')
        plt.xlabel('Day')
        plt.title('Accuracy')

        #Generate RT plots
        plt.subplot(322)
        RT.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'zscoredRT',data=RT, fit_reg=False, ax=ax2, scatter_kws={'s':40})
        plt.axis([0,11,0,8])
        plt.xticks(np.arange(1,11,1))
        plt.ylabel('Reaction Time (z-units)')
        plt.title('Speed')
        plt.xlabel('Day')
        sns.despine(offset=.1, trim=True);

        fig.add_subplot(312)
        fig.add_subplot(313)

        plt.subplot(312)
        blues = plt.get_cmap('Blues')
        # Random
        for i in range(1,len(randLags)+1):
            colorBlue = blues(.05 + float(i)/(len(randLags)+1))
            plt.plot(range(1,16),randLags.loc[i], color = colorBlue, label = 'Day ' + str(i))

        box = plt.gca().get_position()
        plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.xlabel('Lag (Trials)')
        plt.ylabel('Correlation')
        legend = plt.legend(loc='upper right', ncol=1, prop={'size':8}, title='Training Day')
        plt.setp(legend.get_title(),fontsize='xx-small')

        plt.title('Random Block', y=0.9)
        plt.axis([0.5,16, -0.5,1])
        plt.xticks(np.arange(1,16,1))
        plt.yticks(np.arange(-.5,1,0.25))
        sns.despine(offset=.25, trim=True);
        sns.set_style("ticks")

        plt.subplot(313)
        greens = plt.get_cmap('Greens')
        for i in range(1,len(randLags)+1):
            colorGreen = greens(.05 + float(i)/(len(randLags)+1))
            plt.plot(range(1,16),seqLags.loc[i], color = colorGreen, label = 'Day ' + str(i))

        box = plt.gca().get_position()
        plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.xlabel('Lag (Trials)')
        plt.ylabel('Autocorrelation' )
        legend = plt.legend(loc='upper right', ncol=1, prop={'size':8}, title='Training Day')
        plt.setp(legend.get_title(),fontsize='xx-small')
        plt.title('Sequence Block', y=0.9)
        plt.axis([0.5,16, -0.5,1])
        plt.xticks(np.arange(1,16,1))
        plt.yticks(np.arange(-.5,1,0.25))
        sns.despine(offset=.25, trim=True);
        sns.set_style("ticks")

        #save figure
        fileoutname =  out_path + day[:4] + '_summary_Days1-' + str(len(Acc))+ '.svg'
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        fig.savefig(fileoutname)
        plt.close('all')

        #Generate group plots:
        seqLags['sid']= day[:4]
        seqLags['group']= group_dict[group]
        RT['sid'] = day[:4]
        RT['group'] = group_dict[group]
        Acc['sid'] = day[:4]
        Acc['group'] = group_dict[group]
        group_acfs[day[:4]] = seqLags
        group_rts[day[:4]] = RT
        group_acc[day[:4]] = Acc

sns.set_context(context='paper', font_scale=2.0)
sns.set_style("ticks")
fig = plt.figure(figsize=(8,12))
ax1 = fig.add_subplot(321)
ax2 = fig.add_subplot(322)

#Generate group Summaries Accuracy
plt.subplot(321)
result = pd.concat(group_acc.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'group'], value_vars = 'seqAcc')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.tsplot(time='Day', value='value',condition='group',unit='sid',data=df, estimator=np.nanmean,  err_style="ci_bars",color=dict(cue="purple", response="green"), interpolate=False, ci=68, legend=True)
ax.set(xlabel='Day', ylabel='Accuracy')
ax.set_title('Accuracy')
plt.axis([0,11,.5,1])
plt.legend(loc='lower left')
plt.xticks(np.arange(1,11,1))


#Generate Response Times
plt.subplot(322)
result = pd.concat(group_rts.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'group'], value_vars = 'zscoredRT')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.tsplot(time='Day', value='value',condition='group',unit='sid',data=df,estimator=np.nanmean, err_style="ci_bars",color=dict(cue="purple", response="green"), interpolate=False, ci=68, legend=True)
ax.set(xlabel='Day', ylabel='Response Time (z-units)')
ax.set_title('Speed')
plt.axis([0,11,0,7])
plt.xticks(np.arange(1,11,1))
plt.legend(loc='upper left')
sns.despine(offset=5, trim=True);


fig.add_subplot(312)
fig.add_subplot(313)

plt.subplot(312)
#Generate group Summaries Autocorrelation
result = pd.concat(group_acfs.values())
result = result.loc[result['group']=='response']
result['day'] = result.index
lag_names = ['lag' + str(i) for i in  range(1,16)]
df = pd.melt(result, id_vars=["day", 'sid'], value_vars = lag_names)
df['variable'] = df['variable'].map(lambda x: x.lstrip('lag').rstrip('aAbBcC'))
df = df.apply(pd.to_numeric, errors='coerce')
ax = sns.tsplot(time='variable', value='value',unit='sid', condition="day",data=df,interpolate=True, ci=68,color=sns.light_palette("green", n_colors=10))
ax.set(xlabel='Lag (Trial)', ylabel='Autocorrelation')
legend = ax.legend(loc='upper right', ncol=1, prop={'size':8}, title='Training Day')
plt.setp(legend.get_title(),fontsize='xx-small')

group_plot_fn = out_path + 'group' + group_dict[group] + '.svg'
ax.set_title('Response Group', y=.9)
plt.axis([0.5,16, -0.5,1])
plt.xticks(np.arange(1,16,1))
plt.yticks(np.arange(-.5,1,0.25))
plt.plot(np.linspace(1,15,1000), [0]*1000, 'k', linestyle='dashed')
sns.despine(offset=.25, trim=True);
sns.set_style("ticks")

plt.subplot(313)
#Generate group Summaries Autocorrelation
result = pd.concat(group_acfs.values())
result = result.loc[result['group']=='cue']
result['day'] = result.index
lag_names = ['lag' + str(i) for i in  range(1,16)]
df = pd.melt(result, id_vars=["day", 'sid'], value_vars = lag_names)
df['variable'] = df['variable'].map(lambda x: x.lstrip('lag').rstrip('aAbBcC'))
df = df.apply(pd.to_numeric, errors='coerce')
ax = sns.tsplot(time='variable', value='value',unit='sid', condition="day",data=df,interpolate=True, ci=68,color=sns.light_palette("purple", n_colors=10))
ax.set(xlabel='Lag (Trial)', ylabel='Autocorrelation')
legend = ax.legend(loc='upper right', ncol=1, prop={'size':8}, title='Training Day')
plt.setp(legend.get_title(),fontsize='xx-small')
group_plot_fn = out_path + 'group' + group_dict[group] + '.svg'
ax.set_title('Cue Group', y=.9)
plt.axis([0.5,16, -0.5,1])
plt.xticks(np.arange(1,16,1))
plt.yticks(np.arange(-.5,1,0.25))
plt.plot(np.linspace(1,15,1000), [0]*1000, 'k', linestyle='dashed')
sns.despine(offset=.25, trim=True);
sns.set_style("ticks")
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

group_plot_fn = out_path + 'group_performance.svg'
fig.savefig(fileoutname)
plt.savefig(group_plot_fn)
plt.close('all')

#Send the updated results to email
fromaddr = 'beuk.pat@gmail.com'
toaddrs  = 'beuk.pat@gmail.com'
msg = 'modmap_update'

msg = MIMEMultipart()
msg['Subject'] = 'modmap_update'
msg['From'] = 'beuk.pat@gmail.com'
msg['To'] = 'beuk.pat@gmail.com'
msg.preamble = ''

# Credentials
username = 'beuk.pat'
password = ''
for file in glob.glob(out_path + 'group*.svg'):
    fp = open(file, 'rb')
    img = MIMEImage(fp.read(), name=os.path.basename(file), _subtype="svg")
    fp.close()
    msg.attach(img)

# The actual mail send
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()
