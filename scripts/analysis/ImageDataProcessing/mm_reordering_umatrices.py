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


def cleanUp(subject):
    for file in glob.glob('/data/modMap/subjects/%s/%s/rsaRemap*_responses.csv' %(subject,day)):
        os.remove(file)
    for file in glob.glob('/data/modMap/subjects/%s/%s/*practiceOnsets*.csv' %(subject,day)):
        os.remove(file)

def copyOnsets(subject):
    for file in glob.glob('/home/beukema2/Dropbox/modmap/MRI/%s/rsaRemap_%s_Day%s_Session*_responses.csv' %(subject, subject, which_day[day])):
        shutil.copy(file, '/data/modMap/subjects/%s/%s' %(subject, day))
    for file in glob.glob('/home/beukema2/Dropbox/modmap/MRI/%s/%s_practiceOnsets_Day%s_session*.csv' %(subject, subject, which_day[day])):
        shutil.copy(file, '/data/modMap/subjects/%s/%s' %(subject, day))

def genOrderings(subjectDir):
    summary_files = []
    mapping_files = []
    for file in os.listdir(subjectDir):
        if fnmatch.fnmatch(file, '*rsaRemap*responses*.csv'):
            summary_files.append(os.path.realpath(os.path.join(subjectDir,file)))
        if fnmatch.fnmatch(file, '*_practiceOnsets_Day*.csv'):
            mapping_files.append(os.path.realpath(os.path.join(subjectDir,file)))
    cue_reordering = pd.DataFrame(columns = ['1','2', '3', '4', '5', '6', '7', '8'])
    finger_reordering = pd.DataFrame(columns = ['1','2', '3', '4', '5', '6', '7', '8'])

    for file in summary_files:
        (prefix, sep, suffix) = file.rpartition('.')
        base=os.path.basename(file)

        df = pd.read_csv(file)
        df['keysPressed'].replace(to_replace='[^0-9]', value='', inplace=True, regex=True)
        df['correctResp'].replace(to_replace='[^0-9]', value='', inplace=True, regex=True)
        df['onsetTime'] = df['onsetTime'].apply(int)
        df['onsetTime'] = df['onsetTime']/2 # to convert to TRs for spm
        df['chunk'] = df.apply(lambda x : x['chunkID'] if (x['Error'] == 0) else 'NaN', axis=1)
        df['fingers'] = df.apply(lambda x : x['correctResp'] if (x['Error'] == 0) else 'NaN', axis=1)
        df['firstfinger'] = [item[0] for item in df['fingers']]
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

        #Get the cue reordering for this run
        session = base[26:-14]
        print session

        mapping_df = df.drop(['onsetTime', 'correctResp','keysPressed', 'chunkID', 'responseTimes', 'Error', 'fingers'], axis=1)
        mapping_df = mapping_df.drop_duplicates()
        mapping_df = mapping_df[mapping_df['chunk'].str.contains("chunk_C")].reset_index()
        chunk_to_row = {'chunk_C1': 5, 'chunk_C2': 6,'chunk_C3': 7,'chunk_C4': 8}
        mapping_df['row_num'] = mapping_df['chunk'].map(chunk_to_row)
        mapping_df.sort_values(by=['row_num'],inplace=True)
        #mapping_df['firstfinger'] = mapping_df['firstfinger'] + 4
        mapping_df['firstfinger'] = pd.to_numeric(mapping_df.firstfinger)
        mapping_df['firstfinger'] = mapping_df['firstfinger'] + 3
        cue_reordering.loc[:,session] = mapping_df['firstfinger'].values

        #Get the finger reordering for this run
        temp_file = mapping_files[0]
        mapping_file =  temp_file[0:-5] + base[26] + '.csv'
        df_firstcue = pd.read_csv(mapping_file)
        di = {'image_folder/stim_2.png': "A", 'image_folder/stim_3.png': "B",'image_folder/stim_4.png': "C",'image_folder/stim_5.png': "D"}
        df_firstcue = df_firstcue.replace({"img_id": di})
        df_firstcue.cor_ans = df_firstcue.cor_ans.astype(str)
        my_dict = dict(zip(df_firstcue.cor_ans,df_firstcue.img_id))
        df = df.replace({"firstfinger":my_dict})
        mapping_df = df.drop(['onsetTime', 'correctResp','keysPressed', 'chunkID', 'responseTimes', 'Error', 'fingers'], axis=1)
        mapping_df = mapping_df.drop_duplicates()
        mapping_df = mapping_df[mapping_df['chunk'].str.contains("chunk_R")].reset_index()
        chunk_to_row = {'chunk_R1': 1, 'chunk_R2': 2,'chunk_R3': 3,'chunk_R4': 4}
        cue_to_row = {'A': 1, 'B': 2,'C': 3,'D': 4}
        mapping_df['row_num'] = mapping_df['chunk'].map(chunk_to_row)
        mapping_df['cue_to_row'] = mapping_df['firstfinger'].map(cue_to_row)
        mapping_df.sort_values(by=['row_num'],inplace=True)
        finger_reordering.loc[:,session] = mapping_df['cue_to_row'].values
        print finger_reordering
    finger_fn = subjectDir + '/finger_reordering_'+day+'.csv'
    cue_fn = subjectDir + '/cue_reordering_'+day+'.csv'
    finger_reordering.to_csv(finger_fn,sep='\t', index=False, header=False)
    cue_reordering.to_csv(cue_fn,sep='\t', index=False, header=False)



subject = sys.argv[1]
day = sys.argv[2]
which_day = {'Pre':'1', 'Post':'2'}
copyOnsets(subject)

for root, dirs, files in os.walk('/data/modMap/subjects/%s/%s' % (subject,day)):
    genOrderings(root)

#Housekeeping
cleanUp(subject)
