
from psychopy import data, gui, core
import csv
import pylab
from scipy.optimize import curve_fit
import numpy as np

#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

exp_data = []
allIntensities, allResponses = [],[]
for thisFileName in files:
    with open(thisFileName, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for i, row in enumerate(reader):
            width_diff = float(row[2])
            correct = int(row[3])
            exp_data.append({'index': i+1, 'targetSide': int(row[0]), 'staircase': row[1], 'WidthDiff': width_diff, 'correct': correct})
            allIntensities.append(width_diff)
            allResponses.append(0 if correct == -1 else correct)

# Separate data by staircase
groups = {}
for entry in exp_data:
    if entry['staircase'] not in groups:
        groups[entry['staircase']] = []
    groups[entry['staircase']].append(entry)

# Plot each staircase
for name, group in groups.items():
    indices = [entry['index'] for entry in group]
#    print(indices)
    width_diffs = [entry['WidthDiff'] for entry in group]
    pylab.subplot(121)
    pylab.hlines(width_diffs, [i - 1 for i in indices], indices, label=name, color = 'red' if name == 'low' else 'blue')

    for i, (x, y) in enumerate(zip(indices, width_diffs)):
        offset = 0.05 if i % 2 == 0 else -0.05
        pylab.text(x - 0.5, y + offset, str(x), ha='center', va='center', fontsize=8, color='black')

pylab.xlabel('Trial Number')
pylab.gca().set_xticklabels([])
pylab.ylabel('Width Difference')
pylab.title('Interlaced Sequences')
pylab.legend(loc='best')

combinedInten, combinedResp, combinedN = data.functionFromStaircase(allIntensities, allResponses, bins='unique')
             
#fit a sigmoid function to the intensity and percent correct
def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)

p0 = [max(combinedResp), np.mean(combinedInten),1,min(combinedResp)] # init guess

popt, pcov = curve_fit(sigmoid, combinedInten, combinedResp,p0, method='dogbox')

# Points for plotting  curve
x_fit = np.linspace(min(combinedInten), max(combinedInten), 1000)
y_fit = sigmoid(x_fit, *popt)

# Plot the data and the fitted sigmoid curve
pylab.subplot(122)
pylab.plot(combinedInten, combinedResp, 'o', label='Data', color='black')
pylab.plot(x_fit, y_fit, '-', label='Fitted sigmoid', color='red')
pylab.xlabel('Intensity (WidthDiff)')
pylab.ylabel('Percent Correct')
pylab.title('Sigmoid Fit to Intensity vs Percent Correct')
pylab.legend()
pylab.show()
