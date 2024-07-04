# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsMercurial/HgImportDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgImportDialog(object):
    def setupUi(self, HgImportDialog):
        HgImportDialog.setObjectName("HgImportDialog")
        HgImportDialog.resize(500, 450)
        HgImportDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(HgImportDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(parent=HgImportDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.noCommitCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.noCommitCheckBox.setChecked(True)
        self.noCommitCheckBox.setObjectName("noCommitCheckBox")
        self.verticalLayout.addWidget(self.noCommitCheckBox)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.messageEdit = EricSpellCheckedPlainTextEdit(parent=self.groupBox_2)
        self.messageEdit.setEnabled(False)
        self.messageEdit.setTabChangesFocus(True)
        self.messageEdit.setObjectName("messageEdit")
        self.verticalLayout.addWidget(self.messageEdit)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dateEdit = QtWidgets.QDateTimeEdit(parent=self.groupBox_2)
        self.dateEdit.setEnabled(False)
        self.dateEdit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dateEdit.setCalendarPopup(False)
        self.dateEdit.setObjectName("dateEdit")
        self.gridLayout.addWidget(self.dateEdit, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(258, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.userEdit = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.userEdit.setEnabled(False)
        self.userEdit.setObjectName("userEdit")
        self.gridLayout.addWidget(self.userEdit, 1, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.secretCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.secretCheckBox.setObjectName("secretCheckBox")
        self.verticalLayout.addWidget(self.secretCheckBox)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(parent=HgImportDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stripSpinBox = QtWidgets.QSpinBox(parent=HgImportDialog)
        self.stripSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.stripSpinBox.setMaximum(9)
        self.stripSpinBox.setProperty("value", 1)
        self.stripSpinBox.setObjectName("stripSpinBox")
        self.horizontalLayout.addWidget(self.stripSpinBox)
        spacerItem1 = QtWidgets.QSpacerItem(118, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=HgImportDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.patchFilePicker = EricPathPicker(parent=HgImportDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.patchFilePicker.sizePolicy().hasHeightForWidth())
        self.patchFilePicker.setSizePolicy(sizePolicy)
        self.patchFilePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.patchFilePicker.setObjectName("patchFilePicker")
        self.gridLayout_2.addWidget(self.patchFilePicker, 2, 1, 1, 1)
        self.forceCheckBox = QtWidgets.QCheckBox(parent=HgImportDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.gridLayout_2.addWidget(self.forceCheckBox, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=HgImportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.retranslateUi(HgImportDialog)
        self.buttonBox.accepted.connect(HgImportDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgImportDialog.reject) # type: ignore
        self.noCommitCheckBox.toggled['bool'].connect(self.messageEdit.setDisabled) # type: ignore
        self.noCommitCheckBox.toggled['bool'].connect(self.dateEdit.setDisabled) # type: ignore
        self.noCommitCheckBox.toggled['bool'].connect(self.userEdit.setDisabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgImportDialog)
        HgImportDialog.setTabOrder(self.noCommitCheckBox, self.messageEdit)
        HgImportDialog.setTabOrder(self.messageEdit, self.dateEdit)
        HgImportDialog.setTabOrder(self.dateEdit, self.userEdit)
        HgImportDialog.setTabOrder(self.userEdit, self.secretCheckBox)
        HgImportDialog.setTabOrder(self.secretCheckBox, self.stripSpinBox)
        HgImportDialog.setTabOrder(self.stripSpinBox, self.patchFilePicker)
        HgImportDialog.setTabOrder(self.patchFilePicker, self.forceCheckBox)

    def retranslateUi(self, HgImportDialog):
        _translate = QtCore.QCoreApplication.translate
        HgImportDialog.setWindowTitle(_translate("HgImportDialog", "Import Patch"))
        self.groupBox_2.setTitle(_translate("HgImportDialog", "Commit data"))
        self.noCommitCheckBox.setToolTip(_translate("HgImportDialog", "Select to not commit the imported patch"))
        self.noCommitCheckBox.setText(_translate("HgImportDialog", "Do not commit"))
        self.label_3.setText(_translate("HgImportDialog", "Commit message:"))
        self.messageEdit.setToolTip(_translate("HgImportDialog", "Enter the commit message or leave empty to use the default one"))
        self.label.setText(_translate("HgImportDialog", "Commit Date:"))
        self.dateEdit.setToolTip(_translate("HgImportDialog", "Enter optional date for the commit"))
        self.label_2.setText(_translate("HgImportDialog", "Commit User:"))
        self.userEdit.setToolTip(_translate("HgImportDialog", "Enter optional user for the commit"))
        self.secretCheckBox.setToolTip(_translate("HgImportDialog", "Enable to commit with the secret phase"))
        self.secretCheckBox.setText(_translate("HgImportDialog", "Commit with Secret Phase"))
        self.label_4.setText(_translate("HgImportDialog", "Strip Count:"))
        self.stripSpinBox.setToolTip(_translate("HgImportDialog", "Enter number of leading directories to strip off (default 1)"))
        self.label_5.setText(_translate("HgImportDialog", "Patch File:"))
        self.patchFilePicker.setToolTip(_translate("HgImportDialog", "Enter the name of the patch file"))
        self.forceCheckBox.setToolTip(_translate("HgImportDialog", "Select to enforce the import"))
        self.forceCheckBox.setText(_translate("HgImportDialog", "Enforce Import"))
from eric7.EricWidgets.EricPathPicker import EricPathPicker
from eric7.EricWidgets.EricSpellCheckedTextEdit import EricSpellCheckedPlainTextEdit
