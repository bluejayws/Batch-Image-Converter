#
#@author agbjr
#
#
#ToDo: Add an option to convert images in a folder to a different image file type
#

import urllib.request
import PySimpleGUI as sg
import sys
from urllib.error import HTTPError
import random

#Reads a text file with links in them, one link per line.
#Returns a list with these links
def parse_links_text(text_source):
    text_list_file_reader = open(text_source,'r')
    return text_list_file_reader.readlines()

#Returns a name for a given photo number and folder location
def concatenateFileName(image_num, saveFolder):
    # "foto#3.jpg" for example
    #return saveFolder+"\\"+"foto#"+str(image_num)+".jpg"

    #"IMG_6813" for example
    return saveFolder + "\\" + "IMG_" + str(random.randint(1111,9999)) + ".jpg"

def concatenate_link(link):
    return "" + link


if __name__ == '__main__':
    sg.theme('DarkPurple3')
    #Get parameters
    if len(sys.argv) == 1:
        event, values = sg.Window('Photo Batch Downloader v1 :)',
                                  [[sg.Text('Source file: ')],
                                   [sg.In(), sg.FileBrowse()],
                                   [sg.Text('Output folder: ')],
                                    [sg.In(), sg.FolderBrowse()],
                                   [sg.Open(), sg.Cancel()]]).read(close=True)
        fname = values[0]
    else:
        fname = sys.argv[1]

    textFileName = fname

    saveFolder = values[1]

    #Get links as a list
    list_of_links = parse_links_text(textFileName)

    #Find and downloader image links
    image_num = 1;
    for link in list_of_links:
        try:
            urllib.request.urlretrieve(concatenate_link(link), concatenateFileName(image_num, saveFolder))
            image_num += 1
        except HTTPError as httperr:
            if httperr.code == 404:
                print(concatenate_link(link) + " not downloaded! 404 Error for the link")
            #elif httperr.code ==

        #urllib.request.urlretrieve(concatenate_link(link), concatenateFileName(image_num,saveFolder))
        #image_num += 1

        #Inteprets empty space as a link...how to avoid?


