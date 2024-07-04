# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsMercurial/QueuesExtension/HgQueuesFoldDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgQueuesFoldDialog(object):
    def setupUi(self, HgQueuesFoldDialog):
        HgQueuesFoldDialog.setObjectName("HgQueuesFoldDialog")
        HgQueuesFoldDialog.resize(450, 600)
        HgQueuesFoldDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(HgQueuesFoldDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=HgQueuesFoldDialog)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.messageEdit = EricSpellCheckedPlainTextEdit(parent=HgQueuesFoldDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.messageEdit.sizePolicy().hasHeightForWidth())
        self.messageEdit.setSizePolicy(sizePolicy)
        self.messageEdit.setTabChangesFocus(True)
        self.messageEdit.setObjectName("messageEdit")
        self.gridLayout.addWidget(self.messageEdit, 0, 1, 1, 1)
        self.sourcePatches = QtWidgets.QTreeWidget(parent=HgQueuesFoldDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sourcePatches.sizePolicy().hasHeightForWidth())
        self.sourcePatches.setSizePolicy(sizePolicy)
        self.sourcePatches.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sourcePatches.setAlternatingRowColors(True)
        self.sourcePatches.setRootIsDecorated(False)
        self.sourcePatches.setItemsExpandable(False)
        self.sourcePatches.setAllColumnsShowFocus(True)
        self.sourcePatches.setExpandsOnDoubleClick(False)
        self.sourcePatches.setObjectName("sourcePatches")
        self.gridLayout.addWidget(self.sourcePatches, 1, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QToolButton(parent=HgQueuesFoldDialog)
        self.addButton.setEnabled(False)
        self.addButton.setText("")
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtWidgets.QToolButton(parent=HgQueuesFoldDialog)
        self.removeButton.setEnabled(False)
        self.removeButton.setText("")
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.selectedPatches = QtWidgets.QTreeWidget(parent=HgQueuesFoldDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.selectedPatches.sizePolicy().hasHeightForWidth())
        self.selectedPatches.setSizePolicy(sizePolicy)
        self.selectedPatches.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.selectedPatches.setAlternatingRowColors(True)
        self.selectedPatches.setRootIsDecorated(False)
        self.selectedPatches.setItemsExpandable(False)
        self.selectedPatches.setExpandsOnDoubleClick(False)
        self.selectedPatches.setObjectName("selectedPatches")
        self.gridLayout.addWidget(self.selectedPatches, 3, 0, 1, 2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.upButton = QtWidgets.QToolButton(parent=HgQueuesFoldDialog)
        self.upButton.setEnabled(False)
        self.upButton.setText("")
        self.upButton.setObjectName("upButton")
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtWidgets.QToolButton(parent=HgQueuesFoldDialog)
        self.downButton.setEnabled(False)
        self.downButton.setText("")
        self.downButton.setObjectName("downButton")
        self.verticalLayout.addWidget(self.downButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.verticalLayout, 3, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=HgQueuesFoldDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)

        self.retranslateUi(HgQueuesFoldDialog)
        self.buttonBox.accepted.connect(HgQueuesFoldDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(HgQueuesFoldDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(HgQueuesFoldDialog)
        HgQueuesFoldDialog.setTabOrder(self.messageEdit, self.sourcePatches)
        HgQueuesFoldDialog.setTabOrder(self.sourcePatches, self.addButton)
        HgQueuesFoldDialog.setTabOrder(self.addButton, self.removeButton)
        HgQueuesFoldDialog.setTabOrder(self.removeButton, self.selectedPatches)
        HgQueuesFoldDialog.setTabOrder(self.selectedPatches, self.upButton)
        HgQueuesFoldDialog.setTabOrder(self.upButton, self.downButton)
        HgQueuesFoldDialog.setTabOrder(self.downButton, self.buttonBox)

    def retranslateUi(self, HgQueuesFoldDialog):
        _translate = QtCore.QCoreApplication.translate
        HgQueuesFoldDialog.setWindowTitle(_translate("HgQueuesFoldDialog", "Fold Patches"))
        self.label.setText(_translate("HgQueuesFoldDialog", "Message:"))
        self.messageEdit.setToolTip(_translate("HgQueuesFoldDialog", "Enter commit message for the folded patch"))
        self.sourcePatches.headerItem().setText(0, _translate("HgQueuesFoldDialog", "Name"))
        self.sourcePatches.headerItem().setText(1, _translate("HgQueuesFoldDialog", "Summary"))
        self.addButton.setToolTip(_translate("HgQueuesFoldDialog", "Press to add the selected entry to the list of selected patches"))
        self.removeButton.setToolTip(_translate("HgQueuesFoldDialog", "Press to remove the selected entry from the list of selected patches"))
        self.selectedPatches.headerItem().setText(0, _translate("HgQueuesFoldDialog", "Name"))
        self.selectedPatches.headerItem().setText(1, _translate("HgQueuesFoldDialog", "Summary"))
        self.upButton.setToolTip(_translate("HgQueuesFoldDialog", "Press to move the selected patch up"))
        self.downButton.setToolTip(_translate("HgQueuesFoldDialog", "Press to move the selected patch down"))
from eric7.EricWidgets.EricSpellCheckedTextEdit import EricSpellCheckedPlainTextEdit
