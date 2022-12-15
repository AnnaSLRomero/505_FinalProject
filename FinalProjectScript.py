# 505_FinalProject
## By: Anna Romero

#This is testing item recognition memory. Participants are shown 10 images in the beginning of the #block. Afterwards, they are tested on all the images plus 5 new images. They are to press 1 if they #saw the image before ("old" condition) and they have to press 2 if was not presented earlier ("new" #condition). Therefore, overall there are 15 images during testing.

#The stimuli I am using are screenshots of the unity assets we are currently using in our VR videos. #We want to test item recognition for objects we have created in our scenes and I wanted to see if we #could do this through psychopy. I have 2 blocks here, just for the class, but I think for us we will #just have 1 block.

#The images are to be presented for 1500 msecs or 1.5 seconds during the presentation stage. During #testing, the image will stay up until "1" or "2" are pressed.

#In the csv file that is created at the end records the SubjectID, experimenter initials, Block #Number, Trial number, acuuracy, and response times.



#=====================
#IMPORT MODULES
#=====================
#-import numpy and/or numpy functions *
import numpy as np
#-import psychopy functions
from psychopy import core, gui, visual, event, monitors, logging
#-import file save functions
import json
import pandas as pd
#-(import other functions as necessary: os...)
import os
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
#-define the main directory where you will keep all of your experiment files
main_dir = os.getcwd()
print(main_dir)
#-define the directory where you will save your data
data_dir = os.path.join(main_dir,'data')
#-if you will be presenting images, define the image directory
image_dir = os.path.join(main_dir,'images')
print(image_dir)
path = os.path.join(main_dir, 'dataFiles')


#=====================
#COLLECT PARTICIPANT INFO
#=====================
#-create a dialogue box that will collect current participant number, age, gender, handedness
exp_info = {'SubjectID':(), 'Experimenter':()} #dictionary

my_dlg = gui.DlgFromDict(dictionary=exp_info, title = "subject info")

#get date and time
date = datetime.now()
exp_info['date'] = str(date.day) + "-" + str(date.month) + "-" + str(date.year)

#-create a unique filename for the data
filename = str(exp_info['SubjectID']) + '_' + exp_info['date'] + '.csv'
print(filename)
main_dir = os.getcwd()
sub_dir = os.path.join(main_dir,'sub_info',filename)

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
#-number of trials and blocks *
nTrials = 15
nPresent = 10
nBlocks = 2
totalTrials = nTrials*nBlocks
nEach = int(totalTrials/2)

#-stimulus names (and stimulus extensions, if images) *
old = ['old1.png', 'old2.png', 'old3.png', 'old4.png', 'old5.png',
         'old6.png', 'old7.png', 'old8.png', 'old9.png', 'old10.png']
new = ['new1.png','new2.png', 'new3.png', 'new4.png', 'new5.png']

test = ['old1.png', 'old2.png', 'old3.png', 'old4.png', 'old5.png',
         'old6.png', 'old7.png', 'old8.png', 'old9.png', 'old10.png',
         'new1.png','new2.png', 'new3.png', 'new4.png', 'new5.png']


#-start message text *
start_msg = "Welcome to the experiment, press any key to begin"
presentStart_msg = "You will be shown images at the middle of the screen after a fixation cross."
presentEnd_msg = "Press any key to begin the testing"
testStart_msg = "You will be shown images at the middle of the screen after a fixation cross. You will judge whether it was presented to you earlier. If it was presented to you earlier press 1 in the keyboard, if it was not presented to you earlier press 2 in the keyboard. Press any key to begin."
testEnd1_msg = "Press any key to move to the next block"
testEnd2_msg = "Press any key to end the experiment"

#=====================
#PREPARE CONDITION LISTS
#=====================
#-create counterbalanced list of all conditions *
np.random.shuffle(old)
np.random.shuffle(test)

#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
condition = [0]*totalTrials
accuracies = [0]*totalTrials
responseTimes = [0]*totalTrials
trialNumbers = [0]*totalTrials
blockNumbers = [0]*totalTrials

#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
#-define the monitor settings using psychopy functions
mon = monitors.Monitor('myMonitor', width = 30.41, distance = 60)
mon.setSizePix([2500, 1600])

#-define the window (size, color, units, fullscreen mode) using psychopy functions
win = visual.Window(monitor=mon, 
                    color = "grey",
                    fullscr = True)

#-define experiment start text using psychopy functions
start_text = visual.TextStim(win, text = start_msg)

#-define block (start)/end text using psychopy functions
fixation = visual.TextStim(win, text='+', color='black')
presentStart_text = visual.TextStim(win, text = presentStart_msg)
testStart_text = visual.TextStim(win, text = testStart_msg)
instructText = visual.TextStim(win, text = 'Press any key to begin Block ')

#-define stimuli using psychopy functions
fix_text = visual.TextStim(win, text = "+")
my_image = visual.ImageStim(win, units = "pix", size = (400, 400))

#-create response time clock
trial_timer = core.Clock()

#=====================
#START EXPERIMENT
#=====================
#-present start message text
start_text.draw()
win.flip()
#-allow participant to begin experiment with button press
event.waitKeys()

for iblock in range(nBlocks):
    #shows the text and changes the block number in the text depending on the block
    presentStart_text.draw()
    win.flip()
    core.wait(2)
    instructText.text = 'Press any key to begin Block ' + str(iblock+1)
    instructText.draw()
    #shows the window and waiting for keypress
    win.flip()
    event.waitKeys()
    
    for iPresent in range(nPresent):
        fixation.draw()
        win.flip()
        core.wait(.5)
        
        my_image.image = os.path.join(image_dir, old[iPresent])
        my_image.draw()
        win.flip()
        core.wait(1.5)
        
        if iPresent == 9:
            testStart_text.draw()
            win.flip()
            event.waitKeys()
            
    for itrial in range(nTrials):
        overallTrial = iblock*nTrials + itrial
        blockNumbers [overallTrial] = iblock + 1
        trialNumbers[overallTrial] = itrial + 1
        trial_timer.reset()
         
        fixation.draw()
        win.flip()
        core.wait(.5)
        my_image.image = os.path.join(image_dir, test[itrial])
        my_image.draw()
        win.flip()
        keys=event.waitKeys(keyList=['1', '2'])
                
        if keys:
            responseTimes[overallTrial] = trial_timer.getTime() 
            if test[itrial][0] == 'o':
                if keys[0] == '1':
                    accuracies[overallTrial] = 'Correct'
                else:
                    accuracies[overallTrial] = 'Incorrect'
            else:
                if keys[0] == '2':
                    accuracies[overallTrial] = 'Correct'
                else: 
                    accuracies[overallTrial] = 'Incorrect'
    
#print out Block, Trial, Color, Accuracy (correct or incorrect), and RT of current trial
        print(
         ', Trial:', 
         itrial+1, 
         ',', 
         test[itrial][0], 
         ':', 
         accuracies[overallTrial], 
         ', RT:', 
         responseTimes[overallTrial],
         ',',
         keys[0]
        )

#create a data frame from a dictionary of collected data then make it to csv file)
df = pd.DataFrame(data={
 "SubjectID" : exp_info["SubjectID"],
 "Experimenter" : exp_info["Experimenter"],
 "Block Number": blockNumbers,
 "Trial Number": trialNumbers, 
 "Accuracy": accuracies, 
 "Response Time": responseTimes,
})
df.to_csv(os.path.join(path, filename), sep=',', index=False)
#
#close the window and end experiment
win.close()