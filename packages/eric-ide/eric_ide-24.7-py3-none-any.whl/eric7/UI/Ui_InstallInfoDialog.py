# Form implementation generated from reading ui file 'src/eric7/UI/InstallInfoDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_InstallInfoDialog(object):
    def setupUi(self, InstallInfoDialog):
        InstallInfoDialog.setObjectName("InstallInfoDialog")
        InstallInfoDialog.resize(800, 500)
        InstallInfoDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(InstallInfoDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(749, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.editButton = QtWidgets.QToolButton(parent=InstallInfoDialog)
        self.editButton.setCheckable(True)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_2.addWidget(self.editButton)
        self.saveButton = QtWidgets.QToolButton(parent=InstallInfoDialog)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.commandEdit = QtWidgets.QLineEdit(parent=InstallInfoDialog)
        self.commandEdit.setReadOnly(True)
        self.commandEdit.setObjectName("commandEdit")
        self.gridLayout.addWidget(self.commandEdit, 4, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)
        self.installedFromEdit = QtWidgets.QLineEdit(parent=InstallInfoDialog)
        self.installedFromEdit.setReadOnly(True)
        self.installedFromEdit.setObjectName("installedFromEdit")
        self.gridLayout.addWidget(self.installedFromEdit, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.virtenvLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.virtenvLabel.setText("")
        self.virtenvLabel.setObjectName("virtenvLabel")
        self.gridLayout.addWidget(self.virtenvLabel, 6, 1, 1, 1)
        self.sudoLabel1 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.sudoLabel1.setText("")
        self.sudoLabel1.setObjectName("sudoLabel1")
        self.gridLayout.addWidget(self.sudoLabel1, 0, 0, 1, 1)
        self.sudoLabel2 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.sudoLabel2.setObjectName("sudoLabel2")
        self.gridLayout.addWidget(self.sudoLabel2, 0, 1, 1, 1)
        self.installDateTimeLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.installDateTimeLabel.setObjectName("installDateTimeLabel")
        self.gridLayout.addWidget(self.installDateTimeLabel, 7, 1, 1, 1)
        self.userLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.userLabel.setObjectName("userLabel")
        self.gridLayout.addWidget(self.userLabel, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.interpreteEdit = QtWidgets.QLineEdit(parent=InstallInfoDialog)
        self.interpreteEdit.setReadOnly(True)
        self.interpreteEdit.setObjectName("interpreteEdit")
        self.gridLayout.addWidget(self.interpreteEdit, 3, 1, 1, 1)
        self.installPathEdit = QtWidgets.QLineEdit(parent=InstallInfoDialog)
        self.installPathEdit.setReadOnly(True)
        self.installPathEdit.setObjectName("installPathEdit")
        self.gridLayout.addWidget(self.installPathEdit, 5, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 7, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.pipLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.pipLabel.setWordWrap(True)
        self.pipLabel.setObjectName("pipLabel")
        self.verticalLayout.addWidget(self.pipLabel)
        self.guessLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.guessLabel.setWordWrap(True)
        self.guessLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.guessLabel.setObjectName("guessLabel")
        self.verticalLayout.addWidget(self.guessLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.remarksEdit = EricSpellCheckedPlainTextEdit(parent=InstallInfoDialog)
        self.remarksEdit.setToolTip("")
        self.remarksEdit.setReadOnly(True)
        self.remarksEdit.setObjectName("remarksEdit")
        self.horizontalLayout.addWidget(self.remarksEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.userProvidedLabel = QtWidgets.QLabel(parent=InstallInfoDialog)
        self.userProvidedLabel.setText("")
        self.userProvidedLabel.setObjectName("userProvidedLabel")
        self.verticalLayout.addWidget(self.userProvidedLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=InstallInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InstallInfoDialog)
        self.buttonBox.accepted.connect(InstallInfoDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(InstallInfoDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(InstallInfoDialog)
        InstallInfoDialog.setTabOrder(self.installedFromEdit, self.interpreteEdit)
        InstallInfoDialog.setTabOrder(self.interpreteEdit, self.commandEdit)
        InstallInfoDialog.setTabOrder(self.commandEdit, self.installPathEdit)
        InstallInfoDialog.setTabOrder(self.installPathEdit, self.remarksEdit)
        InstallInfoDialog.setTabOrder(self.remarksEdit, self.editButton)
        InstallInfoDialog.setTabOrder(self.editButton, self.saveButton)

    def retranslateUi(self, InstallInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        InstallInfoDialog.setWindowTitle(_translate("InstallInfoDialog", "Installation Information"))
        self.editButton.setToolTip(_translate("InstallInfoDialog", "Press to change to edit mode"))
        self.saveButton.setToolTip(_translate("InstallInfoDialog", "Press to save the changed information"))
        self.label_8.setText(_translate("InstallInfoDialog", "Installed From:"))
        self.label_5.setText(_translate("InstallInfoDialog", "Installed in VirtualEnv:"))
        self.label_2.setText(_translate("InstallInfoDialog", "User name of installer:"))
        self.label_3.setText(_translate("InstallInfoDialog", "Install Command:"))
        self.label_4.setText(_translate("InstallInfoDialog", "Installation Path:"))
        self.label_7.setText(_translate("InstallInfoDialog", "Python Interpreter:"))
        self.label.setText(_translate("InstallInfoDialog", "Installation Date:"))
        self.label_6.setText(_translate("InstallInfoDialog", "Remarks:"))
from eric7.EricWidgets.EricSpellCheckedTextEdit import EricSpellCheckedPlainTextEdit
