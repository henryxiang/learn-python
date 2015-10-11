#!/usr/bin/env python

import sys
from PyQt4.QtGui import *

# Start PyQt Application
app = QApplication(sys.argv)

# Main window widget
window = QWidget()

# Set up table widget
table = QTableWidget(0,4)

# Make the table stretch horizontally
header = table.horizontalHeader()
header.setResizeMode(QHeaderView.Stretch)

# Change table header items
tableHeaders = ["First Name", "Last Name", "Date of Birth", "GPA"]
for i in range(len(tableHeaders)):
 	table.setHorizontalHeaderItem(i, QTableWidgetItem(tableHeaders[i]))

# Create two push buttons
btnAdd = QPushButton("Add New Student")
btnRemove = QPushButton("Remove Student")

# Centralize two buttons in a horizontal box layout
hbox = QHBoxLayout()
hbox.addStretch(1)
hbox.addWidget(btnAdd)
hbox.addWidget(btnRemove)
hbox.addStretch(1)

# Set up the main window layout as vertical box layout,
# and then add table widget and horizontal sub-layout
vbox = QVBoxLayout()

vbox.addWidget(table)
vbox.addLayout(hbox)

window.setLayout(vbox)

window.show()

# Callback function when button "Add New Student" is clicked
def addStudent():
	global table
	table.insertRow(table.rowCount())
# Link button "clicked" event to callback function
btnAdd.clicked.connect(addStudent)

# Callback function when button "Remove Student" is clicked
def removeStudent():
	global table
	sm = table.selectionModel()      
	rowIndices = [ r.row() for r in sm.selectedRows() ]
	for i in sorted(rowIndices, reverse=True):
		table.removeRow(i)
# Link button "clicked" event to callback function
btnRemove.clicked.connect(removeStudent)

sys.exit(app.exec_())


