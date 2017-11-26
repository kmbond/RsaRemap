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
import time


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

expName = 'pilotPerformance'
expInfo = {u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

out_all_fn =  _thisDir + os.sep + 'data/%s__SID_%s_responses.csv' %(expName, expInfo['participant'])
data_out = pd.DataFrame(columns=('nTrials','accuracy', 'time'))


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
practice_with_help = visual.TextStim(win=win, ori=0, name='practice_with_help',
    text=u'Practice trials are about to begin. Ensure that you can comfortably press each button.',    font=u'Arial',
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

key_map = {'I':2, 'M':3, 'R':4, 'P':5}

#Current mapping
img_dict = {'A': 'image_folder/stim_2.png', 'B': 'image_folder/stim_3.png', 'C': 'image_folder/stim_4.png', 'D': 'image_folder/stim_5.png'}


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

event.clearEvents(eventType='keyboard')

#-------Start Routine "Instructions"-------
continueRoutine = True
while continueRoutine:
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
        event.clearEvents(eventType='keyboard')


    if practice_with_help.status == STARTED:
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

#Clear events of type keyboard so that next block doesn't immediately advance.
event.clearEvents(eventType='keyboard')



for session in range(1,9):
    n_stimuli = 0
    pause_text = 'Block %d is completed. Press any key to continue' %(session)
    pause_after_block = visual.TextStim(win=win, ori=0, name='text',
        text=pause_text,    font=u'Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color=u'white', colorSpace='rgb', opacity=1,
        depth=0.0)

    event.clearEvents(eventType='keyboard')
    #-------Ending Routine "Instructions"-------
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    #Remake trails for each session.
    #This dict changes each run.
    resp_dict = [{'R':'A', 'M':'B', 'I':'C' ,'P':'D'}, {'I':'A', 'P':'B', 'M':'C' ,'R':'D'}, {'M':'A', 'R':'B', 'I':'C' ,'P':'D'}, {'P':'A', 'M':'B', 'R':'C' ,'I':'D'}, {'R':'A', 'P':'B', 'I':'C' ,'M':'D'}, {'M':'A', 'I':'B', 'R':'C' ,'P':'D'}, {'P':'A', 'R':'B', 'M':'C' ,'I':'D'},{'R':'A', 'I':'B', 'P':'C' ,'M':'D'}]
    resp_dict = resp_dict[session-1]
    resp_dict_invert = dict([(v, k) for k, v in resp_dict.iteritems()])

    #for practice use this mapping
    pilot_comp_mapping = {2:'h', 3:'j', 4:'k', 5:'l'}
    #Practice trial handle
    this_practice_dict = {key_map[key]: img_dict[resp_dict[key]] for key in key_map.keys()}
    print this_practice_dict
    df_practice = {'cor_ans':this_practice_dict.keys(),'img_id': this_practice_dict.values()}
    df_practice = pd.DataFrame(data=df_practice)
    df_practice = df_practice[['img_id', 'cor_ans']]
    print df_practice
    df_practice = df_practice.replace({'cor_ans':pilot_comp_mapping})
    practiceOnsets_fn =  _thisDir + os.sep + 'data/%s_pilot_session_%s.csv' %(expInfo['participant'], str(session))
    df_practice.to_csv(practiceOnsets_fn, index=False)

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
    mapping = {'h': 'Index ', 'j': 'Middle ', 'k': 'Ring ', 'l':'Little '}
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
    start_time = time.time()

    delay = 1
    for thisPractice_loop in practice_loop:

        if n_practice_trials % 4 == 0:
            core.wait(delay)

        #%Check if threshold performance has been met.
        n_practice_trials +=1
        current_acc = (sum(running_accuracy[-20:])/20.0)
        if n_practice_trials > 80 and current_acc > .90:
            end_time = time.time() - start_time
            data_out.loc[len(data_out)+1]=[n_practice_trials,current_acc, end_time]
            data_out.to_csv(out_all_fn, index=False)
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
        Practice_response = event.BuilderKeyResponse()
        Practice_response.status = NOT_STARTED
        practiceComponents = []
        practiceComponents.append(image)
        practiceComponents.append(Practice_response)
        practiceComponents.append(Wrong_1)
        practiceClock.reset()

        for thisComponent in practiceComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED


        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
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
                theseKeys = event.getKeys(keyList=['2', '3', '4', '5','h', 'j', 'k', 'l'])

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if Practice_response.keys == []:
                        Practice_response.keys = theseKeys[0]
                        Practice_response.rt = Practice_response.clock.getTime()

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
        win.flip()

    #Add pause here:
    t = 0
    InstructionsClock.reset()  # clock
    frameN = -1
    routineTimer.add(5.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    InstructionsComponents = []
    InstructionsComponents.append(pause_after_block)
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    event.clearEvents(eventType='keyboard')

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

    #Clear events of type keyboard so that next block doesn't immediately advance.
    event.clearEvents(eventType='keyboard')



### End of practice, wait 10 second befor continuing.
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
