# Form implementation generated from reading ui file 'src/eric7/UI/DeleteFilesConfirmationDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DeleteFilesConfirmationDialog(object):
    def setupUi(self, DeleteFilesConfirmationDialog):
        DeleteFilesConfirmationDialog.setObjectName("DeleteFilesConfirmationDialog")
        DeleteFilesConfirmationDialog.resize(500, 350)
        DeleteFilesConfirmationDialog.setWindowTitle("")
        DeleteFilesConfirmationDialog.setSizeGripEnabled(True)
        self.vboxlayout = QtWidgets.QVBoxLayout(DeleteFilesConfirmationDialog)
        self.vboxlayout.setObjectName("vboxlayout")
        self.message = QtWidgets.QLabel(parent=DeleteFilesConfirmationDialog)
        self.message.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.vboxlayout.addWidget(self.message)
        self.label = QtWidgets.QLabel(parent=DeleteFilesConfirmationDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.filesList = QtWidgets.QListWidget(parent=DeleteFilesConfirmationDialog)
        self.filesList.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.filesList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.NoSelection)
        self.filesList.setObjectName("filesList")
        self.vboxlayout.addWidget(self.filesList)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=DeleteFilesConfirmationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.No|QtWidgets.QDialogButtonBox.StandardButton.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(DeleteFilesConfirmationDialog)
        QtCore.QMetaObject.connectSlotsByName(DeleteFilesConfirmationDialog)

    def retranslateUi(self, DeleteFilesConfirmationDialog):
        _translate = QtCore.QCoreApplication.translate
        self.message.setText(_translate("DeleteFilesConfirmationDialog", "Dummy"))
        self.label.setText(_translate("DeleteFilesConfirmationDialog", "<font color=\"#FF0000\"><b>WARNING:</b> This operation is not reversible!</font>"))
