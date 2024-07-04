# Form implementation generated from reading ui file 'ibridgesgui/ui_files/renameItem.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_renameItem(object):
    def setupUi(self, renameItem):
        renameItem.setObjectName("renameItem")
        renameItem.resize(500, 200)
        renameItem.setMinimumSize(QtCore.QSize(500, 200))
        renameItem.setMaximumSize(QtCore.QSize(500, 200))
        renameItem.setStyleSheet("QWidget\n"
"{\n"
"    background-color: rgb(211,211,211);\n"
"    color: rgb(88, 88, 90);\n"
"    selection-background-color: rgb(21, 165, 137);\n"
"    selection-color: rgb(245, 244, 244);\n"
"    font: 16pt\n"
"}\n"
"\n"
"QLabel#error_label\n"
"{\n"
"    color: rgb(220, 130, 30);\n"
"}\n"
"\n"
"QLineEdit, QTextEdit, QTableWidget\n"
"{\n"
"   background-color:  rgb(245, 244, 244)\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    background-color: rgb(21, 165, 137);\n"
"    color: rgb(245, 244, 244);\n"
"}\n"
"\n"
"QPushButton#home_button, QPushButton#parent_button, QPushButton#refresh_button\n"
"{\n"
"    background-color: rgb(245, 244, 244);\n"
"}\n"
"\n"
"QTabWidget#info_tabs\n"
"{\n"
"     background-color: background-color: rgb(211,211,211);\n"
"}\n"
"\n"
"")
        self.verticalLayout = QtWidgets.QVBoxLayout(renameItem)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=renameItem)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.item_path_label = QtWidgets.QLabel(parent=renameItem)
        self.item_path_label.setText("")
        self.item_path_label.setObjectName("item_path_label")
        self.horizontalLayout.addWidget(self.item_path_label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(parent=renameItem)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.item_path_input = QtWidgets.QLineEdit(parent=renameItem)
        self.item_path_input.setObjectName("item_path_input")
        self.verticalLayout.addWidget(self.item_path_input)
        self.error_label = QtWidgets.QLabel(parent=renameItem)
        self.error_label.setStyleSheet("")
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")
        self.verticalLayout.addWidget(self.error_label)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=renameItem)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(renameItem)
        self.buttonBox.accepted.connect(renameItem.accept) # type: ignore
        self.buttonBox.rejected.connect(renameItem.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(renameItem)

    def retranslateUi(self, renameItem):
        _translate = QtCore.QCoreApplication.translate
        renameItem.setWindowTitle(_translate("renameItem", "Rename/Move"))
        self.label.setText(_translate("renameItem", "Rename or move:"))
        self.label_2.setText(_translate("renameItem", "to new location:"))
