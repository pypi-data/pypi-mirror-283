# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsGit/GitChangeRemoteUrlDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitChangeRemoteUrlDialog(object):
    def setupUi(self, GitChangeRemoteUrlDialog):
        GitChangeRemoteUrlDialog.setObjectName("GitChangeRemoteUrlDialog")
        GitChangeRemoteUrlDialog.resize(700, 140)
        GitChangeRemoteUrlDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitChangeRemoteUrlDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=GitChangeRemoteUrlDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.nameEdit = QtWidgets.QLineEdit(parent=GitChangeRemoteUrlDialog)
        self.nameEdit.setToolTip("")
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName("nameEdit")
        self.gridLayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=GitChangeRemoteUrlDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.urlEdit = QtWidgets.QLineEdit(parent=GitChangeRemoteUrlDialog)
        self.urlEdit.setToolTip("")
        self.urlEdit.setReadOnly(True)
        self.urlEdit.setObjectName("urlEdit")
        self.gridLayout.addWidget(self.urlEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=GitChangeRemoteUrlDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.newUrlEdit = QtWidgets.QLineEdit(parent=GitChangeRemoteUrlDialog)
        self.newUrlEdit.setObjectName("newUrlEdit")
        self.gridLayout.addWidget(self.newUrlEdit, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GitChangeRemoteUrlDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GitChangeRemoteUrlDialog)
        self.buttonBox.accepted.connect(GitChangeRemoteUrlDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GitChangeRemoteUrlDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitChangeRemoteUrlDialog)

    def retranslateUi(self, GitChangeRemoteUrlDialog):
        _translate = QtCore.QCoreApplication.translate
        GitChangeRemoteUrlDialog.setWindowTitle(_translate("GitChangeRemoteUrlDialog", "Git Change Remote URL"))
        self.label.setText(_translate("GitChangeRemoteUrlDialog", "Name:"))
        self.label_2.setText(_translate("GitChangeRemoteUrlDialog", "URL:"))
        self.label_3.setText(_translate("GitChangeRemoteUrlDialog", "New URL:"))
        self.newUrlEdit.setToolTip(_translate("GitChangeRemoteUrlDialog", "Enter the new remote URL"))
