# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsMercurial/HgMultiRevisionSelectionDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgMultiRevisionSelectionDialog(object):
    def setupUi(self, HgMultiRevisionSelectionDialog):
        HgMultiRevisionSelectionDialog.setObjectName("HgMultiRevisionSelectionDialog")
        HgMultiRevisionSelectionDialog.resize(450, 338)
        HgMultiRevisionSelectionDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgMultiRevisionSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(parent=HgMultiRevisionSelectionDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.changesetsButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.changesetsButton.setChecked(True)
        self.changesetsButton.setObjectName("changesetsButton")
        self.gridLayout.addWidget(self.changesetsButton, 0, 0, 1, 1)
        self.changesetsEdit = QtWidgets.QPlainTextEdit(parent=self.groupBox)
        self.changesetsEdit.setTabChangesFocus(True)
        self.changesetsEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        self.changesetsEdit.setObjectName("changesetsEdit")
        self.gridLayout.addWidget(self.changesetsEdit, 0, 1, 1, 1)
        self.tagButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.tagButton.setObjectName("tagButton")
        self.gridLayout.addWidget(self.tagButton, 1, 0, 1, 1)
        self.tagCombo = QtWidgets.QComboBox(parent=self.groupBox)
        self.tagCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagCombo.sizePolicy().hasHeightForWidth())
        self.tagCombo.setSizePolicy(sizePolicy)
        self.tagCombo.setEditable(True)
        self.tagCombo.setObjectName("tagCombo")
        self.gridLayout.addWidget(self.tagCombo, 1, 1, 1, 1)
        self.branchButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.branchButton.setObjectName("branchButton")
        self.gridLayout.addWidget(self.branchButton, 2, 0, 1, 1)
        self.branchCombo = QtWidgets.QComboBox(parent=self.groupBox)
        self.branchCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.branchCombo.sizePolicy().hasHeightForWidth())
        self.branchCombo.setSizePolicy(sizePolicy)
        self.branchCombo.setEditable(True)
        self.branchCombo.setObjectName("branchCombo")
        self.gridLayout.addWidget(self.branchCombo, 2, 1, 1, 1)
        self.bookmarkButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.bookmarkButton.setObjectName("bookmarkButton")
        self.gridLayout.addWidget(self.bookmarkButton, 3, 0, 1, 1)
        self.bookmarkCombo = QtWidgets.QComboBox(parent=self.groupBox)
        self.bookmarkCombo.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarkCombo.sizePolicy().hasHeightForWidth())
        self.bookmarkCombo.setSizePolicy(sizePolicy)
        self.bookmarkCombo.setEditable(True)
        self.bookmarkCombo.setObjectName("bookmarkCombo")
        self.gridLayout.addWidget(self.bookmarkCombo, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.limitGroup = QtWidgets.QGroupBox(parent=HgMultiRevisionSelectionDialog)
        self.limitGroup.setCheckable(True)
        self.limitGroup.setChecked(False)
        self.limitGroup.setObjectName("limitGroup")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.limitGroup)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.limitGroup)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.limitSpinBox = QtWidgets.QSpinBox(parent=self.limitGroup)
        self.limitSpinBox.setToolTip("")
        self.limitSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.limitSpinBox.setMinimum(1)
        self.limitSpinBox.setMaximum(9999)
        self.limitSpinBox.setObjectName("limitSpinBox")
        self.horizontalLayout.addWidget(self.limitSpinBox)
        spacerItem = QtWidgets.QSpacerItem(164, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.limitGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=HgMultiRevisionSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgMultiRevisionSelectionDialog)
        self.buttonBox.accepted.connect(HgMultiRevisionSelectionDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgMultiRevisionSelectionDialog.reject) # type: ignore
        self.tagButton.toggled['bool'].connect(self.tagCombo.setEnabled) # type: ignore
        self.branchButton.toggled['bool'].connect(self.branchCombo.setEnabled) # type: ignore
        self.bookmarkButton.toggled['bool'].connect(self.bookmarkCombo.setEnabled) # type: ignore
        self.changesetsButton.toggled['bool'].connect(self.changesetsEdit.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgMultiRevisionSelectionDialog)
        HgMultiRevisionSelectionDialog.setTabOrder(self.changesetsButton, self.changesetsEdit)
        HgMultiRevisionSelectionDialog.setTabOrder(self.changesetsEdit, self.tagButton)
        HgMultiRevisionSelectionDialog.setTabOrder(self.tagButton, self.tagCombo)
        HgMultiRevisionSelectionDialog.setTabOrder(self.tagCombo, self.branchButton)
        HgMultiRevisionSelectionDialog.setTabOrder(self.branchButton, self.branchCombo)
        HgMultiRevisionSelectionDialog.setTabOrder(self.branchCombo, self.bookmarkButton)
        HgMultiRevisionSelectionDialog.setTabOrder(self.bookmarkButton, self.bookmarkCombo)
        HgMultiRevisionSelectionDialog.setTabOrder(self.bookmarkCombo, self.limitGroup)
        HgMultiRevisionSelectionDialog.setTabOrder(self.limitGroup, self.limitSpinBox)
        HgMultiRevisionSelectionDialog.setTabOrder(self.limitSpinBox, self.buttonBox)

    def retranslateUi(self, HgMultiRevisionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        HgMultiRevisionSelectionDialog.setWindowTitle(_translate("HgMultiRevisionSelectionDialog", "Mercurial Revisions"))
        self.groupBox.setTitle(_translate("HgMultiRevisionSelectionDialog", "Revision"))
        self.changesetsButton.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Select to specify a list of changesets"))
        self.changesetsButton.setText(_translate("HgMultiRevisionSelectionDialog", "Revisions:"))
        self.changesetsEdit.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Enter revisions by number, id, range or revset expression one per line"))
        self.tagButton.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Select to specify a revision by a tag"))
        self.tagButton.setText(_translate("HgMultiRevisionSelectionDialog", "Tag:"))
        self.tagCombo.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Enter a tag name"))
        self.branchButton.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Select to specify a revision by a branch"))
        self.branchButton.setText(_translate("HgMultiRevisionSelectionDialog", "Branch:"))
        self.branchCombo.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Enter a branch name"))
        self.bookmarkButton.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Select to specify a revision by a bookmark"))
        self.bookmarkButton.setText(_translate("HgMultiRevisionSelectionDialog", "Bookmark:"))
        self.bookmarkCombo.setToolTip(_translate("HgMultiRevisionSelectionDialog", "Enter a bookmark name"))
        self.limitGroup.setTitle(_translate("HgMultiRevisionSelectionDialog", "Limit Results"))
        self.label.setText(_translate("HgMultiRevisionSelectionDialog", "Enter number of entries to show:"))
