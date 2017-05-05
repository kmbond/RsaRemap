#house keeping, delete old files that are no longer needed
for svg in glob.glob('/home/beukema2/Dropbox/modChunk/copy_modmap_behavior/*Days1-*.svg'):
    os.remove(svg)

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
    group_rts = {}
    group_acc= {}
    group_dict = {'r':'Motor_Response', 'c':'Goal'}

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
        randLags = randLags.sort(axis=0)
        seqLags = seqLags.sort(axis=0)

        # Generate autocorrelation plots
        fig = plt.figure()
        blues = plt.get_cmap('Blues')
        # Random
        for i in range(1,len(randLags)+1):
            colorBlue = blues(.05 + float(i)/(len(randLags)+1))
            plt.plot(range(1,16),randLags.loc[i], color = colorBlue, label = 'session ' + str(i))

        box = plt.gca().get_position()
        plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        randPlotFN = day[:4] + '_randCorr_Days1-' + str(len(Acc)) + '.svg'
        plt.xlabel('Lag (Trials)')
        plt.ylabel('Correlation')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.axis([0,16, -0.5,1])
        plt.savefig(randPlotFN)
        plt.close("all")

        greens = plt.get_cmap('Greens')
        for i in range(1,len(randLags)+1):
            colorGreen = greens(.05 + float(i)/(len(randLags)+1))
            plt.plot(range(1,16),seqLags.loc[i], color = colorGreen, label = 'Day ' + str(i))

        box = plt.gca().get_position()
        plt.gca().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        seqPlotFN = day[:4] + '_seqCorr_Days1-' + str(len(Acc))+ '.svg'
        plt.xlabel('Lag (Trials)')
        plt.ylabel('Correlation')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.axis([0,16, -0.5,1])
        plt.savefig(seqPlotFN)
        plt.close("all")

        #Generate Accuracy Plots for the Sequence
        plt.figure(figsize=(8, 6))
        Acc.sort(['Day'], ascending =[True], inplace=True)
        accPlot_fn =  day[:4] + '_Acc_Days1-' + str(len(Acc))+ '.svg'
        colorBlue = blues(.05 + float(i)/(len(randLags)+1))
        plt.plot(range(1,16),randLags.loc[i], color = colorBlue, label = 'seq')
        sns.lmplot('Day', 'seqAcc',data=Acc, fit_reg=False)
        plt.axis([0,len(Acc)+1,.5,1])
        plt.ylabel('% Correct')
        plt.xlabel('Day')
        plt.savefig(accPlot_fn)
        plt.close("all")

        #Generate RT plots
        plt.figure(figsize=(8, 6))
        RT.sort(['Day'], ascending =[True], inplace=True)
        RTPlot_fn =  day[:4] + '_RT_Days1-' + str(len(Acc))+ '.svg'
        sns.lmplot('Day', 'zscoredRT',data=RT, fit_reg=False)
        plt.axis([0,len(RT)+1,-1,10])
        plt.ylabel('Reaction Times (z-scores)')
        plt.xlabel('Day')
        sdTitle = 'Subject:' + day[:4]
        plt.title(sdTitle)
        plt.savefig(RTPlot_fn)
        plt.close("all")

        #Generate group plots:
        seqLags['sid']= day[:4]
        RT['sid'] = day[:4]
        Acc['sid'] = day[:4]
        group_acfs[day[:4]] = seqLags
        group_rts[day[:4]] = RT
        group_acc[day[:4]] = Acc

    #Generate Group Summaries Autocorrelation
    result = pd.concat(group_acfs.values())
    result['day'] = result.index
    lag_names = ['lag' + str(i) for i in  range(1,16)]
    df = pd.melt(result, id_vars=["day", 'sid'], value_vars = lag_names)
    df['variable'] = df['variable'].map(lambda x: x.lstrip('lag').rstrip('aAbBcC'))
    fig = plt.figure(figsize=(9,6))
    df = df.convert_objects(convert_numeric=True)
    ax = sns.tsplot(time='variable', value='value',unit='sid', condition="day",data=df,interpolate=True, ci=68,color=sns.cubehelix_palette(12,reverse=True))
    ax.set(xlabel='Lag (Trial)', ylabel='Autocorrelation')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    group_plot_fn = 'group' + group_dict[group] + '.svg'
    ax.set_title(group_dict[group] + ' group' )
    plt.savefig(group_plot_fn)
    plt.close("all")

    #Generate Group Summaries Accuracy
    result = pd.concat(group_acc.values())
    result['Day'] = result.index
    df = pd.melt(result, id_vars=["Day", 'sid'], value_vars = 'seqAcc')
    ax = sns.tsplot(time='Day', value='value',unit='sid',data=df,interpolate=True, ci=68,color=sns.cubehelix_palette(12,reverse=True))
    ax.set(xlabel='Day', ylabel='Accuracy')
    group_plot_fn = 'group' + group_dict[group] + 'accuracy.svg'
    ax.set_title(group_dict[group] + ' group ' + ' Accuracy')
    plt.axis([0,len(Acc)+1,.5,1])
    plt.savefig(group_plot_fn)
    plt.close("all")

    #Generate Response Times
    result = pd.concat(group_rts.values())
    result['Day'] = result.index
    df = pd.melt(result, id_vars=["Day", 'sid'], value_vars = 'zscoredRT')
    ax = sns.tsplot(time='Day', value='value',unit='sid',data=df,interpolate=True, ci=68,color=sns.cubehelix_palette(12,reverse=True))
    ax.set(xlabel='Day', ylabel='Response Time (z-units)')
    group_plot_fn = 'group' + group_dict[group] + 'response_times.svg'
    print 'group' + group_dict[group] + 'response_times.svg'
    ax.set_title(group_dict[group] + ' group ' + ' Response Times')
    plt.axis([0,len(RT)+1,0,7])
    plt.savefig(group_plot_fn)
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

# Credentials (if needed)
username = 'beuk.pat'
password = 'theBull!1'
for file in glob.glob('group*.svg'):
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
server.quit()modm
