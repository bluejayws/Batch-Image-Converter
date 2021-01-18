#
#@author agbjr
#
#
#
#

import urllib.request
import PySimpleGUI as sg
import sys
from urllib.error import HTTPError

#Reads a text file with links in them, one link per line.
#Returns a list with these links
def parse_links_text(text_source):
    text_list_file_reader = open(text_source,'r')
    return text_list_file_reader.readlines()

#Returns a name for a given photo number and folder location
def concatenateFileName(image_num, saveFolder):
    return saveFolder+"\\"+"foto#"+str(image_num)+".jpg"

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

        #urllib.request.urlretrieve(concatenate_link(link), concatenateFileName(image_num,saveFolder))
        #image_num += 1


