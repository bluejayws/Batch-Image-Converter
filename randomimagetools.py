# coded by: @bluejayws (Antonio G-B), w/help from the internet, stackoverflow, etc.
# icons used are made by: Freepik,
import os
import sys
import subprocess

from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout, QProgressBar,
)

# Takes a path name to an image file and returns a new path name with the extension changed to .png
# ToDo: Add support for more than png (?)
from PyQt6.uic.properties import QtCore


def rename_to_png(path):
    split_file_at_dot = path.split(".")
    new_path = split_file_at_dot[0] + "_PNG.png"
    return new_path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Random Image Tools V1.2 🔨")
        # ToDo: Add a "rename?" flag. Like rename image files

        # to store the directory path for later use
        self.directory_path_name = "/"

        # Set up the layouts
        layer_one = QHBoxLayout()  # First line of buttons
        layer_two = QHBoxLayout()  # Second line of buttons
        layer_three = QHBoxLayout()
        #         login_form_layout.setFormAlignment(Qt.AlignCenter)
        # layer_three.setFormAlignment()
        vertical_layout_parent = QVBoxLayout()

        # Parent widget
        widget = QWidget()

        # Displays selected directory
        self.directory_label = QLabel()
        self.directory_label.setText("Directory to be worked on will show here            ")
        self.directory_label.show()

        # Displays "Select folder" button
        self.select_a_folder_button = QPushButton()
        self.select_a_folder_button.setText("Select a folder:")
        self.select_a_folder_button.clicked.connect(self.select_folder_prompt)
        self.select_a_folder_button.show()

        # Displays button to initiate image conversion
        self.convert_to_png_button = QPushButton()
        self.convert_to_png_button.setText("Convert to PNG")
        self.convert_to_png_button.clicked.connect(self.convert_folder_to_png)
        self.convert_to_png_button.show()

        # Displays button to open selected directory in the file browser
        self.show_folder_button = QPushButton()
        self.show_folder_button.setText("Open selected folder in file browser")
        self.show_folder_button.clicked.connect(self.open_folder)
        self.show_folder_button.show()

        # Displays label when conversion is finished, and the corresponding progress bar
        self.conversion_finished_or_error_label = QLabel()
        self.conversion_finished_or_error_label.setText("👀 waiting for you to press \"Convert to PNG\" ")

        # Put the find folder button and folder selected button together
        layer_one.addWidget(self.select_a_folder_button)
        layer_one.addWidget(self.directory_label)

        # Put the convert button and open-in-finder button together
        layer_two.addWidget(self.convert_to_png_button)
        layer_two.addWidget(self.show_folder_button)

        # Label and progress bar
        layer_three.addWidget(self.conversion_finished_or_error_label)
        layer_three.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Put the "convert to png" button beneath
        vertical_layout_parent.addLayout(layer_one)
        vertical_layout_parent.addLayout(layer_two)
        vertical_layout_parent.addLayout(layer_three)

        widget.setLayout(vertical_layout_parent)
        self.setCentralWidget(widget)

    # Prompts user to select a folder, stores the given folder path and displays chosen path to user
    def select_folder_prompt(self):
        # Append a "/" otherwise it will mix the folder name and containing image file together
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/"

        # Update QLabel to new directory, and store it in self for future use
        self.directory_label.setText(directory)
        self.directory_path_name = directory

    # Given a path name, will open it in the Folder browser app
    def open_folder(self):
        subprocess.call(["open", "-R", self.directory_path_name])

    # Given the current state of the directory_path_name folder, will scan for image files in that folder
    # Just scans .jpg for now
    def scan_for_jpg_file_paths(self):
        image_list = []

        for root, dirs, files in os.walk(self.directory_path_name, topdown=True):
            for filename in files:
                if '.jpg' in filename:
                    absolute_path = self.directory_path_name + filename
                    # Avoid adding duplicates
                    if absolute_path not in image_list:
                        image_list.append(absolute_path)

        return image_list

    # Given a non-empty folder path, converts all jpg images in it to png.
    # ToDo: Let user know that folder had no jpeg files in it, or any other type.
    #  print("There are no .jpeg, or image files in this folder")
    # ToDo: Remove duplicate adding of image paths to image_list
    # Todo: Add conversion to PNG of other file types, f.ex gif, webmp, etc
    # ToDo: Selecting a directory and display a window showing contents
    # Todo: Store png images in a new folder?
    # Todo: Add option to delete jpg images
    # Todo: Add a popup or some sort of progress mechaniism to delete photos : A checkbox
    def convert_folder_to_png(self):

        self.conversion_finished_or_error_label.setText("Converting")

        # Get list of image files in the given folder
        image_list = self.scan_for_jpg_file_paths()

        # Progress bar depends on independent variable, length of image list = x

        if len(image_list) > 0:
            self.conversion_finished_or_error_label.setText("...")
            # Convert images
            for jpg_image_path in image_list:

                # Get absolute path
                abs_path = os.path.abspath(jpg_image_path)

                # Save as png
                jpg_image_to_png = Image.open(abs_path)
                jpg_image_to_png.save(rename_to_png(abs_path))

            self.conversion_finished_or_error_label.setText("Conversion finished")

        if len(image_list) <= 0:
            self.conversion_finished_or_error_label.setText("There are no image files in this folder")


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
