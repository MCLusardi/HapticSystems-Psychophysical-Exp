"""measure your JND in orientation using a staircase method"""
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import numpy, random
from numpy.random import shuffle
import copy #from the std python libs

""" GLOBAL VARIABLES: need to determine day of experiment"""
stairSettings={
    'nReversals':10, 
    'nUp':1, 'nDown':2, 
    'stepType':'lin', 
    'minVal':0, 'maxVal':2.5, 
    'stepSizes':[1.5, 1.0, 1.0, 0.5]
}

conditions=[
    {'label':'high', 'startVal':2, **stairSettings},
    {'label':'low', 'startVal':0.5, **stairSettings},
]

print(conditions)

stairs = data.MultiStairHandler(conditions=conditions, nTrials=10)

try:  # try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:  # if not there then use a default set
    expInfo = {'pilotOrMainStudy':'jwp', 'participantNo':0, 'reference':0}
expInfo['dateStr'] = data.getDateStr()  # add the current time
# present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='JND Exp', fixed=['dateStr'])
if dlg.OK:
    toFile('lastParams.pickle', expInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit

# make a csv file to save data
fileName = (expInfo['pilotOrMainStudy'] 
    + "-p" + str(expInfo['participantNo']) 
    + "-ref" + str(expInfo['reference']) 
    + "-" + expInfo['dateStr'])

dataFile = open(fileName+'.csv', 'w')  
dataFile.write('targetSide,staircase,WidthDiff,correct\n') 

# create window and stimuli
win = visual.Window([800,600],allowGUI=True,
                    monitor='testMonitor', units='deg')
# instead of stimuli, need it to say what measurements should be on the left or right
# only the experimenter is viewing the screen
comparison = visual.TextStim(win, color='white')
reference = visual.TextStim(win, color='white', text="%d mm" %expInfo['reference'])

# display instructions and wait
message1 = visual.TextStim(win, pos=[0,+3],text='Hit a key when ready.')
message2 = visual.TextStim(win, pos=[0,-3],
    text="Then press left or right to identify the narrower stimulus")
message1.draw()
message2.draw()
win.flip()
#pause until there's a keypress
event.waitKeys()

for thisDiff, thisCondition in stairs:  # will continue the staircase until it terminates!
    print('start=%.2f, current=%.4f' %(thisCondition['startVal'], thisDiff))
    
    # set location of stimuli
    referenceSide= random.choice([-1,1])  # will be either +1(right) or -1(left)
    comparison.setPos([-5*referenceSide, 0])
    reference.setPos([5*referenceSide, 0])  # in other location


    # set width of comparison
    thisDirection = random.choice([-1,1])  # will be either +1 or -1
    comparisonValue = expInfo['reference'] + thisDiff*thisDirection
    comparisonText = f"{comparisonValue} mm"
    comparison.setText(comparisonText)

    # set which side the narrower stimulus is on
    targetSide = referenceSide if expInfo['reference'] < comparisonValue else -1*referenceSide

    # draw all stimuli
    comparison.draw()
    reference.draw()
    win.flip()

    # get response - need to fix this logic
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey=='left':
                if targetSide==-1: thisResp = 1  # correct
                else: thisResp = -1              # incorrect
            elif thisKey=='right':
                if targetSide== 1: thisResp = 1  # correct
                else: thisResp = -1              # incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
        event.clearEvents()  # clear other (eg mouse) events - they clog the buffer

    # add the data to the staircase so it can calculate the next level
    stairs.addResponse(thisResp)
    dataFile.write('%i,%s,%.3f,%i\n' %(targetSide, thisCondition['label'], thisDiff, thisResp))
    core.wait(1)

# staircase has ended
dataFile.close()
stairs.saveAsPickle(fileName)  # special python binary file to save all the info

# give some on-screen feedback
feedback1 = visual.TextStim(
        win, pos=[0,+3],
        text='You made it to the end!\n\n')

feedback1.draw()
win.flip()
event.waitKeys()  # wait for participant to respond

win.close()
core.quit()