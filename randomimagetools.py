# coded by: @bluejayws (Antonio G-B), internet, stackoverflow, etc.

import sys


from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QHBoxLayout, QWidget, QFileDialog, QPushButton, QVBoxLayout,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📸 Random Image Tools V1 🔨")

        #to store the directory path for later use
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
        self.select_a_folder_button.setText("Select a folder")
        self.select_a_folder_button.clicked.connect(self.select_folder_prompt)
        self.select_a_folder_button.show()

        # The go button to convert all items in a folder to png
        self.convert_to_png_button = QPushButton()
        self.convert_to_png_button.setText("Convert selected folder to png")
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

    def select_folder_prompt(self):
        # print("select a folder prompt button has been clicked")
        directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # You already passed the object. Just store the string into the object and update it there
        self.directory_label.setText(directory)
        self.directory_path_name = directory
        # print(directory)

    def convert_folder_to_png(self):
        print("converting %s to png..." % self.directory_path_name)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
