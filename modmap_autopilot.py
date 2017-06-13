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

allResp_files = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*allResp*.csv'):
        allResp_files.append(file)

for file_name in allResp_files:
    #rebuild summary statistics file if necessary
    lag_names = ['lag' + str(i) for i in  range(1,16)]
    data_lags = pd.DataFrame(columns = lag_names)
    sum_names = ['block', 'accuracy', 'rt_all', 'rt_cor', 'sdAcc', 'sdRT', 'chunkSize']
    data_summary = pd.DataFrame(columns = (sum_names))
    data_out = pd.read_csv(file_name)
    skip_index = 0
    max_lags = 15

    for i in np.unique(data_out[['block']]):
        #make a plot of the response times vs trial and plot by type save with subject's id.
        data_out['trial'] = np.array(range(1,len(data_out)+1))
        sns.set_context("paper")
        #if i ==7:
        #    sns.lmplot('trial', 'rt', hue = 'type', data=data_out, fit_reg=False)
        #    plt.savefig(plot_fn)
        block_df = data_out.loc[data_out['block']==i]
        mean_acc = block_df[['response']].mean()
        rt_all = block_df[['rt']].mean()
        block_df_cor = block_df.loc[block_df['response']==1]
        rt_cor = block_df_cor[['rt']].mean()
        std_acc = block_df[['response']].std()
        std_rt =  block_df_cor[['rt']].std()

        #del skip trials
        good_trials = block_df.drop(block_df.index[:skip_index])

        good_trials = good_trials[['rt']].replace(np.nan,np.nan)
        y = np.array(good_trials)
        x = np.linspace(1,y.size,y.size)
        x = np.vstack([x,np.ones(len(x))]).T
        result = sm.OLS(y, x, missing='drop').fit()
        R = result.resid
        idx = np.isfinite(y)
        y = y[idx]
        x = np.linspace(1,y.size,y.size)
        z = np.polyfit(x,y, 5)
        p = np.poly1d(z)
        R = y-p(x)

        acfResults = statsmodels.tsa.stattools.acf(R,unbiased=True, nlags=15, fft=True, alpha=0.05, missing='drop')
        lags = acfResults[0]
        lags = lags[1:] #don't care about first lag always 1
        data_lags.loc[i] = lags

        x = range(1,16)
        y = acfResults[0]
        y = y[1:].T
        error = acfResults[1]
        error = error[1:]
        up_conf = error[:,1]
        low_conf = error[:,0]
        #Put into summary data frame. As Column,
        chunkSize = np.argmax(low_conf<0)
        data_summary.loc[i] = [i, mean_acc.response, rt_all.rt, rt_cor.rt, std_acc.response, std_rt.rt, chunkSize]

    #Save the file locally and in dropbox.
    out_sum_fn = file_name.replace('allResp', 'summary')
    data_summary = pd.merge(data_summary, data_lags, left_on = 'block', right_on='lag1',left_index = True,right_index = True, how= 'outer')
    data_summary.to_csv(out_sum_fn, index=False)


#house keeping, delete old files that are no longer needed
for svg in glob.glob('/home/beukema2/Dropbox/modmap/analysis/*.svg'):
    os.remove(svg)
#initialize common group dict of dataframes
group_rts = {}
group_acc= {}
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
    group_acfs = {}

    group_dict = {'r':'cue', 'c':'response'}

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

        #Generate RT plots
        plt.subplot(322)
        RT.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'zscoredRT',data=RT, fit_reg=False, ax=ax2, scatter_kws={'s':40})
        plt.axis([0,11,0,8])
        plt.xticks(np.arange(1,11,1))
        plt.ylabel('Reaction Time')
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
        plt.ylabel('Correlation (Rand)')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
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
        plt.ylabel('Correlation (Seq)' )
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.axis([0.5,16, -0.5,1])
        plt.xticks(np.arange(1,16,1))
        plt.yticks(np.arange(-.5,1,0.25))
        plt.axis([0.5,16, -0.5,1])
        sns.despine(offset=.25, trim=True);
        sns.set_style("ticks")



        #save figure
        fileoutname =  out_path + day[:4] + '_summary_Days1-' + str(len(Acc))+ '.svg'
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        fig.savefig(fileoutname)
        plt.close('all')

        #Generate group plots:
        seqLags['sid']= day[:4]
        RT['sid'] = day[:4]
        RT['Group'] = group_dict[group]
        Acc['sid'] = day[:4]
        Acc['Group'] = group_dict[group]
        group_acfs[day[:4]] = seqLags
        group_rts[day[:4]] = RT
        group_acc[day[:4]] = Acc

    #Generate Group Summaries Autocorrelation
    sns.set_context(context='paper', font_scale=2.0)
    plt.figure(figsize=(8, 6))
    result = pd.concat(group_acfs.values())
    result['day'] = result.index
    lag_names = ['lag' + str(i) for i in  range(1,16)]
    df = pd.melt(result, id_vars=["day", 'sid'], value_vars = lag_names)
    df['variable'] = df['variable'].map(lambda x: x.lstrip('lag').rstrip('aAbBcC'))
    fig = plt.figure(figsize=(9,6))
    df = df.apply(pd.to_numeric, errors='coerce')
    ax = sns.tsplot(time='variable', value='value',unit='sid', condition="day",data=df,interpolate=True, ci=68,color=sns.cubehelix_palette(12,reverse=True))
    ax.set(xlabel='Lag (Trial)', ylabel='Autocorrelation')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    group_plot_fn = out_path + 'group' + group_dict[group] + '.svg'
    ax.set_title(group_dict[group] + ' group' )
    plt.axis([0,16,-.2,.6])
    sns.despine(offset=10, trim=True);
    plt.savefig(group_plot_fn,bbox_inches='tight')
    plt.close("all")

#Generate Group Summaries Accuracy
sns.set_context(context='paper', font_scale=2.0)
plt.figure(figsize=(8, 6))
result = pd.concat(group_acc.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'Group'], value_vars = 'seqAcc')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.tsplot(time='Day', value='value',condition='Group',unit='sid',data=df, estimator=np.nanmean,  err_style="ci_bars",color="Set2", interpolate=False, ci=68)
ax.set(xlabel='Day', ylabel='Accuracy')
group_plot_fn = out_path + 'mean_accuracy.svg'
ax.set_title('Accuracy')
plt.axis([0,11,.5,1])
plt.xticks(np.arange(1,11,1))
sns.despine(offset=5, trim=True);
plt.savefig(group_plot_fn,bbox_inches='tight')
plt.close("all")

#Generate Response Times
sns.set_context(context='paper', font_scale=2.0)
plt.figure(figsize=(8, 6))
result = pd.concat(group_rts.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'Group'], value_vars = 'zscoredRT')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.tsplot(time='Day', value='value',condition='Group',unit='sid',data=df,estimator=np.nanmean, err_style="ci_bars",color="Set2", interpolate=False, ci=68)
ax.set(xlabel='Day', ylabel='Response Time (z-units)')
group_plot_fn = out_path + 'mean_response_times.svg'
ax.set_title('Response Times')
plt.axis([0,11,0,7])
plt.xticks(np.arange(1,11,1))
sns.despine(offset=5, trim=True);
plt.savefig(group_plot_fn,bbox_inches='tight')
plt.close("all")

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
