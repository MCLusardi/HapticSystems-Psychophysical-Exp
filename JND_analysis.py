#This analysis script takes one or more staircase datafiles as input
#from a GUI. It then plots the staircases on top of each other on 
#the left and a combined psychometric function from the same data
#on the right

from psychopy import data, gui, core
from psychopy.tools.filetools import fromFile
import pylab
import numpy

#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses, allReversals = [],[], []
for thisFileName in files:
    thisDat = fromFile(thisFileName)
    # print(type(thisDat))
    theseStairs = thisDat.staircases
    # print(type(theseStairs))
    # print(type(theseStairs[0]))
    for stair in theseStairs:
        allIntensities.append( stair.intensities)
        # print(allIntensities)
        allResponses.append( stair.data )
        # print(allResponses)
        allReversals.append( stair.reversalIntensities[-6:] )
        print(allReversals)

#Calculate mean and standard deviation of the thresholds based on the reversals
approxThreshold = numpy.average(allReversals)
print('approxThreshold', approxThreshold)
stdThreshold = numpy.std(allReversals)
print('stdThreshold', stdThreshold)
    
#plot each staircase
pylab.subplot(121)
pylab.suptitle('Approximate threshold = %0.3f mm' %(approxThreshold))
pylab.title('std = %0.3f' %(stdThreshold))
colors = 'brgkcmbrgkcm'
lines, names = [],[]
for stairNo, thisStair in enumerate(allIntensities):
    # print(stairNo)
    # print('thisStair', thisStair)
    # lines.extend(pylab.plot(thisStair))
    #names = files[fileN]
    pylab.plot(thisStair, label=stairNo)
#pylab.legend()

#get combined data
#Need to replace -1 with 0 to match what functionFromStaircase expects
for stairNo, thisStair in enumerate(allResponses):
    allResponses[stairNo] = [0 if x == -1 else x for x in thisStair]
    print(allResponses[stairNo])
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, bins='unique')

# print(combinedInten)
# print(combinedResp)
# print(combinedN)
#fit a sigmoid function to the intensity and percent correct
fit = data.FitLogistic(combinedInten, combinedResp)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.5)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.71)
print(thresh)

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt, smoothResp, '-')
pylab.plot([thresh, thresh],[0,0.8],'--'); pylab.plot([0, thresh],\
[0.8,0.8],'--')
pylab.title('threshold = %0.3f' %(thresh))
#plot points
pylab.plot(combinedInten, combinedResp, 'o')
pylab.ylim([0,1])

pylab.show()