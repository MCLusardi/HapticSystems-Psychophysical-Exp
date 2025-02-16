from psychopy.misc import fromFile
from psychopy import gui, core

# (replace with the file path to your .psydat file)
#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

for fName in files:
    psydata = fromFile(fName)
    psydata.printAsText()
    # for entry in psydata.entries:
    #     print(entry)