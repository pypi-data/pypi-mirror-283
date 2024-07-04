# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsGit/GitBisectStartDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitBisectStartDialog(object):
    def setupUi(self, GitBisectStartDialog):
        GitBisectStartDialog.setObjectName("GitBisectStartDialog")
        GitBisectStartDialog.resize(450, 117)
        GitBisectStartDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(GitBisectStartDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=GitBisectStartDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.badEdit = QtWidgets.QLineEdit(parent=GitBisectStartDialog)
        self.badEdit.setObjectName("badEdit")
        self.gridLayout.addWidget(self.badEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=GitBisectStartDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.goodEdit = QtWidgets.QLineEdit(parent=GitBisectStartDialog)
        self.goodEdit.setObjectName("goodEdit")
        self.gridLayout.addWidget(self.goodEdit, 1, 1, 1, 1)
        self.noCheckoutCheckBox = QtWidgets.QCheckBox(parent=GitBisectStartDialog)
        self.noCheckoutCheckBox.setObjectName("noCheckoutCheckBox")
        self.gridLayout.addWidget(self.noCheckoutCheckBox, 2, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GitBisectStartDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.retranslateUi(GitBisectStartDialog)
        self.buttonBox.accepted.connect(GitBisectStartDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GitBisectStartDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitBisectStartDialog)

    def retranslateUi(self, GitBisectStartDialog):
        _translate = QtCore.QCoreApplication.translate
        GitBisectStartDialog.setWindowTitle(_translate("GitBisectStartDialog", "Git Bisect Start"))
        self.label.setText(_translate("GitBisectStartDialog", "Bad Commit:"))
        self.badEdit.setToolTip(_translate("GitBisectStartDialog", "Enter a bad commit"))
        self.label_2.setText(_translate("GitBisectStartDialog", "Good Commits:"))
        self.goodEdit.setToolTip(_translate("GitBisectStartDialog", "Enter a list of good commits separated by space"))
        self.noCheckoutCheckBox.setToolTip(_translate("GitBisectStartDialog", "Select to not checkout the working tree"))
        self.noCheckoutCheckBox.setText(_translate("GitBisectStartDialog", "Don\'t checkout working tree"))
