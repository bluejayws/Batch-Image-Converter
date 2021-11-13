# coded by: @bluejayws (Antonio G-B), internet, stackoverflow, etc.
import os
import sys

from PIL import Image
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout,
)


def rename_to_png(path):
    # print("Path before rename: %s" % path)
    split_file_at_dot = path.split(".")
    new_path = split_file_at_dot[0] + "_PNG.png"
    # print("Path after rename: %s" % new_path)
    return new_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Random Image Tools V1 🔨")

        # to store the directory path for later use
        self.directory_path_name = ""

        # load a layout
        layout_button_and_directory_name = QHBoxLayout()
        layout_of_vertical_actions = QVBoxLayout()
        # widget
        widget = QWidget()

        # Create a label to show directory name
        self.directory_label = QLabel()
        self.directory_label.setText("Directory to be worked on will show here            ")
        self.directory_label.show()

        # Create a button to select a folder prompt
        self.select_a_folder_button = QPushButton()
        self.select_a_folder_button.setText("Select a folder with the images you want to convert")
        self.select_a_folder_button.clicked.connect(self.select_folder_prompt)
        self.select_a_folder_button.show()

        # The go button to convert all items in a folder to png
        self.convert_to_png_button = QPushButton()
        self.convert_to_png_button.setText("Convert selected folder contents to png")
        self.convert_to_png_button.clicked.connect(self.convert_folder_to_png)
        self.convert_to_png_button.show()

        # ToDo: Open folder in finder option

        # Put the find folder button and folder selected button together
        layout_button_and_directory_name.addWidget(self.select_a_folder_button)
        layout_button_and_directory_name.addWidget(self.directory_label)

        # Put the "convert to png" button beneath
        layout_of_vertical_actions.addLayout(layout_button_and_directory_name)
        layout_of_vertical_actions.addWidget(self.convert_to_png_button)

        widget.setLayout(layout_of_vertical_actions)

        self.setCentralWidget(widget)

    # Prompts user to select a folder, stores the given folder path and displays chosen path to user
    def select_folder_prompt(self):
        # print("select a folder prompt button has been clicked")
        # Append a "/" otherwise it will mix the folder name and containing image file together
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/"
        #print("bug here maybe: %s" % directory)
        # You already passed the object. Just store the string into the object and update it there
        self.directory_label.setText(directory)
        self.directory_path_name = directory
        # print(directory)

    # Given a non-empty folder path, converts all jpg images in it to png.
    def convert_folder_to_png(self):
        # Get list of image files in the given folder
        # Todo: Add conversion to PNG of other file types, f.ex gif, webmp, etc
        # print("converting %s to png..." % self.directory_path_name)
        image_list = []
        # ToDo: Remove duplicate adding of image paths to image_list
        for root, dirs, files in os.walk(self.directory_path_name, topdown=True):
            for filename in files:
                if '.jpg' in filename:
                    absolute_path = self.directory_path_name + filename
                    # print(absolutePath)
                    if absolute_path not in image_list:
                        # print("appending %s to imageList " % absolutePath)
                        image_list.append(absolute_path)

        for jpg_image_path in image_list:
            # Get absolute path
            abs_path = os.path.abspath(jpg_image_path)

            # save as png
            jpg_image_to_png = Image.open(abs_path)
            jpg_image_to_png.save(rename_to_png(abs_path))

            # Todo: Store png images in a new folder?
            # Todo: Add option to delete jpg images
            # Todo: Add a popup or some sort of progress mechaniism to delete photos




app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
