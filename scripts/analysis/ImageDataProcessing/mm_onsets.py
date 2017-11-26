#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import scipy.io
import pandas as pd
import fnmatch
import os
import matplotlib.pyplot as plt
import glob
import re
import pdb
import sys
import shutil
#find onset files matching .csv and return matlab cell array
#run from dir containing onsets.

def cleanUp(subject):
    for file in glob.glob('/data/modMap/subjects/%s/%s/rsaRemap*_responses.csv' %(subject,day)):
        os.remove(file)

def copyOnsets(subject):
    for file in glob.glob('/home/beukema2/Dropbox/modmap/MRI/%s/rsaRemap_%s_Day%s_Session*_responses.csv' %(subject, subject, which_day[day])):
        print which_day[day]
        shutil.copy(file, '/data/modMap/subjects/%s/%s' %(subject, day))

def genOnsets(subjectDir):
    summary_files = []
    for file in os.listdir(subjectDir):
        if fnmatch.fnmatch(file, '*rsaRemap*responses*.csv'):
            summary_files.append(os.path.realpath(os.path.join(subjectDir,file)))

    for file in summary_files:

        df = pd.read_csv(file)
        df['keysPressed'].replace(to_replace='[^0-9]', value='', inplace=True, regex=True)
        df['correctResp'].replace(to_replace='[^0-9]', value='', inplace=True, regex=True)
        df['onsetTime'] = df['onsetTime'].apply(int)
        df['onsetTime'] = df['onsetTime']/2 # to convert to TRs for spm
        df['chunk'] = df.apply(lambda x : x['chunkID'] if (x['Error'] == 0) else 'NaN', axis=1)

        #Generate the onsets for each different chunk
        new_onsets = np.empty(df.shape[1]+1, dtype=object)
        new_onsets[0] = np.array(df[df['chunk'] == 'chunk_R1']['onsetTime'][:,np.newaxis])
        new_onsets[1] = np.array(df[df['chunk'] == 'chunk_R2']['onsetTime'][:,np.newaxis])
        new_onsets[2] = np.array(df[df['chunk'] == 'chunk_R3']['onsetTime'][:,np.newaxis])
        new_onsets[3] = np.array(df[df['chunk'] == 'chunk_R4']['onsetTime'][:,np.newaxis])
        new_onsets[4] = np.array(df[df['chunk'] == 'chunk_C1']['onsetTime'][:,np.newaxis])
        new_onsets[5] = np.array(df[df['chunk'] == 'chunk_C2']['onsetTime'][:,np.newaxis])
        new_onsets[6] = np.array(df[df['chunk'] == 'chunk_C3']['onsetTime'][:,np.newaxis])
        new_onsets[7] = np.array(df[df['chunk'] == 'chunk_C4']['onsetTime'][:,np.newaxis])
        data={}
        data['ons'] = new_onsets
        (prefix, sep, suffix) = file.rpartition('.')
        base=os.path.basename(file)
        fn = subjectDir + '/RER_Run'+ base[26]+ '/' + base[14:-4] + '.mat'
        fn = fn.replace('responses', 'sets')
        scipy.io.savemat(fn, data)

        #Generate the onsets for the cue_vs_response beta coefficients.
        # new_onsets = np.empty(2, dtype=object)
        # new_onsets[0] = np.array(df[df['chunkID'].str.contains('chunk_R')]['onsetTime'][:,np.newaxis])
        # new_onsets[1] =  np.array(df[df['chunkID'].str.contains('chunk_C')]['onsetTime'][:,np.newaxis])
        # data={}
        # data['ons'] = new_onsets
        # (prefix, sep, suffix) = file.rpartition('.')
        # base=os.path.basename(file)
        # fn = fn.replace('responses', 'cue_vs_responses')
        # scipy.io.savemat(fn, data)
# for subject in  ['0550', '0566', '0738', '0739', '0740', '0741' ,'0742', '0743', '0744', '0745', '0746', '0747' ,'0748' ,'0749', '0750' ,'0751', '0752' ,'0753' ,'0754', '0755']:
#     for day in ['Pre', 'Post']:
subject = sys.argv[1]
day = sys.argv[2]
which_day = {'Pre':'1', 'Post':'2'}
copyOnsets(subject)
for root, dirs, files in os.walk('/data/modMap/subjects/%s/%s' % (subject,day)):
    genOnsets(root)
#Housekeeping
cleanUp(subject)
