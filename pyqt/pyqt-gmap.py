#!/usr/bin/env python

import sys
from PyQt4.QtGui import *
from motionless import *
from urllib.request import *

app = QApplication(sys.argv)

win = QWidget()
win.setGeometry(40,40,640,750)
win.setWindowTitle("Google Map")
win.show()

search = QLineEdit()
button = QPushButton("Get Map")
label = QLabel()

hbox = QHBoxLayout()
vbox = QVBoxLayout()

hbox.addWidget(search)
hbox.addWidget(button)
vbox.addLayout(hbox)
vbox.addWidget(label)

win.setLayout(vbox)
win.show()

def onClick():
    global search, label
    gmap = DecoratedMap(size_x=640, size_y=640)
    gmap.add_marker(AddressMarker(search.text(), label='A'))
    imgData = urlopen(gmap.generate_url()).read()
    img = QImage.fromData(imgData)
    label.setPixmap(QPixmap.fromImage(img))
    search.setText("")

button.clicked.connect(onClick)

sys.exit(app.exit_())
