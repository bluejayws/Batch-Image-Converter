import PySimpleGUI as sg
import urllib.request
import sys
from urllib.error import HTTPError
import random

#Functions for layouts
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
            [sg.Text('3: convert images in folder to .png')]]

layout2 = [[sg.Text('(Choose source file to batch download')],
            [sg.Text('Source file: ')],
            [sg.In(), sg.FileBrowse()]]

layout3 = [[sg.Text('This is the convert folder to .png')]]

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
    elif event in '123':
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)

window.close()
