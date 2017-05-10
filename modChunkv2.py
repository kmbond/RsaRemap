#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import division
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import *

import sys
import pandas as pd
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import itertools

import os
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels
import fnmatch
import time

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'behRemap'
expInfo = {u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['group (c or r)'] = 'r'

#Count how many days this subject has completed:
current_session_count = []
for file in os.listdir(_thisDir+os.sep + 'data'):
    if fnmatch.fnmatch(file, '*' + expInfo['participant'] + '*summary*.csv'):
        current_session_count.append(file)
expInfo['session'] = len(current_session_count) + 1
session = int(expInfo['session'])
if session==11:
    sys.exit("You are done!")

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s_group_%s' %(expInfo['participant'], expName, expInfo['date'], expInfo['group (c or r)'])

# Output summary data and analyzed files
out_sum_fn =  _thisDir + os.sep +'data/%s_summary_%s_%s_session_%s_group_%s.csv' %(expInfo['participant'], expName, expInfo['date'], expInfo['session'],  expInfo['group (c or r)'])
out_all_fn =  _thisDir + os.sep +'data/%s_allResp_%s_%s_session_%s_group_%s.csv' %(expInfo['participant'], expName,  expInfo['date'], expInfo['session'],   expInfo['group (c or r)'])
data_out = pd.DataFrame(columns=('block','response','rt', 'type', 'keyPressed', 'correctKey'))

#Learning mapping data files.
practice_out_fn =  _thisDir + os.sep +'data/%s_practice_%s_%s_session_%s_group_%s.csv' %(expInfo['participant'], expName,  expInfo['date'], expInfo['session'],   expInfo['group (c or r)'])
practice_data_out = pd.DataFrame(columns=('nTrials','accuracy', 'time'))

#### Generate Stimuli ####
keys = [2, 3, 4, 5]
img_filenames = ['image_folder/stim_2.png', 'image_folder/stim_3.png', 'image_folder/stim_4.png', 'image_folder/stim_5.png']
key_name = ['j', 'k', 'l', 'semicolon']
img_dicts = [dict(zip(kperm, img_filenames)) for kperm in itertools.permutations(keys, len(img_filenames))]
key_dicts =  [dict(zip(kperm, key_name)) for kperm in itertools.permutations(keys, len(key_name))]
map_perm = [13,4,8,23,16,7,21,13,1,23,8,16,21,7,4]

# To keep the movements same change img_dict
if  expInfo['group (c or r)'] == 'c':
    img_dict = img_dicts[map_perm[session-1]]
    key_dict = key_dicts[0]
# to keep goals same change key_dict
if  expInfo['group (c or r)'] == 'r':
    img_dict = img_dicts[0]
    key_dict = key_dicts[map_perm[session-1]]

#64 chunks total
#chunkSize = 4
#16 repititions of each chunk
#no pause after first cue during first 7 blocks
key_map = {2:'x', 3:'x', 4:'x', 5:'x'}

this_practice_dict = {key: img_dict[key] for key in key_map.keys()}
#this_practice_dict = {key_dict[key]: img_dict[key] for key in key_map.keys()}
df_practice = {'cor_ans':this_practice_dict.keys(),'img_id': this_practice_dict.values()}
df_practice = pd.DataFrame(data=df_practice)
df_practice = df_practice[['img_id', 'cor_ans']]
df_practice = df_practice.replace({'cor_ans':key_dict})
#This chunk of code reassigns the values so that
list = [df_practice.loc[df_practice['cor_ans']=='j','img_id'].values, df_practice.loc[df_practice['cor_ans']=='k', 'img_id'].values, df_practice.loc[df_practice['cor_ans']=='l', 'img_id'].values,  df_practice.loc[df_practice['cor_ans']=='semicolon', 'img_id'].values]
concatlist = [item for sublist in list for item in sublist]
df_practice['order_img_id'] =  concatlist
df_practice['order_cor_ans'] = ['j', 'k', 'l', 'semicolon']
df_practice.drop('img_id', axis=1)
df_practice = df_practice[['order_img_id', 'order_cor_ans']].copy()
df_practice.columns = ['img_id', 'cor_ans']

practiceOnsets_fn =  _thisDir + os.sep + 'data/%s_practiceOnsets_session_%s.csv' %(expInfo['participant'], expInfo['session'])
df_practice.to_csv(practiceOnsets_fn, index=False)

n_trials = 16*16 # number of trials within a block should be 256
dfStims = pd.DataFrame()
block_ids = [1, 1, 2, 2, 2, 1, 2]#1 is random #2 is sequence
chunks = [[2,3,5,2],[4,5,3,5],[3,2,4,3],[5,4,2,4]]
#Generate Pseudo-Random Stimuli Ordering
def genRandom(n_trials):
    random_stims = []
    random_img_ids = []
    random_ans = []
    for x in range(0,n_trials):
        if len(random_stims) == 0:
            random_stims.append(randint(2,6))
        elif len(random_stims) > 0:
            val = randint(2,6)
            while val == random_stims[x-1]:
                val = randint(2,6)
            random_stims.append(val)
        random_img_ids.append(img_dict[random_stims[x]])
        random_ans.append(key_dict[random_stims[x]])
    random_img_ids = np.asarray(random_img_ids)
    random_ans= np.asarray(random_ans)
    return (random_img_ids, random_ans)

#Generate Sequence Ordering
def genSequence(n_trials):
    #Generate Sequence Stimuli Ordering.
    sequence_stims = [2,3,5,2,4,5,3,5,3,2,4,3,5,4,2,4]
    #rota_ind = randint(1,len(sequence_stims)-1) #don't want to rotate
    #sequence_stims = sequence_stims[rota_ind:]  + sequence_stims[:rota_ind] #don't want to rotate
    sequence_img_ids = []
    sequence_ans = []
    sequence_stims= np.tile(sequence_stims,16)
    for x in range(0,n_trials):
        sequence_img_ids.append(img_dict[sequence_stims[x]])
        sequence_ans.append(key_dict[sequence_stims[x]])
    return (sequence_img_ids, sequence_ans)

for type in range(0,len(block_ids)):
    if block_ids[type] == 1:
        img_ids, ran_ans = genRandom(n_trials)
        dfStims['block_'+str(type+1)+'_img'] = img_ids
        dfStims['block_'+str(type+1)+'_ans'] = ran_ans
    elif block_ids[type] == 2:
        img_ids, seq_ans = genSequence(n_trials)
        dfStims['block_'+str(type+1)+'_img'] = img_ids
        dfStims['block_'+str(type+1)+'_ans'] = seq_ans

dfStims.to_csv('behavior_stimuli.csv', index= False)


behavior_blocks = pd.DataFrame()
behavior_blocks['Block_id'] = ['block_1_img','block_2_img','block_3_img','block_4_img' ,'block_5_img','block_6_img' ,'block_7_img' ]
behavior_blocks['Block_ans'] = ['block_1_ans','block_2_ans','block_3_ans','block_4_ans','block_5_ans','block_6_ans','block_7_ans' ]
behavior_blocks.to_csv('behavior_blocks.csv', index= False)


# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=[400,400], fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True
    )

# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess


# Initialize components for Routine "Instructions"
InstructionsClock = core.Clock()
instrText = visual.TextStim(win=win, ori=0, name='instrText',
    text=u'In this experiment, you will see a series of images displayed on the screen. Each image corresponds to a unique finger movement (index, middle, ring, pinky). \n Position your index finger on \'j\', your middle finger on \'k\',your ring on \'l\' and your pinky on \';\'. \n Before starting, you will learn the mapping of each image to key press. Press any key to continue.',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "practice"
practiceClock = core.Clock()

image = visual.ImageStim(win=win, name='image', units='pix',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[200,200],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Feedback
practiceFeedback = visual.TextStim(win=win, ori=0, name='text_4',
    text=u'Press the space bar to continue. \n',    font=u'Arial',
    pos=[0, -.6], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

Wrong_1 = visual.Circle(win=win, units = 'pix', radius = 100,lineColor='red', fillColor = 'red')

# Initialize components for Routine "Begin_Blocks"
Begin_BlocksClock = core.Clock()
text_3 = visual.TextStim(win=win, ori=0, name='text_3',
    text=u'End of practice rounds. Press any key to continue. ',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "Block"
BlockClock = core.Clock()
image_2 = visual.ImageStim(win=win, name='image_2',units='pix',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[200,200],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Initialize components for Routine "Feedback"
FeedbackClock = core.Clock()
#initialize n_corr and mean_Rt

text_2 = visual.TextStim(win=win, ori=0, name='text_2',
    text='',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "End_Experiment"
End_ExperimentClock = core.Clock()
text = visual.TextStim(win=win, ori=0, name='text',
    text=u'Experiment is completed. Thank you for your participation.\n',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

practice_with_help = visual.TextStim(win=win, ori=0, name='practice_with_help',
    text=u'Practice trails are about to begin. Ensure that you can comfortably press each button.',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)


practice_without_help = visual.TextStim(win=win, ori=0, name='practice_without_help',
        text=u'Now you will practice the same key presses, but there will not be any text telling you which key to press. The only feedback will be a red circle if you incorrectly press a finger. Once you reach at least 90 % accuarcy, the experiment will automatically advance to the next phase. ',    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

pause_text = 'Practice is completed. Press any key to continue'
pause_after_block = visual.TextStim(win=win, ori=0, name='text',
    text=pause_text,    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)
# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

#------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
instructions_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
instructions_response.status = NOT_STARTED
# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(instrText)
InstructionsComponents.append(instructions_response)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText* updates
    if t >= 0.0 and instrText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText.tStart = t  # underestimates by a little under one frame
        instrText.frameNStart = frameN  # exact frame index
        instrText.setAutoDraw(True)

    # *instructions_response* updates
    if t >= 0.0 and instructions_response.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions_response.tStart = t  # underestimates by a little under one frame
        instructions_response.frameNStart = frameN  # exact frame index
        instructions_response.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if instructions_response.status == STARTED:
        theseKeys = event.getKeys()

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(practice_with_help)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Instructions"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practice_with_help* updates
    if t >= 0.0 and practice_with_help.status == NOT_STARTED:
        # keep track of start time/frame for later
        practice_with_help.tStart = t  # underestimates by a little under one frame
        practice_with_help.frameNStart = frameN  # exact frame index
        practice_with_help.setAutoDraw(True)
    if practice_with_help.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
        practice_with_help.setAutoDraw(False)
        continueRoutine = False
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#Clear events of type keyboard so that next block doesn't immediately advance.
event.clearEvents(eventType='keyboard')

#-------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# set up handler to look after randomisation of conditions etc
practice_loop = data.TrialHandler(nReps=5, method='sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(practiceOnsets_fn),
    seed=None, name='practice_loop')

thisExp.addLoop(practice_loop)  # add the loop to the experiment
thisPractice_loop = practice_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisPractice_loop.rgb)
if thisPractice_loop != None:
    for paramName in thisPractice_loop.keys():
        exec(paramName + '= thisPractice_loop.' + paramName)
mapping = {'j': 'Index ','k': 'Middle ', 'l': 'Ring ', 'semicolon':'Little '}
for thisPractice_loop in practice_loop:

    # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
    if thisPractice_loop != None:
        for paramName in thisPractice_loop.keys():
            exec(paramName + '= thisPractice_loop.' + paramName)

    #------Prepare to start Routine "practice"-------
    t = 0
    practiceClock.reset()
    routineTimer.add(100)  # clock

    frameN = -1

    # update component parameters for each repeat
    image.setImage(img_id)
    Practice_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Practice_response.status = NOT_STARTED
    # keep track of which components have finished
    practiceComponents = []
    practiceComponents.append(image)
    practiceComponents.append(Practice_response)
    practiceComponents.append(Wrong_1)
    eplicit_instruction = mapping[cor_ans]
    practiceFeedback = visual.TextStim(win=win, ori=0, name='text_4',
            text=eplicit_instruction,    font=u'Arial',
            pos=[0, -.6], height=0.1, wrapWidth=None,
            color=u'white', colorSpace='rgb', opacity=1,
            depth=0.0)
    practiceComponents.append(practiceFeedback)

    for thisComponent in practiceComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "practice"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:

        practiceFeedback.setAutoDraw(True)

        # get current time
        t = practiceClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *image* updates
        if t >= .25 and image.status == NOT_STARTED:
            # keep track of start time/frame for later
            image.tStart = t  # underestimates by a little under one frame
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)

        # *Practice_response* updates
        if t >= .25 and Practice_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            Practice_response.tStart = t  # underestimates by a little under one frame
            Practice_response.frameNStart = frameN  # exact frame index
            Practice_response.status = STARTED
            # keyboard checking is just starting
            Practice_response.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if Practice_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['2', '3', '4', '5','j', 'k', 'l', 'semicolon'])


            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed

                if Practice_response.keys == []:
                    Practice_response.keys = theseKeys[0]  # just the last key pressed


                    Practice_response.rt = Practice_response.clock.getTime()
                    # was this 'correct'?
                    if (Practice_response.keys == str(cor_ans)) or (Practice_response.keys == cor_ans):
                        Practice_response.corr = 1
                        continueRoutine = False
                    else:
                        Practice_response.corr = 0
                        Wrong_1.setAutoDraw(True)
                        win.flip()
                        core.wait(.2)
                        continueRoutine = False

                    practiceFeedback.setAutoDraw(True)

        # a response ends the routine
        if practiceFeedback.status == STARTED and event.getKeys(keyList=['space']):
            continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "practice"-------
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Store nothing

        # a response ends the routine
        if practiceFeedback.status == STARTED and event.getKeys(keyList=['space']):
            continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "practice"-------
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Store nothing

#------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(practice_without_help)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Practice without help"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practice_with_help* updates
    if t >= 0.0 and practice_without_help.status == NOT_STARTED:
        # keep track of start time/frame for later
        practice_without_help.tStart = t  # underestimates by a little under one frame
        practice_without_help.frameNStart = frameN  # exact frame index
        practice_without_help.setAutoDraw(True)
    if practice_without_help.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
        practice_without_help.setAutoDraw(False)
        continueRoutine = False
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#Clear events of type keyboard so that next block doesn't immediately advance.
event.clearEvents(eventType='keyboard')

#-------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# set up handler to look after randomisation of conditions etc
practice_loop = data.TrialHandler(nReps=1000, method='random',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(practiceOnsets_fn),
    seed=None, name='practice_loop')

thisExp.addLoop(practice_loop)  # add the loop to the experiment
thisPractice_loop = practice_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisPractice_loop.rgb)
if thisPractice_loop != None:
    for paramName in thisPractice_loop.keys():
        exec(paramName + '= thisPractice_loop.' + paramName)
mapping = {2: 'Index Finger', 3: 'Middle finger', 4: 'Ring finger', 5:'Little finger'}
running_accuracy = []
n_practice_trials = 0
start_time = time.time()
for thisPractice_loop in practice_loop:


    #%Check if threshold performance has been met.
    n_practice_trials +=1
    current_acc = (sum(running_accuracy[-20:])/20.0)
    if n_practice_trials > 80 and current_acc > .90:
        end_time = time.time() - start_time
        practice_data_out.loc[len(data_out)+1]=[n_practice_trials,current_acc, end_time]
        practice_data_out.to_csv(practice_out_fn, index=False)
        break

    # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
    if thisPractice_loop != None:
        for paramName in thisPractice_loop.keys():
            exec(paramName + '= thisPractice_loop.' + paramName)

    #------Prepare to start Routine "practice"-------
    t = 0

    routineTimer.add(100)  # clock

    frameN = -1

    # update component parameters for each repeat
    image.setImage(img_id)
    Practice_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Practice_response.status = NOT_STARTED
    # keep track of which components have finished
    practiceComponents = []
    practiceComponents.append(image)
    practiceComponents.append(Practice_response)
    practiceComponents.append(Wrong_1)
    #eplicit_instruction = mapping[cor_ans]
    #practiceFeedback = visual.TextStim(win=win, ori=0, name='text_4',text=eplicit_instruction,font=u'Arial', pos=[0, -.6], height=0.1, wrapWidth=None, color=u'white', colorSpace='rgb', opacity=1,depth=0.0)
    #practiceComponents.append(practiceFeedback)
    practiceClock.reset()
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "practice"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:

        #practiceFeedback.setAutoDraw(True)

        # get current time
        t = practiceClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if t >= 1.25:
            # keep track of start time/frame for later
            Practice_response.corr = 0
            running_accuracy.append(0)
            Wrong_1.setAutoDraw(True)
            win.flip()
            core.wait(.2)
            continueRoutine = False
        # *image* updates
        if t >= .25 and image.status == NOT_STARTED:
            # keep track of start time/frame for later
            image.tStart = t  # underestimates by a little under one frame
            image.frameNStart = frameN  # exact frame index
            image.setAutoDraw(True)

        # *Practice_response* updates
        if t >= .25 and Practice_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            Practice_response.tStart = t  # underestimates by a little under one frame
            Practice_response.frameNStart = frameN  # exact frame index
            Practice_response.status = STARTED
            # keyboard checking is just starting
            Practice_response.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if Practice_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['2', '3', '4', '5','j', 'k', 'l', 'semicolon'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if Practice_response.keys == []:
                    Practice_response.keys = theseKeys[0]  # just the last key pressed


                    Practice_response.rt = Practice_response.clock.getTime()
                    # was this 'correct'?
                    if (Practice_response.keys == str(cor_ans)) or (Practice_response.keys == cor_ans):
                        Practice_response.corr = 1
                        continueRoutine = False
                        running_accuracy.append(1)


                    else:
                        Practice_response.corr = 0
                        running_accuracy.append(0)
                        image.setAutoDraw(False)
                        Wrong_1.setAutoDraw(True)
                        win.flip()
                        core.wait(.2)
                        continueRoutine = False
                    #practiceFeedback.setAutoDraw(True)


        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()


    #-------Ending Routine "practice"-------
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Store nothing



        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in practiceComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()


    #-------Ending Routine "practice"-------
    for thisComponent in practiceComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # Store nothing
#-------Start Routine "Instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practice_with_help* updates
    if t >= 0.0 and pause_after_block.status == NOT_STARTED:
        # keep track of start time/frame for later
        pause_after_block.tStart = t  # underestimates by a little under one frame
        pause_after_block.frameNStart = frameN  # exact frame index
        pause_after_block.setAutoDraw(True)
        event.clearEvents(eventType='keyboard')


    if pause_after_block.status == STARTED:
        theseKeys = event.getKeys()

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    #continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
#-------Ending Routine "Instructions"-------

pause_after_block.setAutoDraw(False)
win.flip()
#Clear events of type keyboard so that next block doesn't immediately advance.
event.clearEvents(eventType='keyboard')


# set up handler to look after randomisation of conditions etc
Block_Loop = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(u'behavior_blocks.csv'),
    seed=None, name='Block_Loop')
thisExp.addLoop(Block_Loop)  # add the loop to the experiment
thisBlock_Loop = Block_Loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock_Loop.rgb)
if thisBlock_Loop != None:
    for paramName in thisBlock_Loop.keys():
        exec(paramName + '= thisBlock_Loop.' + paramName)

nBlock = 0
max_rt = 1
iti = .25
RTclock = core.Clock()

for thisBlock_Loop in Block_Loop:
    nBlock = nBlock+1
    delay = 1
    if nBlock == 7 or nBlock == 6:
        delay = 0



    currentLoop = Block_Loop
    # abbreviate parameter names if possible (e.g. rgb = thisBlock_Loop.rgb)
    if thisBlock_Loop != None:
        for paramName in thisBlock_Loop.keys():
            exec(paramName + '= thisBlock_Loop.' + paramName)

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='sequential',
        extraInfo=expInfo, originPath=None,
        trialList=data.importConditions(u'behavior_stimuli.csv'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    block_rts = []
    acc_last_block = []
    n_stimuli = 0
    for thisTrial in trials:
        core.wait(.05)
        if n_stimuli % 4 == 0:
            core.wait(delay)
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)

        #------Prepare to start Routine "Block"-------
        t = 0
        BlockClock.reset()  # clock
        frameN = -1
        routineTimer.add(.5+max_rt)
        # update component parameters for each repeat
        image_2.setImage(eval(Block_id))
        key_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
        key_response.status = NOT_STARTED
        # keep track of which components have finished
        #see if this works better:

        BlockComponents = []
        BlockComponents.append(image_2)
        BlockComponents.append(key_response)
        BlockComponents.append(Wrong_1)
        for thisComponent in BlockComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #-------Start Routine "Block"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = BlockClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *image_2* updates

            image_2.setAutoDraw(True)
            win.flip()
            RTclock.reset()
            event.clearEvents(eventType='keyboard')
            theseKeys = event.waitKeys(max_rt,('j','k','l','semicolon'), timeStamped = RTclock)

            if theseKeys is None:
                key_response.corr = 0
                key_response.keys=None
                key_response.rt = float('nan')
                Wrong_1.setAutoDraw(True)
                win.flip()
                core.wait(0.1)
                continueRoutine=False

            elif(len(theseKeys[0]) > 0):
                key_response.keys = theseKeys[0][0]  # just the last key pressed
                key_response.rt = theseKeys[0][1]
                # was this 'correct'?
                if (key_response.keys == str(eval(Block_ans))) or (key_response.keys == eval(Block_ans)):
                    key_response.corr = 1

                else:
                    key_response.corr = 0
                    Wrong_1.setAutoDraw(True)
                    win.flip()

                continueRoutine = False

            for thisComponent in BlockComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
                    win.flip()

            core.wait(iti)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
            n_stimuli += 1

        # store data for trials (TrialHandler)
        trials.addData('key_response.keys',key_response.keys)
        trials.addData('key_response.corr', key_response.corr)
        if key_response.keys != None:  # we had a response
            trials.addData('key_response.rt', key_response.rt)

        thisExp.nextEntry()
        block_rts = np.append(block_rts,key_response.rt)
        acc_last_block = np.append(acc_last_block, key_response.corr)

        #save data in case program crashes -- remove this if its causing any hold ups
        if nBlock in [1,2,6]:
            trial_type = 1
        elif nBlock in [3,4,5,7]:
            trial_type = 2
        #ocasionally key is
        if not key_response.rt:
            key_response.rt = float('nan')
        #add data to file
        data_out.loc[len(data_out)+1]=[nBlock, key_response.corr, key_response.rt, trial_type, key_response.keys, str(eval(Block_ans))]
        data_out.to_csv(out_all_fn, index=False)
        #'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])
    #build adaptive rt design.

    n_corr = np.sum(acc_last_block)
    acc_last_block = n_corr/len(acc_last_block)
    mean_rt = np.nanmean(block_rts)
    std_rt = np.nanstd(block_rts)
    adapt_rt = mean_rt+std_rt


    # completed 1 repeats of 'trials'

    #feedback text component after block completion.
    text_4 = visual.TextStim(win=win, ori=0, name='text_2',
        text='End of Block.\nMean response time: %i ms\nTrials correct: %i %% ' %(mean_rt*1000, n_corr/n_trials*100), font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

    #------Prepare to start Routine "Feedback"-------
    t = 0
    FeedbackClock.reset()  # clock
    frameN = -1
    # update component parameters for each repeat
    key_resp_5 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_5.status = NOT_STARTED
    # keep track of which components have finished
    FeedbackComponents = []
    FeedbackComponents.append(text_4)
    FeedbackComponents.append(key_resp_5)
    for thisComponent in FeedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "Feedback"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = FeedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *text_2* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index

            text_4.setAutoDraw(True)
            event.clearEvents(eventType='keyboard')
            core.wait(.5)
        # *key_resp_5* updates
        if t >= 0.0 and key_resp_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_5.tStart = t  # underestimates by a little under one frame
            key_resp_5.frameNStart = frameN  # exact frame index
            key_resp_5.status = STARTED

            # keyboard checking is just starting
            event.clearEvents(eventType='keyboard')


        if key_resp_5.status == STARTED:
            theseKeys = event.getKeys()

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                # a response ends the routine
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FeedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "Feedback"-------
    for thisComponent in FeedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # the Routine "Feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

# completed 1 repeats of 'Block_Loop'


#------Prepare to start Routine "End_Experiment"-------
t = 0
End_ExperimentClock.reset()  # clock
frameN = -1
routineTimer.add(1.000000)
# update component parameters for each repeat
# keep track of which components have finished
End_ExperimentComponents = []
End_ExperimentComponents.append(text)
for thisComponent in End_ExperimentComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "End_Experiment"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = End_ExperimentClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *text* updates
    if t >= 0.0 and text.status == NOT_STARTED:
        # keep track of start time/frame for later
        text.tStart = t  # underestimates by a little under one frame
        text.frameNStart = frameN  # exact frame index
        text.setAutoDraw(True)
    if text.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
        text.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in End_ExperimentComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "End_Experiment"-------
for thisComponent in End_ExperimentComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


#build summary statistics file
lag_names = ['lag' + str(i) for i in  range(1,16)]
data_lags = pd.DataFrame(columns = lag_names)
sum_names = ['block', 'accuracy', 'rt_all', 'rt_cor', 'sdAcc', 'sdRT', 'chunkSize']
data_summary = pd.DataFrame(columns = (sum_names))

win.close()

skip_index = 0
max_lags = 15
plot_fn =  _thisDir + os.sep +'data/rtPlot_%s_%s_%s_Day_%s.svg' %(expInfo['participant'], expName, expInfo['date'], expInfo['session'])


for i in np.unique(data_out[['block']]):
    #make a plot of the response times vs trial and plot by type save with subject's id.
    data_out['trial'] = np.array(range(1,len(data_out)+1))
    sns.set_context("paper")

    if i==7:
        plt.figure(figsize=(8, 6))
        sns.lmplot('trial', 'rt', hue = 'type', data=data_out, fit_reg=False)
        plt.savefig(plot_fn)

    block_df = data_out.loc[data_out['block']==i]
    mean_acc = block_df[['response']].mean()
    rt_all = block_df[['rt']].mean()
    block_df_cor = block_df.loc[block_df['response']==1]
    rt_cor = block_df_cor[['rt']].mean()
    std_acc = block_df[['response']].std()
    std_rt =  block_df_cor[['rt']].std()

    #del skip trials
    good_trials = block_df.drop(block_df.index[:skip_index])
    #replace NaNs with mean of rts in that block
    good_trials = good_trials[['rt']].replace(np.nan,rt_cor.rt)

    #regress the good trials using OLS
    y = np.array(good_trials['rt'])
    x = np.linspace(1,y.size,y.size)
    x = np.vstack([x,np.ones(len(x))]).T
    result = sm.OLS(y, x).fit()
    R = result.resid
    #regress the good trials using 5th order polynmoial
    idx = np.isfinite(y)
    y = y[idx]
    x = np.linspace(1,y.size,y.size)
    z = np.polyfit(x,y, 5)
    p = np.poly1d(z)
    R = y-p(x)

    acfResults = statsmodels.tsa.stattools.acf(R, unbiased=False, nlags=15, qstat=True, fft=False, alpha=0.05, missing='drop')
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
data_summary = pd.merge(data_summary, data_lags, left_on = 'block', right_on='lag1',left_index = True,right_index = True, how= 'outer')
data_summary.to_csv(out_sum_fn, index=False)
real_path = os.path.expanduser('~/Dropbox/modmap/behavior/')
summary_dropbox =  real_path + '%s_summary_%s_%s_session_%s_group_%s.csv' %(expInfo['participant'], expName, expInfo['date'], expInfo['session'], expInfo['group (c or r)'])
allResp_dropbox =  real_path + '%s_allResp_%s_%s_session_%s_group_%s.csv' %(expInfo['participant'], expName,  expInfo['date'], expInfo['session'], expInfo['group (c or r)'])
data_summary.to_csv(summary_dropbox, index=False)
data_out.to_csv(allResp_dropbox, index=False)
data_out.to_csv(out_all_fn, index=False)
core.quit()
