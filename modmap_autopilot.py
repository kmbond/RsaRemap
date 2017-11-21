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

# Use os.path.expanduser if you are working on multiple machines, this way relative paths will point to right place
# Use os.path.expanduser if you are working on multiple machines, this way relative paths will point to right place
# Use os.path.expanduser if you are working on multiple machines, this way relative paths will point to right place
os.chdir(os.path.expanduser('~/Dropbox/modmap/behavior/'))
out_path = os.path.expanduser('~/Dropbox/modmap/analysis/')

# Good house keeping, this will delete old figures that you are about to update
for svg in glob.glob(os.path.expanduser('~/Dropbox/modmap/analysis/*.svg')):
    os.remove(svg)

# Initialize common dictionaries for group level analyses
# These will be converted to dataframes
# We use a dict since each subject will have a variable number of training days
group_rts = {}
group_acc= {}
group_acfs = {}
group_dict = {'r':'cue', 'c':'response'}
group_set_acfs = {}

# Loop through the two groups (r and c) in the study
for group in ['r', 'c']:

    # Generate a list of the subjects that are currently in the study
    summary_files = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*summary*' + group + '.csv'):
            summary_files.append(file)
    subs = []
    for i in range(0, len(summary_files)):
        subs.append(summary_files[i][:4])
    uniqueSubs = list(set(subs))

    # First loop through subjects and generate individual summary figures for each
    for sub in uniqueSubs:

        #initialize the dataframes
        Acc = pd.DataFrame(columns=('Day', 'randAcc', 'seqAcc'))
        RT = pd.DataFrame(columns = ('Day', 'zscoredRT', 'duration'))
        sdRT = pd.DataFrame(columns = ('Day', 'sdRTseq','sdRTrand', 'sdRatio'))
        lag_names = ['lag' + str(i) for i in  range(1,16)]
        chunkSizeSeq = pd.DataFrame(columns=('Day', 'chunkSize'))
        chunkSizeRand = pd.DataFrame(columns=('Day', 'chunkSize'))
        randLags = pd.DataFrame(columns = lag_names)
        seqLags = pd.DataFrame(columns = lag_names)
        df = pd.DataFrame()

        # Find the subjects summary data files
        sub_files = []
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file, sub+'*summary*' + '.csv'):
                sub_files.append(file)

        # populate the dataframes containing each summary statistic for each day
        for day in sub_files:
            df = pd.read_csv(day)

            this_day = int(day[day.find('session')+8:-12])
            Acc.loc[this_day] = [this_day,df['accuracy'][5], df['accuracy'][6]]
            zscoreRT = (df['rt_all'][5] - df['rt_all'][6])/df['sdRT'][5]
            RT.loc[this_day] = [this_day, zscoreRT, df['rt_all'][6]]
            sdRT.loc[this_day] = [this_day, df['sdRT'][6],df['sdRT'][5], df['sdRT'][6]/df['sdRT'][5]]
            randLags.loc[this_day] = df[lag_names].loc[6]
            seqLags.loc[this_day] = df[lag_names].loc[6]

        # Sort so that dataframes are ordered by day
        randLags = randLags.sort_index(axis=0)
        seqLags = seqLags.sort_index(axis=0)

        # Setting the context in this way will make your figure font size appear properly on a standard paper e.g for a journal submission.
        sns.set_context(context='paper', font_scale=2.0)
        # this is the setting you want
        sns.set_style("white", {'axes.linewidth':0.0000001, 'axes.edgecolor':'black'})

        #Set up one big figure for each panel and then add subplots to that figure (Panel A, B and so on)
        fig = plt.figure(figsize=(8,12))
        ax1 = fig.add_subplot(331)
        ax2 = fig.add_subplot(332)
        ax3 = fig.add_subplot(333)

        #Generate Accuracy Plots for the Sequence
        plt.subplot(331) # Specify which subplot to write to
        Acc.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'seqAcc',data=Acc, fit_reg=False, ax=ax1, scatter_kws={'s':40})
        plt.axis([1,10,.5,1])
        plt.xticks(np.arange(1,10.1,1))
        plt.ylabel('Accuracy')
        plt.xlabel('Day')
        plt.title('(a)', loc='left', y = 1.1, x = -0.35)
        plt.grid(linestyle='dotted')

        #Generate RT plots
        plt.subplot(332)
        RT.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'zscoredRT',data=RT, fit_reg=False, ax=ax2, scatter_kws={'s':40})
        plt.axis([1,10,0,6])
        plt.xticks(np.arange(1,10.1,1))
        plt.ylabel('Reaction Time (z-units)')
        plt.xlabel('Day')
        plt.title('(b)', loc='left',y = 1.1, x = -0.35)
        plt.grid(linestyle='dotted')

        # Skill plot
        plt.subplot(333) #
        Acc['errorRate'] = 1 - Acc['seqAcc']
        Acc.loc[Acc.errorRate == 0, 'errorRate'] = 0.01
        Acc['skill'] =  10*(1-Acc['errorRate'])/(Acc['errorRate']*np.log(1000*RT['duration'])**5)
        RT.sort_values(by=['Day'], ascending = [True], inplace=True)
        sns.regplot('Day', 'skill',data=Acc, fit_reg=False, ax=ax3, scatter_kws={'s':40})
        plt.axis([1,10,-300,200])
        plt.xticks(np.arange(1,10.1,1))
        plt.ylabel('Skill')
        plt.xlabel('Day')
        plt.title('(c)', loc='left',y = 1.1, x = -0.35)
        plt.grid(linestyle='dotted')

                # add subplots for panels C and D
        fig.add_subplot(312)
        fig.add_subplot(313)

        plt.subplot(312)
        blues = plt.get_cmap('Blues')
        # Autocorrelation for random trials
        for i in range(1,len(randLags)+1):
            colorBlue = blues(.05 + float(i)/(len(randLags)+1))
            plt.plot(range(1,16),randLags.loc[i], color = colorBlue, label = 'Day ' + str(i))
        box = plt.gca().get_position()
        plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.xlabel('Lag (Trials)')
        plt.ylabel('Autocorrelation')
        legend = plt.legend(loc='upper right', ncol=1, prop={'size':8}, title='Training Day')
        plt.setp(legend.get_title(),fontsize='xx-small')
        plt.title('(c)', y=0.9, loc='left', x = -0.15)
        plt.axis([1,15, -0.5,.75])
        plt.xticks(np.arange(1,16,1))
        plt.yticks(np.arange(-.5,.76,0.25))
        plt.grid(linestyle='dotted')


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
        plt.title('(d)', y=0.9, loc='left', x = -0.15)
        plt.axis([1,15, -0.5,.75])
        plt.xticks(np.arange(1,16,1))
        plt.yticks(np.arange(-.5,.76,0.25))
        plt.grid(linestyle='dotted')

        #save figure
        ind_plot_fn =  out_path + day[:4] + '_summary_Days1-' + str(len(Acc))+ '.svg'
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        fig.savefig(ind_plot_fn, rasterize=True)
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

        first_set_acfs = RT.copy()
        del first_set_acfs['zscoredRT']
        first_set_acfs['firstset']=seqLags[['lag1', 'lag2', 'lag3']].mean(axis=1)
        first_set_acfs['seq_index']=seqLags[['lag4']]
        first_set_acfs['group']  = group_dict[group]
        group_set_acfs[day[:4]] = first_set_acfs

# Now generate the up to date group summary figures
sns.set_context(context='paper', font_scale=2.0)
sns.set_style("white", {'axes.linewidth':0.0001, 'axes.edgecolor':'black'})
fig = plt.figure(figsize=(8,15))



#Generate group accuracy plots
plt.subplot(511)
result = pd.concat(group_acc.values())
result['Day'] = result.index
result.drop([])
df = pd.melt(result, id_vars=['Day', 'sid', 'group'], value_vars = 'seqAcc')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.boxplot(x='Day', y='value',hue='group',data=df,palette="PRGn")
ax.set(xlabel='Day', ylabel='Accuracy')
plt.grid(linestyle='dotted')
plt.axis([0,10,0,1])





#Generate grup response time plots
plt.subplot(512)
result = pd.concat(group_rts.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'group'], value_vars = 'zscoredRT')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.boxplot(x='Day', y='value',hue='group',data=df,palette="PRGn")
    ax.set(xlabel='Day', ylabel='RT (z-units)')
plt.legend(loc='upper left')
plt.grid(linestyle='dotted')


#Generate group skill plots
plt.subplot(513)
result = pd.concat(group_acc.values())
result['Day'] = result.index
df = pd.melt(result, id_vars=['Day', 'sid', 'group'], value_vars = 'skill')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
    ax = sns.boxplot(x="Day", y="value",hue='group', data=df,palette="PRGn");
ax.set(xlabel='Day', ylabel='skill (a.u.)')
plt.grid(linestyle='dotted')
plt.legend(loc='upper left')




#Generate group summaries autocorrelation
plt.subplot(514)
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

plt.axis([1,15, -0.25,.5])
plt.xticks(np.arange(1,16,1))
plt.yticks(np.arange(-.25,.51,0.25))
plt.grid(linestyle='dotted')

plt.subplot(515)
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

plt.axis([1,15, -0.25,.5])
plt.xticks(np.arange(1,16,1))
plt.yticks(np.arange(-.25,.51,0.25))
plt.grid(linestyle='dotted')
plt.tight_layout(pad=0.2, w_pad=0.2, h_pad=.5)
group_plot_fn = out_path + 'group_performance.svg'
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
username = 'beuk.pat'
password = ''
#Grab the group summary figures
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
