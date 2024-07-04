# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsGit/GitWorktreeDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GitWorktreeDialog(object):
    def setupUi(self, GitWorktreeDialog):
        GitWorktreeDialog.setObjectName("GitWorktreeDialog")
        GitWorktreeDialog.resize(800, 500)
        GitWorktreeDialog.setProperty("sizeGripEnabled", True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GitWorktreeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.actionsButton = QtWidgets.QToolButton(parent=GitWorktreeDialog)
        self.actionsButton.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        self.actionsButton.setObjectName("actionsButton")
        self.horizontalLayout.addWidget(self.actionsButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.expireCheckBox = QtWidgets.QCheckBox(parent=GitWorktreeDialog)
        self.expireCheckBox.setObjectName("expireCheckBox")
        self.horizontalLayout.addWidget(self.expireCheckBox)
        self.expireDateTimeEdit = QtWidgets.QDateTimeEdit(parent=GitWorktreeDialog)
        self.expireDateTimeEdit.setEnabled(False)
        self.expireDateTimeEdit.setCalendarPopup(True)
        self.expireDateTimeEdit.setObjectName("expireDateTimeEdit")
        self.horizontalLayout.addWidget(self.expireDateTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.worktreeList = QtWidgets.QTreeWidget(parent=GitWorktreeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.worktreeList.sizePolicy().hasHeightForWidth())
        self.worktreeList.setSizePolicy(sizePolicy)
        self.worktreeList.setAlternatingRowColors(True)
        self.worktreeList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.worktreeList.setRootIsDecorated(False)
        self.worktreeList.setItemsExpandable(False)
        self.worktreeList.setExpandsOnDoubleClick(False)
        self.worktreeList.setObjectName("worktreeList")
        self.verticalLayout.addWidget(self.worktreeList)
        self.errorGroup = QtWidgets.QGroupBox(parent=GitWorktreeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self._2 = QtWidgets.QVBoxLayout(self.errorGroup)
        self._2.setObjectName("_2")
        self.errors = QtWidgets.QTextEdit(parent=self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self._2.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GitWorktreeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GitWorktreeDialog)
        self.expireCheckBox.toggled['bool'].connect(self.expireDateTimeEdit.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GitWorktreeDialog)
        GitWorktreeDialog.setTabOrder(self.actionsButton, self.expireCheckBox)
        GitWorktreeDialog.setTabOrder(self.expireCheckBox, self.expireDateTimeEdit)
        GitWorktreeDialog.setTabOrder(self.expireDateTimeEdit, self.worktreeList)
        GitWorktreeDialog.setTabOrder(self.worktreeList, self.errors)

    def retranslateUi(self, GitWorktreeDialog):
        _translate = QtCore.QCoreApplication.translate
        GitWorktreeDialog.setWindowTitle(_translate("GitWorktreeDialog", "Git Worktree"))
        self.actionsButton.setToolTip(_translate("GitWorktreeDialog", "Select action from menu"))
        self.expireCheckBox.setToolTip(_translate("GitWorktreeDialog", "Select to annotate missing worktrees older than the entered date and time as prunable."))
        self.expireCheckBox.setText(_translate("GitWorktreeDialog", "Expire:"))
        self.expireDateTimeEdit.setToolTip(_translate("GitWorktreeDialog", "All missing worktrees older than the entered date and time will be annotated as prunable."))
        self.expireDateTimeEdit.setDisplayFormat(_translate("GitWorktreeDialog", "yyyy-MM-dd HH:mm:ss"))
        self.worktreeList.setSortingEnabled(True)
        self.worktreeList.headerItem().setText(0, _translate("GitWorktreeDialog", "Name"))
        self.worktreeList.headerItem().setText(1, _translate("GitWorktreeDialog", "Path"))
        self.worktreeList.headerItem().setText(2, _translate("GitWorktreeDialog", "Commit"))
        self.worktreeList.headerItem().setText(3, _translate("GitWorktreeDialog", "Branch"))
        self.errorGroup.setTitle(_translate("GitWorktreeDialog", "Errors"))
