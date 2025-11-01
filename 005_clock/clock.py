import sys
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TIME_STRING = "%m-%d-%Y %I:%M:%S%p"

def curtime() -> str:
    return datetime.datetime.now().strftime(TIME_STRING)
            
class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.curtime = curtime()
        self.label = QLabel(self.curtime)
        self.label.setFont(QFont('Arial', 32))
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer_id: int = self.startTimer(1000)

    def timerEvent(self, event):
        if event.timerId() == self.timer_id:
            self.curtime = curtime()
            self.label.setText(self.curtime)

def window():
   app = QApplication(sys.argv)
   w = Window()
   w.setWindowTitle("Clock")
   w.move(0, 0)
   
   w.setWindowFlag(Qt.WindowStaysOnTopHint)
   

   w.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
    window()