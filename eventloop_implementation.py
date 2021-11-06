import PySimpleGUI as sg
import sys
import urllib
import random
import os
import array
from urllib.error import HTTPError
from PIL import Image

#Functions for layout2
#------------------------------------------------------------------------------#
#Reads a text file with links in them, one link per line.
#Returns a list with these links
def parse_links_text(text_source):
    text_list_file_reader = open(text_source,'r')
    return text_list_file_reader.readlines()

#Returns a name for a given photo number and folder location
#Adds a randomized number + IMG to the file name
def randomizedFileName(image_num, saveFolder):
    # "foto#3.jpg" for example
    #return saveFolder+"\\"+"foto#"+str(image_num)+".jpg"

    #"IMG_6813" for example
    return saveFolder + "\\" + "IMG_" + str(random.randint(1111,9999)) + ".jpg"

def concatenate_link(link):
    return "" + link

#------------------------------------------------------------------------------#


sg.theme('BluePurple')

#Main layout
layout1 = [[sg.Text('1: Home')],
            [sg.Text('2: Batch download Images from .txt file')],
            [sg.Text('3: Convert images in folder to .png')]]

layout2 = [[sg.Text('In the pop up window, provide a path to a .txt file, and a destination folder to save your images in')]]

layout3 = [[sg.Text('Select a folder of images to automatically convert them all to PNG')]]

#------------------------------------------------------------------------------#

#layout1 is batch download from a .txt file
#layout2 is convert all images in a folder to .png
layout = [[sg.Column(layout1, key='-COL1-'),
            sg.Column(layout2, visible=False, key='-COL2-'),
            sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Button('1'), sg.Button('2'), sg.Button('3') ,sg.Button('Exit')]]

#Name of window
window = sg.Window('🐍📸PIT🔨🗂', layout)

#------------------------------------------------------------------------------#

layout = 1  # The currently visible layout

while True:
    event, values = window.read()
    print(event, values)

    if event in (None, 'Exit'):
        break
    elif event in '1':
        #Set current column-view to invisible
        window[f'-COL{layout}-'].update(visible=False)
        #Update layout value
        layout = int(event)
        #Set new corresponding column-view layout
        window[f'-COL{layout}-'].update(visible=True)
    elif event in '2':
        # Having lots of trouble with this; switching to mac is my problem?
        # Images download multiple times
        # Images saved with file name prefixed to desired name
        # Change: Just provide the text file and have it download in the containing folder.
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)

        if len(sys.argv) == 1:
            event, values = sg.Window('.txt Batch Image Downloader',
                                  [ [sg.Text('(Choose source folder, or source file, but not both)')],
                                    [sg.Text('Source file: ')],
                                    [sg.In(), sg.FileBrowse()],
                                    [sg.Text('Output folder: ')],
                                    [sg.In(), sg.FolderBrowse()],
                                    [sg.Open(), sg.Cancel()]]).read(close=True)
            fname = values[0]
        else:
            fname = sys.argv[1]

        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:
            #------------------------------.txt batch downloader---------------#
            textFileName = fname
            saveFolder = values[1]

            # Debugging print statements
            ## TODO: Test what these parameters are when providing only a text file, vs a folder source. Add an if statement accordingly.
            print(fname)
            print(saveFolder)
            #print(saveFolder)

            #If text file provided, we are doing a batch download
                #Get links as a list
            list_of_links = parse_links_text(textFileName)
                #Find and downloader image links
            image_num = 1;
            for link in list_of_links:
                    if not link or link.startswith('#'):
                        continue
                    try:
                        urllib.request.urlretrieve(concatenate_link(link), randomizedFileName(image_num, saveFolder))
                        image_num += 1
                    except HTTPError as httperr:
                        if httperr.code == 404:
                            print(concatenate_link(link) + " not downloaded! 404 Error for the link")
                        #elif httperr.code ==
                    urllib.request.urlretrieve(concatenate_link(link), randomizedFileName(image_num,saveFolder))
                    image_num += 1

                    #Inteprets empty space as a link...how to avoid?

                #------------------------------.txt batch downloader---------------#

    elif event in '3':
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)

        #Select a folder.
        #For each file in that folder
            #convert it to png
        if len(sys.argv) == 1:
            event, values = sg.Window('Convert Folder to PNG',
                            [[sg.Text('Folder of unconverted images:')],
                            [sg.In(), sg.FolderBrowse()],
                            [sg.Open(), sg.Cancel()]]).read(close=True)
            fname = values[0]
        else:
            fname = sys.argv[1] #The location of the folder

        if not fname:
            sg.popup("Cancel", "No filename supplied")
            raise SystemExit("Cancelling: no filename supplied")
        else:

            #sg.popup('The filename you chose was', fname)
            #get list of image file names (X)
            # create a folde for the converted images (x)
            #for each image in the list of image file names
                #Convert it
                #save it in the new Folder

            path = fname + "/Converted_Images"
            print(path)
            print("--------")
            #os.mkdir(path, exist_ok=True)
            os.makedirs(path, exist_ok=True)
            imageList = []

            for root, dirs, files in os.walk(fname, topdown=True):
                for filename in files:
                     if '.jpg' in filename:
                        print(fname+filename)
                        imageList.append(fname+filename)

            cwd = os.getcwd()  # Get the current working directory (cwd)
            files = os.listdir(cwd)  # Get all the files in that directory
            print("Files in %r: %s" % (cwd, files))


            for img in imageList:
                print(img)
                absolutePathJpg = os.path.abspath(img)
                print(absolutePathJpg)
                img = Image.open(absolutePathJpg)
                #img = Image.open("/Users/antoniogurrola-beltran/Desktop/TEST BATCH DOWNLOAD/TEST DESTINATION FOLDERTEST DESTINATION FOLDER/IMG_6409.jpg")

                #img = Image.open(absolutePathJpg)
                #absolutePathPng = os.path.abspath(path)
                #img.save()
                print("_____________")



#            if '.jpg' in filename:
#                absolutePath = fname+filename
#                print(fname+filename)
#                f = open(fname+filename)
#                converted = Image.open(f)
                #im1.save(path)



window.close()
