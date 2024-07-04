# Form implementation generated from reading ui file 'src/eric7/MicroPython/ConnectionSelectionDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ConnectionSelectionDialog(object):
    def setupUi(self, ConnectionSelectionDialog):
        ConnectionSelectionDialog.setObjectName("ConnectionSelectionDialog")
        ConnectionSelectionDialog.resize(400, 108)
        ConnectionSelectionDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(ConnectionSelectionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=ConnectionSelectionDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.portNameComboBox = QtWidgets.QComboBox(parent=ConnectionSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portNameComboBox.sizePolicy().hasHeightForWidth())
        self.portNameComboBox.setSizePolicy(sizePolicy)
        self.portNameComboBox.setObjectName("portNameComboBox")
        self.gridLayout.addWidget(self.portNameComboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=ConnectionSelectionDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.deviceTypeComboBox = QtWidgets.QComboBox(parent=ConnectionSelectionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceTypeComboBox.sizePolicy().hasHeightForWidth())
        self.deviceTypeComboBox.setSizePolicy(sizePolicy)
        self.deviceTypeComboBox.setObjectName("deviceTypeComboBox")
        self.gridLayout.addWidget(self.deviceTypeComboBox, 1, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=ConnectionSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(ConnectionSelectionDialog)
        self.buttonBox.accepted.connect(ConnectionSelectionDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(ConnectionSelectionDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ConnectionSelectionDialog)

    def retranslateUi(self, ConnectionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionSelectionDialog.setWindowTitle(_translate("ConnectionSelectionDialog", "Port and Device Type Selection"))
        self.label.setText(_translate("ConnectionSelectionDialog", "Serial Port Name:"))
        self.portNameComboBox.setToolTip(_translate("ConnectionSelectionDialog", "Select the serial port name to connect"))
        self.label_2.setText(_translate("ConnectionSelectionDialog", "Device Type:"))
        self.deviceTypeComboBox.setToolTip(_translate("ConnectionSelectionDialog", "Select the device type"))
