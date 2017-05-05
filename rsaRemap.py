#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division  #
from psychopy import visual, core, data, event, logging, gui
from psychopy.constants import *
import pandas as pd
import numpy as np
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os
import scipy.io
import itertools
from subprocess import call

debug = 0

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
expName = 'rsaRemap'
expInfo = {u'Day': u'',u'session':u'', u'SID': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
session = int(expInfo['session'])
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['SID'], expName, expInfo['date'])
out_all_fn =  _thisDir + os.sep + 'data/%s_%s_Day%s_Session%s_responses.csv' %(expName, expInfo['SID'],expInfo['Day'] , expInfo['session'])
data_out = pd.DataFrame(columns=('onsetTime','correctResp','keysPressed', 'chunkID', 'responseTimes', 'Error'))

# Create random random permtuation of [1,8] so that each subject starts with random presentation of the resp dictionaries, only for the first session
this_subject_mappings_fn =  _thisDir + os.sep + 'data/%s_this_subject_mapping_day_%s.csv' %(expInfo['SID'], expInfo['Day'])
if not os.path.isfile(this_subject_mappings_fn):
    this_subject_mappings = pd.DataFrame(data = np.random.permutation(8))
    this_subject_mappings.to_csv(this_subject_mappings_fn, index=False)
    #dynamically generate onsets
    os.system("optseq2 --ntp 240 --tr 2.0 --psdwin 0 16 2 --ev chunk_R1 6 5 --ev chunk_R2 6 5 --ev chunk_R3 6 5 --ev chunk_R4 6 5 --ev chunk_C1 6 5 --ev chunk_C2 6 5 --ev chunk_C3 6 5 --ev chunk_C4 6 5 --nkeep 8 --o modmap --nsearch 10000 --tnullmin 4 --tprescan -4")
this_day_mapping = pd.read_csv(this_subject_mappings_fn)

thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
endExpNow = False  # flag for 'escape' or other condition => quit the exp

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
practice_with_help = visual.TextStim(win=win, ori=0, name='practice_with_help',
    text=u'Practice trails are about to begin. Ensure that you can comfortably press each button. Press any key to continue',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

practice_without_help = visual.TextStim(win=win, ori=0, name='practice_without_help',
        text=u'Now you will practice the same key presses, but there will not be any text telling you which key to press. The only feedback will be a red circle if you incorrectly press a finger. Once you reach at least 90 % accuarcy, the experiment will automatically advance to the next phase. ',    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

chunk_practice_sequential = visual.TextStim(win=win, ori=0, name='chunk_practice_sequential',
        text=u'Now you will practice the groups of 4 presses, they will all appear on the screen at the same time. Take your time to press each with. There is a 6 second time limit for the entire set. Press any key to start.',    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

begin_scan = visual.TextStim(win=win, ori=0, name='begin_scan',
        text=u'Well done, practice is completed. Now the scan will start where you will perform a group of 4 movements as quickly and accurately as you can.', font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
chunkClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')

size_chunk = [200,200]
image = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=size_chunk,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

chunk_image_1 = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[-300, 0], size=size_chunk,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

chunk_image_2 = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[-100, 0], size=size_chunk,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

chunk_image_3 = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[100, 0], size=size_chunk,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

chunk_image_4 = visual.ImageStim(win=win, name='image',units='pix',
    image='sin', mask=None,
    ori=0, pos=[300, 0], size=size_chunk,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

wrong_rad = size_chunk[0]/2
chunk_image_1_wrong = visual.Circle(win=win,units='pix',
    ori=0, pos=[-300, 0], radius = wrong_rad,lineColor='red', fillColor = 'red')

chunk_image_2_wrong = visual.Circle(win=win,units='pix',
    ori=0, pos=[-100, 0], radius = wrong_rad,lineColor='red', fillColor = 'red')

chunk_image_3_wrong = visual.Circle(win=win,units='pix',
    ori=0, pos=[100, 0], radius = wrong_rad,lineColor='red', fillColor = 'red')

chunk_image_4_wrong = visual.Circle(win=win,units='pix',
    ori=0, pos=[300, 0], radius = wrong_rad,lineColor='red', fillColor = 'red')

fixation = visual.ShapeStim(win,
    vertices=((0, -50), (0, 50), (0,0), (-50,0), (50, 0)),
    lineWidth=5,
    closeShape=False,units='pix',
    lineColor='white')

Wrong_1 = visual.Circle(win=win, units = 'pix', radius = wrong_rad,lineColor='red', fillColor = 'red')

EndClock = core.Clock()
text = visual.TextStim(win=win, ori=0, name='text',
    text=u'Block is completed. You may rest. Try to minimize movement.',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

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
resp_dict = [{'R':'A', 'M':'B', 'I':'C' ,'P':'D'}, {'I':'A', 'P':'B', 'R':'C' ,'M':'D'}, {'M':'A', 'R':'B', 'I':'C' ,'P':'D'}, {'P':'A', 'I':'B', 'R':'C' ,'M':'D'}, {'R':'A', 'P':'B', 'I':'C' ,'M':'D'}, {'M':'A', 'I':'B', 'R':'C' ,'P':'D'}, {'P':'A', 'R':'B', 'M':'C' ,'I':'D'},{'R':'A', 'I':'B', 'P':'C' ,'M':'D'}]
resp_dict = resp_dict[this_day_mapping.ix[session-1,0]] #grab the mapping for this session.
resp_dict_invert = dict([(v, k) for k, v in resp_dict.iteritems()])

#Practice trial handle
this_practice_dict = {key_map[key]: img_dict[resp_dict[key]] for key in key_map.keys()}
df_practice = {'cor_ans':this_practice_dict.keys(),'img_id': this_practice_dict.values()}
df_practice = pd.DataFrame(data=df_practice)
df_practice = df_practice[['img_id', 'cor_ans']]
practiceOnsets_fn =  _thisDir + os.sep + 'data/%s_practiceOnsets_Day%s_session_%s.csv' %(expInfo['SID'],expInfo['Day'],expInfo['session'])
df_practice.to_csv(practiceOnsets_fn, index=False)

this_practice_dict = {key_map[key]: img_dict[resp_dict[key]] for key in key_map.keys()}
df_practice = {'cor_ans':this_practice_dict.keys(),'img_id': this_practice_dict.values()}
df_practice = pd.DataFrame(data=df_practice)
df_practice = df_practice[['img_id', 'cor_ans']]
df_practice = pd.concat([df_practice]*500, ignore_index=True)
df_practice = df_practice.sample(frac=1).reset_index(drop=True)
practiceChunks_fn =  _thisDir + os.sep + 'data/%s_practiceChunks_Day%s_session_%s.csv' %(expInfo['SID'],expInfo['Day'],expInfo['session'])
df_practice.to_csv(practiceChunks_fn, index=False)

practice_chunks_ordered = pd.DataFrame({'trial_img': ['chunk_C1','chunk_C2','chunk_C3','chunk_C4','chunk_R1','chunk_R2','chunk_R3','chunk_R4'], 'trial_ans': np.arange(1,9)})
practice_chunks_ordered_fn =  _thisDir + os.sep + 'data/%s_practice_chunks_ordered_Day%s_session_%s.csv' %(expInfo['SID'],expInfo['Day'],expInfo['session'])
practice_chunks_ordered.to_csv(practice_chunks_ordered_fn, index=False)

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

dfStims = pd.DataFrame
sequence_img_ids = []

key_dict = {2:'2', 3:'3', 4:'4', 5:'5'}

keys = [1,2,3,4,5,6,7,8]
img_filenames = ['chunk_C1', 'chunk_C2', 'chunk_C3', 'chunk_C4', 'chunk_R1', 'chunk_R2', 'chunk_R3', 'chunk_R4']

img_dict = dict(zip(keys, img_filenames))
iti = .250

n_trs = 240
onset_filename = 'modmap-00%d.par' % (session)
dfStims = pd.read_csv(onset_filename, header=None, sep=r"\s*")
dfStims = dfStims[[0,4]]
dfStims.columns = ['time', 'trial_img']
dfStims.set_index('time')
new_index = pd.Index(np.arange(0,n_trs*2,2), name='time')
dfStims = dfStims.set_index('time').reindex(new_index).reset_index()
dfStims = dfStims.fillna('image_folder/skip.png')
dfStims['trial_ans'] = dfStims['trial_img']
dict_lookup = {'chunk_C1':1, 'chunk_C2':2, 'chunk_C3':3, 'chunk_C4':4, 'chunk_R1':5, 'chunk_R2':6, 'chunk_R3':7, 'chunk_R4':8, 'image_folder/skip.png':0 }
dfStims = dfStims.replace({"trial_ans": dict_lookup})
del dfStims['time']
dfStims.to_csv('MM_onsets.csv', index=False)
filename = _thisDir + os.sep + 'data/%s_%s_%s_onsets.csv' %(expInfo['SID'], expName, expInfo['session'])
dfStims.to_csv(filename)

t_vec = range(0,n_trs*2,2)
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
    if event.getKeys(keyList=['2', '3', '4', '5']):
        continueRoutine = False
        practice_with_help.setAutoDraw(False)
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
practiceClock = core.Clock()

mapping = {2: 'Index ', 3: 'Middle ', 4: 'Ring ', 5:'Little '}
for thisPractice_loop in practice_loop:
    if debug:
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
practice_loop = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(practiceChunks_fn),
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
    if debug:
        break
    win.flip()
    #%Check if threshold performance has been met.
    n_practice_trials +=1
    if n_practice_trials >80 and (sum(running_accuracy[-20:])/20.0)>.9:
        break
    if n_practice_trials % 4 == 0:
        core.wait(1)

    # abbreviate parameter names if possible (e.g. rgb = thisPractice_loop.rgb)
    if thisPractice_loop != None:
        for paramName in thisPractice_loop.keys():
            exec(paramName + '= thisPractice_loop.' + paramName)

    #------Prepare to start Routine "practice"-------
    t = 0
    practiceClock.reset()
    routineTimer.add(100)  # clock
    frameN = -1
    image.setImage(img_id)
    Practice_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
    Practice_response.status = NOT_STARTED
    practiceComponents = []
    practiceComponents.append(image)
    practiceComponents.append(Practice_response)
    practiceComponents.append(Wrong_1)


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


## Chunk Practice Loop through each Chunk R1-R4 and C1-C4
#------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
InstructionsComponents = []
InstructionsComponents.append(chunk_practice_sequential)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


#-------Start Routine "Practice chunks sequential help"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *practice_with_help* updates
    if t >= 0.0 and chunk_practice_sequential.status == NOT_STARTED:
        # keep track of start time/frame for later
        chunk_practice_sequential.tStart = t  # underestimates by a little under one frame
        chunk_practice_sequential.frameNStart = frameN  # exact frame index
        chunk_practice_sequential.setAutoDraw(True)

    if event.getKeys(keyList=['2', '3', '4', '5']):
        chunk_practice_sequential.setAutoDraw(False)
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

trials = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions(practice_chunks_ordered_fn),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)
RTclock = core.Clock()
max_rt = 1
trial = -1
for thisTrial in trials:
    if debug:
        break
    trial = trial+1
    currentLoop = trials
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    win.flip()
    frameN = -1

    chunk = chunk_dict[trial_img]
    cor_resp = cor_resp_dict[trial_img]
    event.clearEvents(eventType='keyboard') #clear after executing each chunk
    key_response = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_response.status = NOT_STARTED
    onsetTime = globalClock.getTime()
    chunk_image_1.setImage(chunk[0])
    chunk_image_1.setAutoDraw(True)
    chunk_image_2.setImage(chunk[1])
    chunk_image_2.setAutoDraw(True)
    chunk_image_3.setImage(chunk[2])
    chunk_image_3.setAutoDraw(True)
    chunk_image_4.setImage(chunk[3])
    chunk_image_4.setAutoDraw(True)
    fixation.setAutoDraw(False)
    win.flip()
    chunkClock.reset()
    n_elements = 5
    for chunk_element,this_cor_resp,this_elem in zip(chunk, cor_resp, xrange(1, n_elements)):
        if chunkClock.getTime() > 5.95:
            break
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
        trialClock.reset()
        while continueRoutine:
            t = trialClock.getTime()
            frameN = frameN + 1

            if t >= 0.0 and image.status == NOT_STARTED:
                image.tStart = t
                image.frameNStart = frameN

            if image.status == STARTED and t >= (0.0 + (6-win.monitorFramePeriod*0.75)):
                image.setAutoDraw(False)
                continueRoutine = False

            if t >= 0.0 and key_response.status == NOT_STARTED:
                key_response.tStart = t
                key_response.frameNStart = frameN
                key_response.status = STARTED
                key_response.clock.reset()  # now t=0

            if key_response.status == STARTED and t >= (0.0 + (6-win.monitorFramePeriod*0.75)):
                key_response.status = STOPPED
                continueRoutine = False

            if key_response.status == STARTED:
                theseKeys = event.getKeys(keyList=['2', '3', '4', '5'])
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:
                    key_response.keys.extend(theseKeys)  # storing all keys
                    key_response.rt.append(key_response.clock.getTime())
                    if (theseKeys[0] == str(this_cor_resp)) or (theseKeys[0] == this_cor_resp):
                        mycode = 'chunk_image_'+str(this_elem)+'.setAutoDraw(False)'
                        exec(mycode)
                        continueRoutine = False
                        win.flip()
                        made_error = 0
                    else:
                        mycode = 'chunk_image_'+str(this_elem)+'_wrong.setAutoDraw(True)'
                        exec(mycode)
                        win.flip()
                        core.wait(.1)
                        #Wrong_1.setAutoDraw(True)""
                        mycode = 'chunk_image_'+str(this_elem)+'_wrong.setAutoDraw(False)'
                        exec(mycode)
                        win.flip()
                        continueRoutine = True
                        made_error = 1

            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            if continueRoutine:
                win.flip()
            if chunkClock.getTime() > 5.95:
                break
        if chunkClock.getTime() > 5.95:
            break
        win.flip()

    chunk_image_1.setAutoDraw(False)
    chunk_image_2.setAutoDraw(False)
    chunk_image_3.setAutoDraw(False)
    chunk_image_4.setAutoDraw(False)
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    thisExp.nextEntry()
    win.flip()
    core.wait(2.0)

## End Chunk Practice

t = 0
InstructionsClock.reset()  # clock
frameN = -1
routineTimer.add(5.000000)

InstructionsComponents = []
InstructionsComponents.append(begin_scan)
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Begin the Scan"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    t = InstructionsClock.getTime()
    frameN = frameN + 1
    if t >= 0.0 and begin_scan.status == NOT_STARTED:
        begin_scan.tStart = t
        begin_scan.frameNStart = frameN
        begin_scan.setAutoDraw(True)
    if begin_scan.status == STARTED and t >= (0.0 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
        begin_scan.setAutoDraw(False)
        continueRoutine = False

    if not continueRoutine:
        break
    continueRoutine = False
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break

    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:
        win.flip()

### Begin Scan Acquisition
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
ScannerKey = event.waitKeys(keyList=["asciicircum","escape"])

if endExpNow or "escape" in ScannerKey:
   core.quit()
globalClock.reset()

trial = -1
for thisTrial in trials:
    trial = trial+1
    currentLoop = trials

    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    fixation.setAutoDraw(True)
    win.flip()
    frameN = -1
    routineTimer.add(2.000000)
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


        chunk_image_1.setImage(chunk[0])
        chunk_image_1.setAutoDraw(True)
        chunk_image_2.setImage(chunk[1])
        chunk_image_2.setAutoDraw(True)
        chunk_image_3.setImage(chunk[2])
        chunk_image_3.setAutoDraw(True)
        chunk_image_4.setImage(chunk[3])
        chunk_image_4.setAutoDraw(True)
        fixation.setAutoDraw(False)
        win.flip()
        chunkClock.reset()
        n_elements = 5
        made_error = 0
        for chunk_element,this_cor_resp,this_elem in zip(chunk, cor_resp, xrange(1, n_elements)):
            if chunkClock.getTime() > 5.95:
                break
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
            trialClock.reset()
            while continueRoutine:
                t = trialClock.getTime()
                frameN = frameN + 1

                if t >= 0.0 and image.status == NOT_STARTED:
                    image.tStart = t
                    image.frameNStart = frameN

                if image.status == STARTED and t >= (0.0 + (6-win.monitorFramePeriod*0.75)):
                    image.setAutoDraw(False)
                    continueRoutine = False

                if t >= 0.0 and key_response.status == NOT_STARTED:
                    key_response.tStart = t
                    key_response.frameNStart = frameN
                    key_response.status = STARTED
                    key_response.clock.reset()  # now t=0

                if key_response.status == STARTED and t >= (0.0 + (6-win.monitorFramePeriod*0.75)):
                    key_response.status = STOPPED
                    continueRoutine = False

                if key_response.status == STARTED:
                    theseKeys = event.getKeys(keyList=['2', '3', '4', '5'])
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:
                        key_response.keys.extend(theseKeys)  # storing all keys
                        key_response.rt.append(key_response.clock.getTime())
                        if (theseKeys[0] == str(this_cor_resp)) or (theseKeys[0] == this_cor_resp):
                            mycode = 'chunk_image_'+str(this_elem)+'.setAutoDraw(False)'
                            exec(mycode)
                            continueRoutine = False
                            win.flip()

                        else:
                            mycode = 'chunk_image_'+str(this_elem)+'_wrong.setAutoDraw(True)'
                            exec(mycode)
                            win.flip()
                            core.wait(.1)
                            #Wrong_1.setAutoDraw(True)""
                            mycode = 'chunk_image_'+str(this_elem)+'_wrong.setAutoDraw(False)'
                            exec(mycode)
                            win.flip()
                            continueRoutine = True
                            made_error = 1

                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break

                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                if continueRoutine:
                    win.flip()
                if chunkClock.getTime() > 5.95:
                    break
            if chunkClock.getTime() > 5.95:
                break
            win.flip()

        chunk_image_1.setAutoDraw(False)
        chunk_image_2.setAutoDraw(False)
        chunk_image_3.setAutoDraw(False)
        chunk_image_4.setAutoDraw(False)
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
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
        data_out.loc[len(data_out)+1]=[onsetTime,cor_resp_dict[trial_img], str(key_response.keys).strip('[]'), trial_img, key_response.rt, made_error]
        data_out.to_csv(out_all_fn, index=False)

    elif trial_img == 'image_folder/skip.png':
        fixation.setAutoDraw(True)
        core.wait(0.0)
    thisExp.nextEntry()

core.wait(3)
fixation.setAutoDraw(False)
win.flip()

#------Prepare to start Routine "End"-------
t = 0
EndClock.reset()  # clock
frameN = -1
routineTimer.add(1.000000)
EndComponents = []
EndComponents.append(text)
for thisComponent in EndComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "End"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    t = EndClock.getTime()
    frameN = frameN + 1
    if t >= 0.0 and text.status == NOT_STARTED:
        text.tStart = t
        text.frameNStart = frameN
        text.setAutoDraw(True)
    if text.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)):
        text.setAutoDraw(False)
    if not continueRoutine:
        break
    continueRoutine = False
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    if continueRoutine:
        win.flip()

#-------Ending Routine "End"-------
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
win.close()
core.quit()
