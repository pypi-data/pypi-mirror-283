# Form implementation generated from reading ui file 'src/eric7/EricWidgets/EricListSelectionDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EricListSelectionDialog(object):
    def setupUi(self, EricListSelectionDialog):
        EricListSelectionDialog.setObjectName("EricListSelectionDialog")
        EricListSelectionDialog.resize(400, 500)
        EricListSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(EricListSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.messageLabel = QtWidgets.QLabel(parent=EricListSelectionDialog)
        self.messageLabel.setWordWrap(True)
        self.messageLabel.setObjectName("messageLabel")
        self.verticalLayout.addWidget(self.messageLabel)
        self.selectionList = QtWidgets.QListWidget(parent=EricListSelectionDialog)
        self.selectionList.setAlternatingRowColors(True)
        self.selectionList.setObjectName("selectionList")
        self.verticalLayout.addWidget(self.selectionList)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=EricListSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EricListSelectionDialog)
        self.buttonBox.accepted.connect(EricListSelectionDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EricListSelectionDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EricListSelectionDialog)

    def retranslateUi(self, EricListSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        EricListSelectionDialog.setWindowTitle(_translate("EricListSelectionDialog", "Select from List"))
        self.messageLabel.setText(_translate("EricListSelectionDialog", "Select from the list below:"))
