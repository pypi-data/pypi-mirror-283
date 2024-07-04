# Form implementation generated from reading ui file 'src/eric7/MicroPython/ConvertToUF2Dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ConvertToUF2Dialog(object):
    def setupUi(self, ConvertToUF2Dialog):
        ConvertToUF2Dialog.setObjectName("ConvertToUF2Dialog")
        ConvertToUF2Dialog.resize(600, 600)
        ConvertToUF2Dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConvertToUF2Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=ConvertToUF2Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.firmwarePicker = EricPathPicker(parent=ConvertToUF2Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firmwarePicker.sizePolicy().hasHeightForWidth())
        self.firmwarePicker.setSizePolicy(sizePolicy)
        self.firmwarePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.firmwarePicker.setObjectName("firmwarePicker")
        self.gridLayout.addWidget(self.firmwarePicker, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(parent=ConvertToUF2Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.familiesComboBox = QtWidgets.QComboBox(parent=ConvertToUF2Dialog)
        self.familiesComboBox.setObjectName("familiesComboBox")
        self.gridLayout.addWidget(self.familiesComboBox, 1, 1, 1, 2)
        self.label_3 = QtWidgets.QLabel(parent=ConvertToUF2Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.addressEdit = QtWidgets.QLineEdit(parent=ConvertToUF2Dialog)
        self.addressEdit.setMaxLength(4)
        self.addressEdit.setClearButtonEnabled(True)
        self.addressEdit.setObjectName("addressEdit")
        self.gridLayout.addWidget(self.addressEdit, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.convertButton = QtWidgets.QPushButton(parent=ConvertToUF2Dialog)
        self.convertButton.setObjectName("convertButton")
        self.gridLayout.addWidget(self.convertButton, 3, 0, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.outputEdit = QtWidgets.QTextEdit(parent=ConvertToUF2Dialog)
        self.outputEdit.setReadOnly(True)
        self.outputEdit.setObjectName("outputEdit")
        self.verticalLayout.addWidget(self.outputEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=ConvertToUF2Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ConvertToUF2Dialog)
        self.buttonBox.accepted.connect(ConvertToUF2Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(ConvertToUF2Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ConvertToUF2Dialog)
        ConvertToUF2Dialog.setTabOrder(self.firmwarePicker, self.familiesComboBox)
        ConvertToUF2Dialog.setTabOrder(self.familiesComboBox, self.addressEdit)
        ConvertToUF2Dialog.setTabOrder(self.addressEdit, self.convertButton)
        ConvertToUF2Dialog.setTabOrder(self.convertButton, self.outputEdit)

    def retranslateUi(self, ConvertToUF2Dialog):
        _translate = QtCore.QCoreApplication.translate
        ConvertToUF2Dialog.setWindowTitle(_translate("ConvertToUF2Dialog", "Convert To UF2"))
        self.label.setText(_translate("ConvertToUF2Dialog", "Firmware File:"))
        self.firmwarePicker.setToolTip(_translate("ConvertToUF2Dialog", "Enter the path of the MicroPython firmware file to be converted."))
        self.label_2.setText(_translate("ConvertToUF2Dialog", "Chip Family:"))
        self.familiesComboBox.setToolTip(_translate("ConvertToUF2Dialog", "Select the chip family of the firmware file."))
        self.label_3.setText(_translate("ConvertToUF2Dialog", "Base Address:"))
        self.addressEdit.setToolTip(_translate("ConvertToUF2Dialog", "Enter the base address for .bin firmware files or leave empty to use the default (0x2000)."))
        self.convertButton.setToolTip(_translate("ConvertToUF2Dialog", "Press to start the conversion process."))
        self.convertButton.setText(_translate("ConvertToUF2Dialog", "Convert"))
from eric7.EricWidgets.EricPathPicker import EricPathPicker
