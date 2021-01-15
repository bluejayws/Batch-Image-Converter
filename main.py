#
#@author agbjr
#
#
#
#

import urllib.request


#Reads a text file with links in them, one link per line.
#Returns a list with these links
def parse_links_text(text_source):
    text_list_file_reader = open(text_source,'r')
    return text_list_file_reader.readlines()


def concatenateFileName(image_num, saveFolder):
    return saveFolder+"\\"+"foto#"+str(image_num)+".jpg"
#C:\Users\evgnn\Desktop\aqui


def concatenate_link(link):
    return "" + link


if __name__ == '__main__':
    #Get parameters
    textFileName = input("Location of text file: " )
    print(textFileName)
    saveFolder = input("Location of save folder: ")
    print(saveFolder)

    #Get links as a list
    list_of_links = parse_links_text(textFileName)

    image_num = 1;
    for link in list_of_links:
        urllib.request.urlretrieve(concatenate_link(link), concatenateFileName(image_num,saveFolder))
        image_num += 1


