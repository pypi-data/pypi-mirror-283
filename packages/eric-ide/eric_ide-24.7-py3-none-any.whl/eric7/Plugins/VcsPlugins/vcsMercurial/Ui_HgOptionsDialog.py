# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsMercurial/HgOptionsDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgOptionsDialog(object):
    def setupUi(self, HgOptionsDialog):
        HgOptionsDialog.setObjectName("HgOptionsDialog")
        HgOptionsDialog.resize(565, 78)
        HgOptionsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgOptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TextLabel5 = QtWidgets.QLabel(parent=HgOptionsDialog)
        self.TextLabel5.setObjectName("TextLabel5")
        self.horizontalLayout.addWidget(self.TextLabel5)
        self.vcsLogEdit = QtWidgets.QLineEdit(parent=HgOptionsDialog)
        self.vcsLogEdit.setObjectName("vcsLogEdit")
        self.horizontalLayout.addWidget(self.vcsLogEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=HgOptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.TextLabel5.setBuddy(self.vcsLogEdit)

        self.retranslateUi(HgOptionsDialog)
        self.buttonBox.accepted.connect(HgOptionsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgOptionsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgOptionsDialog)

    def retranslateUi(self, HgOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        HgOptionsDialog.setWindowTitle(_translate("HgOptionsDialog", "Initial Commit"))
        HgOptionsDialog.setWhatsThis(_translate("HgOptionsDialog", "<b>Initial Commit Dialog</b>\n"
"<p>Enter the message for the initial commit.</p>"))
        self.TextLabel5.setText(_translate("HgOptionsDialog", "Commit &Message:"))
        self.vcsLogEdit.setToolTip(_translate("HgOptionsDialog", "Enter the log message for the new project."))
        self.vcsLogEdit.setWhatsThis(_translate("HgOptionsDialog", "<b>Log Message</b>\n"
"<p>Enter the log message to be used for the new project.</p>"))
        self.vcsLogEdit.setText(_translate("HgOptionsDialog", "new project started"))
