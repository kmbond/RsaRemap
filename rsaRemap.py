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
expInfo = {u'Day': u'',u'session':u'', u'participant': u'', u'group': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
session = int(expInfo['session'])

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

out_all_fn =  _thisDir + os.sep + 'data/%s_%s_%s_responses.csv' %(expInfo['participant'], expName, expInfo['session'])
data_out = pd.DataFrame(columns=('onsetTime','correctResp','keysPressed', 'img_filename'))


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
win = visual.Window(size=(500, 500), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
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
text_2 = visual.TextStim(win=win, ori=0, name='text_2',
    text=u'The experiment is about to begin. ',    font=u'Arial',
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
    vertices=((0, -0.2), (0, 0.2), (0,0), (-0.2,0), (0.2, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor='white')

Wrong_1 = visual.Circle(win=win, units = 'pix', radius = 100,lineColor='red', fillColor = 'red')


# Initialize components for Routine "End"
EndClock = core.Clock()
text = visual.TextStim(win=win, ori=0, name='text',
    text=u'Experiment is completed. Thank you for your participation.',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)


#######################
#### Set up onsets ####
#######################
keys = [2, 3, 4, 5]
img_filenames = ['image_folder/stim_2.png', 'image_folder/stim_3.png', 'image_folder/stim_4.png', 'image_folder/stim_5.png']

img_dicts = [dict(zip(kperm, img_filenames)) for kperm in itertools.permutations(keys, len(img_filenames))]
img_dicts = [img_dicts[i] for i in (0,23,13,4,8,21,16,7)]

#Dynamic mapping
img_dict = img_dicts[session-1]
#Static mapping
#img_dict = {2: 'image_folder/stim_2.png', 3: 'image_folder/stim_3.png', 4: 'image_folder/stim_4.png', 5: 'image_folder/stim_5.png'}

corr_thresh = 0.1
dfStims = pd.DataFrame
sequence_img_ids = []

key_dict = {2:'2', 3:'3', 4:'4', 5:'5'}

isDone = 0
while not isDone:
    trial_types = np.asarray([2, 3, 4, 5])
    trial_IDs = np.asarray(range(4))
    trial_freq = np.asarray([12, 12, 12, 12])
    iti_range = np.asarray([2, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7, 8])

    n_post = 3
    t_vec = []
    iti_vec = []
    tid_vec = []

    for tt in range(0,len(trial_types)):
        t_vec = np.repeat(trial_types,12)
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
    ons = np.zeros((12,4))
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


#######################
## End Set up onsets ##
#######################

filename = _thisDir + os.sep + 'data/%s_%s_%s_onsets.csv' %(expInfo['participant'], expName, expInfo['session'])
np.savetxt(filename, ons, '%5.2f',delimiter=",")
dfStims.to_csv('MM_onsets.csv', index= False)


#######################
## Save as mat file for SPM
#######################

#
# new_onsets = np.empty((4,), dtype=object)
# df = pd.read_csv('0273_r2d4_MM_Run1_onsets.csv',header=None)
# new_onsets[0] = np.array(df[0][:,np.newaxis])/2
# new_onsets[1] = np.array(df[1][:,np.newaxis])/2
# new_onsets[2] = np.array(df[2][:,np.newaxis])/2
# new_onsets[3] = np.array(df[3][:,np.newaxis])/2
# data={}
# data['ons'] = new_onsets
# scipy.io.savemat('0273_r2d4_MM_Run1_onsets.mat', data)
#

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
InstructionsComponents.append(text_2)
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

    # *text_2* updates
    if t >= 0.0 and text_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_2.tStart = t  # underestimates by a little under one frame
        text_2.frameNStart = frameN  # exact frame index
        text_2.setAutoDraw(True)
    if text_2.status == STARTED and t >= (0.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
        text_2.setAutoDraw(False)

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
        fixation.setAutoDraw(False)
        win.flip()
        image.setImage(trial_img)
        key_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
        key_response.status = NOT_STARTED
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
                   # get current me
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *image* updates
            if t >= 0.0 and image.status == NOT_STARTED:
                # keep track of start time/frame for later
                image.tStart = t  # underestimates by a little under one frame
                image.frameNStart = frameN  # exact frame index
                image.setAutoDraw(True)
                onsetTime = globalClock.getTime()
            if image.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
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
                event.clearEvents(eventType='keyboard')
            if key_response.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                key_response.status = STOPPED
                continueRoutine = False
            if key_response.status == STARTED:
                theseKeys = event.getKeys(keyList=['2', '3', '4', '5'])

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_response.keys.extend(theseKeys)  # storing all keys
                    key_response.rt.append(key_response.clock.getTime())
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


        data_out.loc[len(data_out)+1]=[onsetTime,trial_ans, str(key_response.keys).strip('[]'), trial_img]
        data_out.to_csv(out_all_fn, index=False)

    elif trial_img == 'image_folder/skip.png':
        fixation.setAutoDraw(True)
        core.wait(0.5)
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
