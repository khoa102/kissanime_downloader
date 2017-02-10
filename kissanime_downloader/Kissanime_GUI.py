#!/usr/bin/python
#
# Kissanime_GUi.py - Creating the GUI for kissanime program

# Import sys to take argument from the command line
import sys

# Import PySide for GUI
from PySide.QtCore import *
from PySide.QtGui import *

# Create Qt application for the program
qtApp = QApplication(sys.argv)

class KissanimeGUI(QWidget):
    ''' The main GUI interface'''
    def __init__(self):
        # Initialize the object as a widget to create the main window
        # set its title and minimum width
        QWidget.__init__(self)
        self.setWindowTitle('Kissanime Downloader')
        self.setMinimumWidth(700)

        # Create a layout as the main layout
        self.layout = QGridLayout()

        # Create a label for anime URL and set alignment for the label
        self.urlLabel = QLabel("Anime URL:", self)
        self.urlLabel.setAlignment(Qt.AlignRight);

        # Add the label to layout
        self.layout.addWidget(self.urlLabel,0,0)
 
        
        # Create a entry control to specify the anime URL
        self.animeURL = QLineEdit(self)
        self.animeURL.setPlaceholderText("E.g: www.kissanime.ru/Anime/Nodame")
        
        # Add the animeURL entry control to the layout
        # Span the QlineEdit for 5 columns
        self.layout.addWidget(self.animeURL,0,1,1,5)

        # Create add URL button with its caption
        self.urlButton = QPushButton('&Add URL',self)

        # Add the button the sixth column of the grid
        self.layout.addWidget(self.urlButton,0,6)

        # Create a label for avaible episode
        self.episodeLabel = QLabel('Available Episodes:', self)
        self.episodeLabel.setAlignment(Qt.AlignRight)
        
        # Add the episode label to the layout
        self.layout.addWidget(self.episodeLabel, 1,0)


        # Create a progress bar label
        self.progressLabel = QLabel('Progress:', self)
        self.progressLabel.setAlignment(Qt.AlignRight)
        
        # Add the progress label to the layout
        self.layout.addWidget(self.progressLabel, 2, 0)

        # Create a progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(20)
        self.progressBar.setValue(0)
        
        # Add the progress bar to the layout
        self.layout.addWidget(self.progressBar, 2, 1, 1, 5)
        
        # Set the Grid layout as the main window's main layout
        self.setLayout(self.layout)

    def addURL(self):
         pass       
    
    def run(self):
        # Show the window
        self.show()

        # Run the qt application
        qtApp.exec_()

# Create an instance of the application window and run it
app = KissanimeGUI()
app.run()
