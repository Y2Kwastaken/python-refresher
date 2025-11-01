import sys
import datetime
import pygame.mixer as mixer
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.paused = False
        
        self.button = QPushButton("Select Song")
        self.button.clicked.connect(self.select_song)
        self.pause_button = QPushButton(">")
        self.pause_button.clicked.connect(self.pause_song)
        
        self.label = QLabel("No song selected.")
        self.label.setStyleSheet("color: gray;")

        self.slider_label = QLabel("Volume")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(100)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.adjust_volume)
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)
        
        self.setLayout(layout)
        
    def select_song(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select a song",
            ""
            "Audio Files (*.mp3 *.wave *.flac *.ogg);;All Files (*)"
        )
        
        if file:
            self.label.setText(f"Selected: {file}")
            self.label.setStyleSheet("color: gray;")
        else:
            self.label.setText("No song selected.")
            self.label.setStyleSheet("color: gray;")
            
            Q
        mixer.music.load(file)
        mixer.music.play()
        
    def pause_song(self):
        if not self.paused:
            mixer.music.pause()
            self.play_button.setText("Play")
            self.paused = True
        else:
            mixer.music.unpause()
            self.play_button.setText("Pause")
            self.paused = False
    
    def adjust_volume(self):
        mixer.music.set_volume(self.slider.value() / 100)

def window():
    app = QApplication(sys.argv)
    w = Window()
    w.setWindowTitle("Music Box")   
    mixer.init()

    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    window()