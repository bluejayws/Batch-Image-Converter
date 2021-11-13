# coded by: @bluejayws (Antonio G-B), internet, stackoverflow, etc.
import os
import sys
import subprocess

from PIL import Image
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout,
)


# Takes a path name to an image file and returns a new path name with the extension changed to .png
# ToDo: Add support for more than png (?)
def rename_to_png(path):
    split_file_at_dot = path.split(".")
    new_path = split_file_at_dot[0] + "_PNG.png"
    return new_path


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Random Image Tools V1.1 🔨")

        # to store the directory path for later use
        self.directory_path_name = ""

        # Set up the layouts
        layer_one = QHBoxLayout()  # First line of buttons
        layer_two = QHBoxLayout()  # Second line of buttons
        vertical_layout_parent = QVBoxLayout()

        # Main widget
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

        # Show folder after conversion
        self.show_folder_button = QPushButton()
        self.show_folder_button.setText("Open chosen directory in Finder")
        self.show_folder_button.clicked.connect(self.open_folder)
        self.show_folder_button.show()

        # Put the find folder button and folder selected button together
        layer_one.addWidget(self.select_a_folder_button)
        layer_one.addWidget(self.directory_label)

        # Put the convert button and open-in-finder button together
        layer_two.addWidget(self.convert_to_png_button)
        layer_two.addWidget(self.show_folder_button)

        # Put the "convert to png" button beneath
        vertical_layout_parent.addLayout(layer_one)
        vertical_layout_parent.addLayout(layer_two)

        widget.setLayout(vertical_layout_parent)
        self.setCentralWidget(widget)

    # Prompts user to select a folder, stores the given folder path and displays chosen path to user
    def select_folder_prompt(self):
        # Append a "/" otherwise it will mix the folder name and containing image file together
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/"
        # Note to self: You already passed the object. Just store the string into the object and update it there
        self.directory_label.setText(directory)
        self.directory_path_name = directory

    # Given a valid path name, will open it in the Folder browser app ( Only tested on MacOS so far)
    def open_folder(self):
        if self.directory_path_name != "":
            subprocess.call(["open", "-R", self.directory_path_name])
        else:
            # ToDo: Turn this into a error display that the user can see
            print("Not a valid directory :,(")

    # Given a non-empty folder path, converts all jpg images in it to png.
    def convert_folder_to_png(self):
        # ToDo: Remove duplicate adding of image paths to image_list
        # Todo: Add conversion to PNG of other file types, f.ex gif, webmp, etc

        # Get list of image files in the given folder
        image_list = []
        for root, dirs, files in os.walk(self.directory_path_name, topdown=True):
            for filename in files:
                if '.jpg' in filename:
                    absolute_path = self.directory_path_name + filename
                    # Avoid adding duplicates
                    if absolute_path not in image_list:
                        image_list.append(absolute_path)

        if len(image_list) > 0:  # There's at least on
            for jpg_image_path in image_list:
                # Get absolute path
                abs_path = os.path.abspath(jpg_image_path)

                # Save as png
                jpg_image_to_png = Image.open(abs_path)
                jpg_image_to_png.save(rename_to_png(abs_path))

                # Todo: Store png images in a new folder?
                # Todo: Add option to delete jpg images
                # Todo: Add a popup or some sort of progress mechaniism to delete photos
        else:
            # ToDo: Let user know that folder had no jpeg files in it, or any other type.
            print("There was no .jpeg, or image files that aren't in PNG format")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
