#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import pandas as pd
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io
import itertools

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

expName = 'rsaRemap'
expInfo = {u'Day': u'',u'session':u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
session = int(expInfo['session'])

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

out_all_fn =  _thisDir + os.sep + 'data/%s_%s_%s_%s_responses.csv' %(expName, expInfo['participant'],expInfo['Day'] , expInfo['session'])
data_out = pd.DataFrame(columns=('onsetTime','correctResp','keysPressed', 'chunk_id'))


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
win = visual.Window(size=(500, 500), fullscr=False, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Instructions"
InstructionsClock = core.Clock()
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

begin_scan = visual.TextStim(win=win, ori=0, name='begin_scan',
        text=u'Well done, practice is completed. Now the scan will start where you will perform 4 groups of movements as quickly as you can.',    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')
image = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[200,200],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

fixation = visual.ShapeStim(win,
    vertices=((0, -50), (0, 50), (0,0), (-50,0), (50, 0)),
    lineWidth=5,
    closeShape=False,units='pix',
    lineColor='white')

Wrong_1 = visual.Circle(win=win, units = 'pix', radius = 100,lineColor='red', fillColor = 'red')


# Initialize components for Routine "End"
EndClock = core.Clock()
text = visual.TextStim(win=win, ori=0, name='text',
    text=u'Experiment is completed. Thank you for your participation.',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

practiceClock = core.Clock()
#######################
#### Set up onsets ####
#######################
#Visual chunks
ChunkC1 = ['A', 'B', 'D', 'A']
ChunkC2 = ['C', 'D', 'B', 'D']
ChunkC3 = ['B', 'A', 'C', 'B']
ChunkC4 = ['D', 'C', 'A', 'C']
#Response chunks
ChunkR1 = ['I', 'M', 'P', 'I']
ChunkR2 = ['R', 'P', 'M', 'P']
ChunkR3 = ['M', 'I', 'R', 'M']
ChunkR4 = ['P', 'R', 'I', 'R']

#static dict
key_map = {'I':2, 'M':3, 'R':4, 'P':5}

#Current mapping
img_dict = {'A': 'image_folder/stim_2.png', 'B': 'image_folder/stim_3.png', 'C': 'image_folder/stim_4.png', 'D': 'image_folder/stim_5.png'}

#This dict changes each run.
resp_dict = [{'R':'A', 'M':'B', 'I':'C' ,'P':'D'}, {'I':'A', 'P':'B', 'M':'C' ,'R':'D'}, {'M':'A', 'R':'B', 'I':'C' ,'P':'D'}, {'P':'A', 'M':'B', 'R':'C' ,'I':'D'}, {'R':'A', 'P':'B', 'I':'C' ,'M':'D'}, {'M':'A', 'I':'B', 'R':'C' ,'P':'D'}, {'P':'A', 'R':'B', 'M':'C' ,'I':'D'},{'R':'A', 'I':'B', 'P':'C' ,'M':'D'}]
resp_dict = resp_dict[session-1]
resp_dict_invert = dict([(v, k) for k, v in resp_dict.iteritems()])

#Practice trial handle
this_practice_dict = {key_map[key]: img_dict[resp_dict[key]] for key in key_map.keys()}
df_practice = {'cor_ans':this_practice_dict.keys(),'img_id': this_practice_dict.values()}
df_practice = pd.DataFrame(data=df_practice)
df_practice = df_practice[['img_id', 'cor_ans']]
practiceOnsets_fn =  _thisDir + os.sep + 'data/%s_practiceOnsets_session_%s.csv' %(expInfo['participant'], expInfo['session'])
df_practice.to_csv(practiceOnsets_fn, index=False)



ChunkC1_img = [img_dict[letter] for letter in ChunkC1]
ChunkC1_cor_key = [key_map[resp_dict_invert[letter]] for letter in ChunkC1]
ChunkC2_img = [img_dict[letter] for letter in ChunkC2]
ChunkC2_cor_key = [key_map[resp_dict_invert[letter]] for letter in ChunkC2]
ChunkC3_img = [img_dict[letter] for letter in ChunkC3]
ChunkC3_cor_key = [key_map[resp_dict_invert[letter]] for letter in ChunkC3]
ChunkC4_img = [img_dict[letter] for letter in ChunkC4]
ChunkC4_cor_key = [key_map[resp_dict_invert[letter]] for letter in ChunkC4]

ChunkR1_img = [img_dict[resp_dict[letter]] for letter in ChunkR1]
ChunkR1_cor_key = [key_map[letter] for letter in ChunkR1]
ChunkR2_img = [img_dict[resp_dict[letter]] for letter in ChunkR2]
ChunkR2_cor_key = [key_map[letter] for letter in ChunkR2]
ChunkR3_img = [img_dict[resp_dict[letter]] for letter in ChunkR3]
ChunkR3_cor_key = [key_map[letter] for letter in ChunkR3]
ChunkR4_img = [img_dict[resp_dict[letter]] for letter in ChunkR4]
ChunkR4_cor_key = [key_map[letter] for letter in ChunkR4]

chunk_dict = {'chunk_C1': ChunkC1_img, 'chunk_C2': ChunkC2_img,'chunk_C3': ChunkC3_img,'chunk_C4': ChunkC4_img,'chunk_R1': ChunkR1_img,'chunk_R2': ChunkR2_img,'chunk_R3': ChunkR3_img,'chunk_R4': ChunkR4_img}
cor_resp_dict = {'chunk_C1': ChunkC1_cor_key, 'chunk_C2': ChunkC2_cor_key,'chunk_C3': ChunkC3_cor_key,'chunk_C4': ChunkC4_cor_key,'chunk_R1': ChunkR1_cor_key,'chunk_R2': ChunkR2_cor_key,'chunk_R3': ChunkR3_cor_key,'chunk_R4': ChunkR4_cor_key}

corr_thresh = 0.05
dfStims = pd.DataFrame
sequence_img_ids = []

key_dict = {2:'2', 3:'3', 4:'4', 5:'5'}

keys = [1,2,3,4,5,6,7,8]
img_filenames = ['chunk_C1', 'chunk_C2', 'chunk_C3', 'chunk_C4', 'chunk_R1', 'chunk_R2', 'chunk_R3', 'chunk_R4']

img_dict = dict(zip(keys, img_filenames))
iti = .250

isDone = 0
while not isDone:
    trial_types = np.asarray([1,2,3,4,5,6,7,8])
    trial_IDs = np.asarray(range(8))
    iti_range = np.asarray([2, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8])


    n_post = 3
    t_vec = []
    iti_vec = []
    tid_vec = []

    for tt in range(0,len(trial_types)):
        t_vec = np.repeat(trial_types,6)
        iti_vec = np.tile(iti_range,4)

    np.random.shuffle(t_vec)
    np.random.shuffle(iti_vec)
    vec = [0]
    id_vec = vec

    for t in range(0, len(t_vec)):
        vec = vec + [t_vec[t]] +  np.repeat(0,iti_vec[t]).tolist()
    vec = vec + [0,0,0]
    dfStims = pd.DataFrame()
    X = np.zeros((len(vec),len(trial_types)))
    ons = np.zeros((6,8))
    for c in trial_types:
        a = np.where(vec==c)[0]
        ons[:,c-2] = a*2
        for indx in range(0, len(a)):
            name = a[indx]
            X[a[indx]][c-2]= 1

    df=pd.DataFrame(X)
    cxy = df.corr()
    cxy = abs(np.tril(cxy, k=-1))
    if cxy.max() < corr_thresh:
        isDone = 1

for x in range(0,len(vec)):
    if vec[x] == 0:
        sequence_img_ids.append('image_folder/skip.png')
    elif vec[x] != 0:
        sequence_img_ids.append(img_dict[vec[x]])

id_vec = vec
t_vec = range(0,480,2)
dfStims['trial_img'] = sequence_img_ids
dfStims['trial_ans'] = vec

filename = _thisDir + os.sep + 'data/%s_%s_%s_onsets.csv' %(expInfo['participant'], expName, expInfo['session'])
np.savetxt(filename, ons, '%5.2f',delimiter=",")
dfStims.to_csv('MM_onsets.csv', index= False) # Change this so that it is unique.

#######################
## End Set up onsets ##
#######################


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

#------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
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
mapping = {2: 'Index ', 3: 'Middle ', 4: 'Ring ', 5:'Little '}
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
            theseKeys = event.getKeys(keyList=['2', '3', '4', '5','h', 'j', 'k', 'l'])

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

# completed 5 repeats of 'practice_loop'
#------Prepare to start Routine "Instructions"-------
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

for thisPractice_loop in practice_loop:

    #%Check if threshold performance has been met.
    n_practice_trials +=1
    if n_practice_trials >20 and (sum(running_accuracy[-20:])/20.0)>.9:
        break



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
    #eplicit_instruction = mapping[cor_ans]
    #practiceFeedback = visual.TextStim(win=win, ori=0, name='text_4',text=eplicit_instruction,font=u'Arial', pos=[0, -.6], height=0.1, wrapWidth=None, color=u'white', colorSpace='rgb', opacity=1,depth=0.0)
    #practiceComponents.append(practiceFeedback)

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
            image.setAutoDraw(True)
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
            theseKeys = event.getKeys(keyList=['2', '3', '4', '5','h', 'j', 'k', 'l'])

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
                        image.setAutoDraw(True)
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

### End of practice, wait 10 second befor econitnueing.
t = 0
InstructionsClock.reset()  # clock
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(begin_scan)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Begin the Scan"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practice_with_help* updates
    if t >= 0.0 and begin_scan.status == NOT_STARTED:
        # keep track of start time/frame for later
        begin_scan.tStart = t  # underestimates by a little under one frame
        begin_scan.frameNStart = frameN  # exact frame index
        begin_scan.setAutoDraw(True)
    if begin_scan.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
        begin_scan.setAutoDraw(False)
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


### Begin Scan Acquisition
# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(u'MM_onsets.csv'),
    seed=None, name='trials')


thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)
RTclock = core.Clock()
max_rt = 1


##### Wait for scanner trigger key #####
event.clearEvents(eventType='keyboard')

ScannerKey = event.waitKeys(["^","escape"])
if endExpNow or "escape" in ScannerKey:
   core.quit()
globalClock.reset()



trial = -1
for thisTrial in trials:
    trial = trial+1

    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    fixation.setAutoDraw(True)
    win.flip()

    #------Prepare to start Routine "trial"-------

    frameN = -1
    routineTimer.add(2.000000)

    #For Debugging
    #print globalClock.getTime()
    #print t_vec[trial]
    # update component parameters for each repeat
    while globalClock.getTime() < t_vec[trial]:
        core.wait(.001)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()


    if trial_img != 'image_folder/skip.png':
        chunk = chunk_dict[trial_img]
        cor_resp = cor_resp_dict[trial_img]
        event.clearEvents(eventType='keyboard') #clear after executing each chunk
        key_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
        key_response.status = NOT_STARTED
        onsetTime = globalClock.getTime()
        for chunk_element,this_cor_resp in zip(chunk, cor_resp):

            fixation.setAutoDraw(False)
            win.flip()
            image.setImage(chunk_element)

            # keep track of which components have finished
            trialComponents = []
            trialComponents.append(image)
            trialComponents.append(key_response)

            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            #-------Start Routine "trial"-------
            continueRoutine = True
            trialClock.reset()  # clock
            # Print routTimer to verify matches correct onset timings.
            # print routineTimer.getTime()

            while continueRoutine:
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *image* updates
                if t >= 0.0 and image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    image.tStart = t  # underestimates by a little under one frame
                    image.frameNStart = frameN  # exact frame index
                    image.setAutoDraw(True)
                    #Only grab onset Time if this is the first element in the chunk

                if image.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                    image.setAutoDraw(False)
                    continueRoutine = False
                # *key_response* updates
                if t >= 0.0 and key_response.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    key_response.tStart = t  # underestimates by a little under one frame
                    key_response.frameNStart = frameN  # exact frame index
                    key_response.status = STARTED
                    # keyboard checking is just starting
                    key_response.clock.reset()  # now t=0

                if key_response.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                    key_response.status = STOPPED
                    continueRoutine = False
                if key_response.status == STARTED:
                    theseKeys = event.getKeys(keyList=['2', '3', '4', '5'])
                    # check for quit:

                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed

                        #Check if response was correct:
                        key_response.keys.extend(theseKeys)  # storing all keys
                        key_response.rt.append(key_response.clock.getTime())
                        if (theseKeys[0] == str(this_cor_resp)) or (theseKeys[0] == this_cor_resp):
                            image.setAutoDraw(False)
                            continueRoutine = False
                            win.flip()
                        else:
                            image.setAutoDraw(False)
                            Wrong_1.setAutoDraw(True)
                            win.flip()
                            continueRoutine = False
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break

                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            Wrong_1.setAutoDraw(False)
            win.flip()
            core.wait(iti)

        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_response.keys in ['', [], None]:  # No response was made
           key_response.keys=None
           # was no response the correct answer?!
           if str(trial_ans).lower() == 'none': key_response.corr = 1  # correct non-response
           else: key_response.corr = 0  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_response.keys',key_response.keys)
        trials.addData('key_response.corr', key_response.corr)
        if key_response.keys != None:  # we had a response
            trials.addData('key_response.rt', key_response.rt)
        thisExp.nextEntry()
        win.flip()
        #Save Data to output File

        #Change this trail_ans
        data_out.loc[len(data_out)+1]=[onsetTime,cor_resp_dict[trial_img], str(key_response.keys).strip('[]'), trial_img]
        data_out.to_csv(out_all_fn, index=False)

    elif trial_img == 'image_folder/skip.png':
        fixation.setAutoDraw(True)
        core.wait(0.0)
    thisExp.nextEntry()


# completed all trials


#------Prepare to start Routine "End"-------
t = 0
EndClock.reset()  # clock
frameN = -1
routineTimer.add(1.000000)
# update component parameters for each repeat
# keep track of which components have finished
EndComponents = []
EndComponents.append(text)
for thisComponent in EndComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "End"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = EndClock.getTime()
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
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "End"-------
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
win.close()
core.quit()
