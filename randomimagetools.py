# coded by: @bluejayws (Antonio G-B), w/help from the internet, stackoverflow, etc.
# icons used are made by: Freepik,
import os
import sys
import subprocess

from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout, QCheckBox, QListWidget,
)


# ToDo: After selecting item in QListWidget, and double clicking it, will open the image file


# Takes a path name to an image file and returns a new path name with the extension changed to .png
def rename_image_path_to_png(path):
    split_file_at_dot = path.split(".")
    new_path = split_file_at_dot[0] + "_PNG.png"
    return new_path

# Given a filepath to an image, will extract the filename and it's extension
# Used for storing PNG files when the "Create new folder?" checkbox is checked
def extract_image_name_and_extension(path) :
    split_file_at_slash = path.split('/')
    print("EXTRACTED: " + split_file_at_slash[len(split_file_at_slash)-1])
    return split_file_at_slash[len(split_file_at_slash)-1]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Random Image Tools V1.2 🔨")
        self.image_list = []
        # ToDo: Add a "rename?" flag. Like rename image files

        # to store the directory path for later use
        self.directory_path_name = "/"

        # Set up the layouts
        layer_one = QHBoxLayout()  # Select a folder, selected directory

        layer_one_and_a_half = QHBoxLayout()  # Selected directory contents

        layer_two = QHBoxLayout()  # Second line of buttons
        layer_two_vertical_one = QVBoxLayout()  # Store the first column w/checkbox and "Convert"
        layer_two_vertical_two = QVBoxLayout()  # Store the second column w/checkbox and "Open in File Browser"

        layer_three = QHBoxLayout()  # Conversion process state
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

        # Displays the image contents of the selected folder
        self.image_paths_list_widget = QListWidget()
        self.image_paths_list_widget.show()

        # Displays button to initiate image conversion
        self.convert_to_png_button = QPushButton()
        self.convert_to_png_button.setText("Convert to PNG")
        self.convert_to_png_button.clicked.connect(self.convert_folder_to_png)
        self.convert_to_png_button.show()

        # Check boxes for "Create new folder for PNGs" and "Delete original files after converting"
        self.create_new_folder_checkbox = QCheckBox()
        self.create_new_folder_checkbox.setText("Create new folder to store converted PNG's?")
        self.create_new_folder_checkbox.show()

        self.delete_original_files_checkbox = QCheckBox()
        self.delete_original_files_checkbox.setText("Delete original files after converting them to PNG?")
        self.create_new_folder_checkbox.show()

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

        # Image paths of selected folder
        layer_one_and_a_half.addWidget(self.image_paths_list_widget)

        # Put the convert button and open-in-finder button together
        layer_two_vertical_one.addWidget(self.convert_to_png_button)
        layer_two_vertical_one.addWidget(self.delete_original_files_checkbox)
        layer_two.addLayout(layer_two_vertical_one)

        layer_two_vertical_two.addWidget(self.show_folder_button)
        layer_two_vertical_two.addWidget(self.create_new_folder_checkbox)
        layer_two.addLayout(layer_two_vertical_two)

        # Label and progress bar
        layer_three.addWidget(self.conversion_finished_or_error_label)
        layer_three.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Put the "convert to png" button beneath
        vertical_layout_parent.addLayout(layer_one)
        vertical_layout_parent.addLayout(layer_one_and_a_half)
        vertical_layout_parent.addLayout(layer_two)
        vertical_layout_parent.addLayout(layer_three)

        widget.setLayout(vertical_layout_parent)
        self.setCentralWidget(widget)

    # Prompts user to select a folder, stores the given folder path and displays chosen path to user
    def select_folder_prompt(self):
        #  Clear self.image_list and QListWidget to prepare for newly selected folder.
        self.image_list.clear()
        self.image_paths_list_widget.clear()

        # print("checkState() is: " + str(self.create_new_folder_checkbox.checkState()))
        # print("isChecked() is: " + str(self.delete_original_files_checkbox.isChecked()))

        # Append a "/" otherwise it will mix the folder name and containing image file together
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory")) + "/"
        # Update QLabel to new directory, and store it in self for future use
        self.directory_label.setText(directory)
        self.directory_path_name = directory

        # Update self.image_list field
        image_list = self.scan_for_jpg_file_paths()
        self.image_list = image_list

        # Populated the QListWindow() with the update self.image_list field
        self.image_paths_list_widget.addItems(self.image_list)

    # Given a path name, will open it in the Folder browser app
    def open_folder(self):
        subprocess.call(["open", "-R", self.directory_path_name])

    # Given the current state of the directory_path_name folder, will scan for image files in that folder
    def scan_for_jpg_file_paths(self):
        image_list = []

        for root, dirs, files in os.walk(self.directory_path_name, topdown=True):
            for filename in files:
                if '.jpeg' or '.jpg' or '.webp' or '.gif' or '.icns' in filename:
                    if '.png' not in filename:
                        # print("Added : " + filename + " to our conversion list")
                        absolute_path = self.directory_path_name + filename
                        # Avoid adding duplicates
                        if absolute_path not in image_list:
                            image_list.append(absolute_path)

        return image_list

    # Given a non-empty folder path, converts all jpg images in it to png.
    # Todo: Store png images in a new folder?
    # ToDo: Add a "Delete images after converting?"
    # ToDo: Add functionality for checkboxes
    # Ok so that the QListWidget can update, I'm going to have to get the image_list before calling this function.
    # In other words, image_list is a field in the MainWindow subclass, and is update after selecting the folder, and
    #   called before calling this function.
    def convert_folder_to_png(self):
        self.conversion_finished_or_error_label.setText("Converting")
        # Progress bar depends on independent variable, length of image list = x
        if len(self.image_list) > 0:
            self.convert_images_to_png()
            self.conversion_finished_or_error_label.setText("Conversion finished")
        if len(self.image_list) <= 0:
            self.conversion_finished_or_error_label.setText("There are no image files in this folder")

    # This will be called after a folder has been selected and the "Convert to PNG" button has been pressed
    def convert_images_to_png(self):
        self.conversion_finished_or_error_label.setText("...")
        # Convert images
        # ToDo : Put the checkbox logic here

        user_wanted_png_in_new_folder = self.create_new_folder_checkbox.isChecked()
        converted_png_folder_name = ""

        if user_wanted_png_in_new_folder:
            converted_png_folder_name = self.directory_path_name + "Converted PNG Files/"
            print("Created PNG folder name: " + converted_png_folder_name) #  /Users/antoniogurrola-beltran/Desktop/testFolder/imagetestfolder/Converted PNG Files/
            os.mkdir(converted_png_folder_name)


        for image_path in self.image_list:
            # Get absolute path
            absolute_image_path = os.path.abspath(image_path)
            if ".DS_Store" not in absolute_image_path:  # Mac adds .DS_Store, just a way to ignore these pesky files
                unconverted_image = Image.open(absolute_image_path)  # Image object
                if user_wanted_png_in_new_folder:  # If the user wanted to store converted PNGS in a folder
                    name_and_extension_of_image = extract_image_name_and_extension(absolute_image_path)
                    # Add the image name and extensions s.t. they end up in the folder
                    image_path_stored_in_converted_png_folder = converted_png_folder_name + name_and_extension_of_image
                    unconverted_image.save(rename_image_path_to_png(image_path_stored_in_converted_png_folder))
                else:
                    unconverted_image.save(rename_image_path_to_png(absolute_image_path))


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
