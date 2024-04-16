
import array
from ast import Num
import os
from stat import UF_APPEND
import subprocess
import shutil
import wave
import contextlib
import audioread
import tkinter as tk #used for GUI
from tkinter import ttk
from tkinter import * #imports the slider
import pydub
from pydub import AudioSegment
from scaler_gan import inference




global menu
global selectedDuration



#Initializes variables used in SelectedAudio()
selectedDuration = 0
durationScaleFactor = []
durationTable = []
scale1 = 0
scale2 = 0
scale3 = 0

#Holds the Final Filenames and Durations used in the Complete Segment
finalFiles = []
finalScales = []
lowerDuration = []
upperDuration = []
sortedArrayLower = []
sortedArrayHigher = []
#Sets up the Window
root = tk.Tk()
root.title("Audio Editor") #names the GUI
root.geometry("500x500")  # Sets the window dimensions (width x height)
root.minsize(500,500)
root.maxsize(800,700)


########################################################################### 
###########################################################################    
###      SelectedAudio()                                                ###
###      Calls Inference.py and merges all wavefiles                    ###
###      finalFiles[] holds  the .wav files in order of time            ###
###      finalScales[] holds the scaling factors in order of time       ###      
###########################################################################    
###########################################################################  

def completedAudio():
    newarray = []
    #Loop to call Inference Py for all instances of selection
    for k in range(0,len(finalFiles)):    
            with open(inferenceTextFile + "inference.txt", "w") as output_file:
               output_file.write('data\Project' + "\\" + str(finalFiles[k]))
            command = ['python', 'scaler_gan/inference.py', '--infer_scales', finalScales[k]]
            subprocess.run(command)
            command2 = ['python', 'inference_e2e.py', '--checkpoint_file', 'generator_v2']
            subprocess.run(command2, cwd= 'hifi_gan')
            
            removefileDirectory = currentDirectoryPath + '/hifi_gan/test_mel_files'
            removefiles = os.listdir(removefileDirectory)
            for removefile in removefiles:
               file_path = os.path.join(removefileDirectory, removefile)
               os.remove(file_path)

            for completedFile,_,Files in os.walk(currentDirectoryPath + '/hifi_gan/generated_files_from_mel'):              #Loop gets all of the .wav files stored in the data Folder and stores the file paths in wavFiles[] and stores the names in Filenames
               for Filename in Files:
                  if Filename.lower().endswith(".wav"):
                     print(currentDirectoryPath + '/hifi_gan/generated_files_from_mel' + Filename)
                     print(currentDirectoryPath + '/data' + "//" + finalFiles[k])
                     shutil.move(currentDirectoryPath + '/hifi_gan/generated_files_from_mel/' + Filename, currentDirectoryPath + '/data/Project' + "//" + finalFiles[k])
   
   

    unscaledWaves = []
    totalSound = AudioSegment.empty()
    if (sortedArrayLower[0] != 0):
        temp = AudioSegment.from_file(selectedFilePath, format = "wav")
        newWave = temp[0:int(sortedArrayLower[0])*1000]
        unscaledWaves.insert(0,newWave)
        totalSound = unscaledWaves.pop(0)
    for t in range(0,len(sortedArrayLower)):
        if (t+1 == len(sortedArrayLower)) and (selectedDuration != sortedArrayHigher[t]):
           temp = AudioSegment.from_file(selectedFilePath, format = "wav")
           newWave = temp[int(sortedArrayHigher[t])*1000:selectedDuration*1000]
           unscaledWaves.insert(t,newWave)

        else:
           temp = AudioSegment.from_file(selectedFilePath, format = "wav")
           newWave = temp[int(sortedArrayHigher[t])*1000:int(sortedArrayLower[t+1])*1000]
           unscaledWaves.insert(t,newWave)
        
    if len(finalFiles) > len(unscaledWaves):
       arrayLength = len(finalFiles)
    else: 
       arrayLength = len(unscaledWaves)
    
    sounds = []
    
   #Merge all Wav Files 
    for j in range(0,arrayLength):
      sound1= AudioSegment.from_file(wavFileLocation + "\\" + finalFiles[j],format = "wav")
      totalSound += sound1 
      totalSound += unscaledWaves[j]
    totalSound.export(wavFileLocation + "\\New_" + selected, format = "wav")
    newLabel = Label(root, text = "File Complete").pack()
    
   
   
 
########################################################################### 
###########################################################################    
###      Sort()                                                         ###
###      Sorts the times in lowerDuration, so that the final arrays are ###
###      in sequential order.                                           ###
###      finalFiles[] holds  the .wav files in order of time            ###
###      finalScales[] holds the scaling factors in order of time       ###      
###########################################################################    
###########################################################################  

def sort(lowerDuration,lower,upper,scale3):
   arrayLength = len(sortedArrayLower)
  
   for r in range(0,arrayLength):
      if int(lower) <= sortedArrayLower[r]:
         finalFiles.insert(r,str(lower) + "_" + str(upper) + selected)
         sortedArrayLower.insert(r,int(lower))
         sortedArrayHigher.insert(r,int(upper))
         finalScales.insert(r,scale3)
         break
      elif r+1 == arrayLength:
         finalFiles.insert(r+1,str(lower) + "_" + str(upper) + selected)
         sortedArrayLower.insert(r+1,lower)
         sortedArrayHigher.insert(r+1,upper)
         finalScales.insert(r+1,scale3)
   
   if (arrayLength == 0):
      finalFiles.insert(0,str(lower) + "_" + str(upper) + selected)
      sortedArrayLower.insert(0,int(lower))
      sortedArrayHigher.insert(0,int(upper))
      finalScales.insert(0,scale3) 
   
   

########################################################################### 
###########################################################################    
###      SelectedAudio()                                                ###
###      Determines the selected duration to edit, the selected file,   ###
###      creates a new wave file, and writes that to the inference.txt  ###
###      checks to make sure that the time period has not  been edited  ###
###      sorts out which time period is lower                           ###
###      durationTable[] holds the selected time period (lower,higher)  ###
###      wavFile is the new audio file                                  ###
###      durationScalingFactor[] holds the scaling factor               ###
###########################################################################    
###########################################################################  
   


def selectedAudio():
   global durationTable
   durationFound = False
   commitedText = " "
   #Stores the Commited duration edits in the correct order
   if float(scale1) > float(scale2):
      lower = scale2
      upper = scale1
   else:
      lower = scale1
      upper = scale2
   
   arraySize = len(durationTable)
   i=0
   #Checks to make sure any edits have been committed 
   if(arraySize > 0):
      #for i in range(0,arraySize):
     while(durationFound == False):
         #checks  to make sure that the user hasnt tried to edit this time segmnet yet 
          if ((int(upper) > int(durationTable[i])) and(int(upper) < int(durationTable[i+1]))) or ((int(lower) >int(durationTable[i])) and (int(lower) < int(durationTable[i+1]))):
             commitedText = "Error timestamp already used"
             durationFound = True
             break
          i+=2 #increments to next time band
          if(i >= arraySize):
             break
      
   
  
  #if the time band has not been edited yet
   if (durationFound == False):
      durationTable.append(lower) #inserts lower bound
      lowerDuration.append(lower)
      
      durationTable.append(upper) #inserts upper bound
      upperDuration.append(upper)
      durationScaleFactor.append(scale3) #inserts the scaling factor for the accepted time period
      wavFile = AudioSegment.from_file(selectedFilePath, format = "wav")
      scaledWavFile = wavFile[int(lower)*1000:int(upper)*1000]
      scaledWavFile.export(wavFileLocation + "\\" + str(lower) + "_" + str(upper) + selected, format = "wav")
      commitedText = ("Adjusting time between: " +str(lower) + " and " + str(upper))
      commitedNoteLabel = Label(root,text=commitedText).pack()
      
      #Sort the files by time 
      sort(lowerDuration,lower,upper,scale3)
      #with open(inputTextFile,"a") as output_file:
         #output_file.write("\n" + 'data\Project' +  "\\" + str(lower) + "_" + str(upper) + selected)

         
      
   


      
########################################################################### 
###########################################################################    
###      Sets up all scales                                             ###
###                                                                     ###
###########################################################################    
###########################################################################  

flag = False #initializes flag to false which is used in scale3Adjustment 
   
#sets the lower duration value
def scale1Adjustment(value):
   global scale1
   scale1 = value

#sets the upper duration value
def scale2Adjustment(value):
   global scale2
   scale2 = value
   
#sets the scaling value
def scale3Adjustment(value):
   global scale3
   global flag
   scale3 = format(float(value),'.2f')
   if (flag == True):
      labelRemove()
   scale3Value(scale3)
   flag = True #sets the flag to true, so that it can remove the scaling label in the future

#Prints the Scaling Factor Value to the GUI
def scale3Value(value):
    global selectedDurationLabel6
    selectedDurationLabel6 = Label(root,text="Scaling Factor: " + value)
    selectedDurationLabel6.pack()
   

#Removes excess labels of the Scaling Factor
def labelRemove():
   global selectedDurationLabel6
   selectedDurationLabel6.pack_forget()  
   


############################################################################################ 
############################################################################################    
###         Sets the main menu GUI with sliders and buttons                              ###
###         Scale1 is for the Lower Duration Slider                                      ###
###         Scale2 is for the Upper Duration Slider                                      ###
###         Scale3 is for the Scaling Factor Slider                                      ###                                      
############################################################################################    
############################################################################################


   
#Main GUI which controls the time stamps that one uses 
def select(event):
   global selectedFilePath
   global selected
   selected = selectedFile.get()
   menu.destroy()   #Erases the initial GUI to create a new frame for the user to select
   
   selectedFileLabel = tk.Label(root,text=selected).pack()
   #grabs the duration associated with the specific .wav file
   for i in range(0,totalNumFiles):
      if (selected == filenames[i]):
         global selectedDuration
         selectedDuration = waveFileDuration[i] 
         selectedFilePath = waveFiles[i]
         
   #Sets up a new GUI 
   newMenu = Frame(root)
   newMenu.pack()
   selectedDurationLabel = tk.Label(newMenu,text="Time Stamp Runs from 0 seconds to " + str(selectedDuration) + " seconds.\n Adjust lower duration and upper duration sliders to enter time period.\n Adjust Scaling Factor slider to set how much to adjust time period.").pack()
   
   selectedDurationLabel3 = tk.Label(newMenu,text="Enter the Time to Adjust: (Lower Duration Upper Duration").pack()

   #Scale 1  
   selectedDurationLabel4 = tk.Label(newMenu,text="Lower Duration Slider").pack()
   slider1 = tk.Scale(newMenu, orient = 'horizontal', from_=0, to=selectedDuration,command=scale1Adjustment)
   slider1.pack()


   #Scale 2
   selectedDurationLabel5 = tk.Label(newMenu,text="Upper Duration Slider").pack()
   slider2 = tk.Scale(newMenu,orient = 'horizontal',from_=0, to=selectedDuration,command=scale2Adjustment)
   slider2.pack()
   

   #Scale 3
   slider3 = ttk.Scale(newMenu,orient = 'horizontal',from_=0, to=10,command = scale3Adjustment)
   slider3.pack()



   commitedEditButton = Button(newMenu, text = "Commit Changes", command = selectedAudio).pack()
   finalizeEditsButton = Button(newMenu, text = "Complete Edits", command = completedAudio).pack()





      
############################################################################################ 
############################################################################################    
###         Sets Up Initial Settings and variables                                       ###
###         waveFileDuration[] holds the lengths of each audio file in the data folder   ###
###         filenames[] holds the names of each .wav file in the data folder             ###
###         waveFiles[] holds the file paths of each .wav file in the data folder        ###
###         selectedFile holds the file that the user wants to edit                      ###                                        
############################################################################################    
############################################################################################



inferenceTextPath = '\data\inference.txt'  #Gets file path for Inference.txt file that holds all .wav files
dataFilePath = '\data\Project'                     #gets the file path for the data folder 
currentDirectoryPath = os.path.dirname(__file__)           #Gets the current directory's file path

inputTextFile = currentDirectoryPath + inferenceTextPath   #Sets up path for Inference.txt file
wavFileLocation = currentDirectoryPath + dataFilePath      #sets up path for all .wav files
inferenceTextFile = currentDirectoryPath + '\data' + '\\'
totalNumFiles = 0                                          #initializes the variable that holds the total number of .wav  files
waveFiles = []                                             #initializes an array to store .wav Files
filenames = []                                             #initializes an array to storethe filenames   


for file,_,files in os.walk(wavFileLocation):              #Loop gets all of the .wav files stored in the data Folder and stores the file paths in wavFiles[] and stores the names in Filenames
      for filename in files:
         if filename.lower().endswith(".wav"):
            totalNumFiles +=1
            waveFiles.append(wavFileLocation + "\\" + filename) 
            filenames.append(filename)
             



waveFileDuration = []                                      #Initializes an array to hold the duration of each audio file

for i in range(0,totalNumFiles):                           #Loop gets all of the lengths of each .wav File and stores them in waveFileDuration[]
  with audioread.audio_open(waveFiles[i]) as output_file:
    totalTime = output_file.duration
    waveFileDuration.append(totalTime)
    

    

menu = Frame(root)                                         #Creates the Menu Window
menu.pack()
label = tk.Label(menu, text="Pick the Audio File to select").pack()

selectedFile = StringVar(menu)                            #Holds the file that the user picked
selectedFile.set(filenames[0])
dropdown = OptionMenu(menu,selectedFile,*filenames,command=select).pack(pady=20)

















# Enter the main event loop
root.mainloop()





