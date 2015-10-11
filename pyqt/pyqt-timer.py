#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

app = QApplication(sys.argv)

window = QWidget()
window.setFixedSize(300,200)
window.show()

lcd = QLCDNumber()
lcd.setMinimumHeight(100)
lcd.setMaximumHeight(100)
btn = QPushButton("Start")
btn.setCheckable(True)

vbox = QVBoxLayout()
window.setLayout(vbox)

hbox = QHBoxLayout()
hbox.addStretch(1)
hbox.addWidget(btn)
hbox.addStretch(1)

vbox.addWidget(lcd)
vbox.addStretch(1)
vbox.addLayout(hbox)


timer = QTimer(window)
timer.setInterval(1000)

countDown = 20
def showCount():
    global lcd, countDown
    lcd.display(countDown)
    countDown -= 1
timer.timeout.connect(showCount)

def onClicked(pressed):
    if pressed:
        timer.start(1000)
        btn.setText("Stop")
    else:
        timer.stop()
        btn.setText("Start")

btn.clicked[bool].connect(onClicked)

sys.exit(app.exec_())
