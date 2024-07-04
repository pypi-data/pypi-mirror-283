# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsPySvn/SvnMergeDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SvnMergeDialog(object):
    def setupUi(self, SvnMergeDialog):
        SvnMergeDialog.setObjectName("SvnMergeDialog")
        SvnMergeDialog.resize(456, 152)
        SvnMergeDialog.setSizeGripEnabled(True)
        self.gridlayout = QtWidgets.QGridLayout(SvnMergeDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.forceCheckBox = QtWidgets.QCheckBox(parent=SvnMergeDialog)
        self.forceCheckBox.setObjectName("forceCheckBox")
        self.gridlayout.addWidget(self.forceCheckBox, 3, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SvnMergeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.textLabel1 = QtWidgets.QLabel(parent=SvnMergeDialog)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout.addWidget(self.textLabel1, 2, 0, 1, 1)
        self.targetCombo = QtWidgets.QComboBox(parent=SvnMergeDialog)
        self.targetCombo.setEditable(True)
        self.targetCombo.setInsertPolicy(QtWidgets.QComboBox.InsertPolicy.InsertAtTop)
        self.targetCombo.setDuplicatesEnabled(False)
        self.targetCombo.setObjectName("targetCombo")
        self.gridlayout.addWidget(self.targetCombo, 2, 1, 1, 1)
        self.tag2Combo = QtWidgets.QComboBox(parent=SvnMergeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tag2Combo.sizePolicy().hasHeightForWidth())
        self.tag2Combo.setSizePolicy(sizePolicy)
        self.tag2Combo.setEditable(True)
        self.tag2Combo.setDuplicatesEnabled(False)
        self.tag2Combo.setObjectName("tag2Combo")
        self.gridlayout.addWidget(self.tag2Combo, 1, 1, 1, 1)
        self.tag1Combo = QtWidgets.QComboBox(parent=SvnMergeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tag1Combo.sizePolicy().hasHeightForWidth())
        self.tag1Combo.setSizePolicy(sizePolicy)
        self.tag1Combo.setEditable(True)
        self.tag1Combo.setDuplicatesEnabled(False)
        self.tag1Combo.setObjectName("tag1Combo")
        self.gridlayout.addWidget(self.tag1Combo, 0, 1, 1, 1)
        self.TextLabel1_2 = QtWidgets.QLabel(parent=SvnMergeDialog)
        self.TextLabel1_2.setObjectName("TextLabel1_2")
        self.gridlayout.addWidget(self.TextLabel1_2, 1, 0, 1, 1)
        self.TextLabel1 = QtWidgets.QLabel(parent=SvnMergeDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.gridlayout.addWidget(self.TextLabel1, 0, 0, 1, 1)

        self.retranslateUi(SvnMergeDialog)
        self.buttonBox.accepted.connect(SvnMergeDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SvnMergeDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SvnMergeDialog)
        SvnMergeDialog.setTabOrder(self.tag1Combo, self.tag2Combo)
        SvnMergeDialog.setTabOrder(self.tag2Combo, self.targetCombo)
        SvnMergeDialog.setTabOrder(self.targetCombo, self.forceCheckBox)
        SvnMergeDialog.setTabOrder(self.forceCheckBox, self.buttonBox)

    def retranslateUi(self, SvnMergeDialog):
        _translate = QtCore.QCoreApplication.translate
        SvnMergeDialog.setWindowTitle(_translate("SvnMergeDialog", "Subversion Merge"))
        self.forceCheckBox.setToolTip(_translate("SvnMergeDialog", "Select to force the merge operation"))
        self.forceCheckBox.setText(_translate("SvnMergeDialog", "Enforce merge"))
        self.textLabel1.setText(_translate("SvnMergeDialog", "Target:"))
        self.targetCombo.setToolTip(_translate("SvnMergeDialog", "Enter the target"))
        self.targetCombo.setWhatsThis(_translate("SvnMergeDialog", "<b>Target</b>\n"
"<p>Enter the target for the merge operation into this field. Leave it empty to\n"
"get the target URL from the working copy.</p>\n"
"<p><b>Note:</b> This entry is only needed, if you enter revision numbers above.</p>"))
        self.tag2Combo.setToolTip(_translate("SvnMergeDialog", "Enter an URL or a revision number"))
        self.tag2Combo.setWhatsThis(_translate("SvnMergeDialog", "<b>URL/Revision</b>\n"
"<p>Enter an URL or a revision number to be merged into\n"
"the working copy.</p>"))
        self.tag1Combo.setToolTip(_translate("SvnMergeDialog", "Enter an URL or a revision number"))
        self.tag1Combo.setWhatsThis(_translate("SvnMergeDialog", "<b>URL/Revision</b>\n"
"<p>Enter an URL or a revision number to be merged into\n"
"the working copy.</p>"))
        self.TextLabel1_2.setText(_translate("SvnMergeDialog", "2. URL/Revision:"))
        self.TextLabel1.setText(_translate("SvnMergeDialog", "1. URL/Revision:"))
