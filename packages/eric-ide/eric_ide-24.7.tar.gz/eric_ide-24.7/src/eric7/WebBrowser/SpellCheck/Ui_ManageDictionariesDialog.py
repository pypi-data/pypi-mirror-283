# Form implementation generated from reading ui file 'src/eric7/WebBrowser/SpellCheck/ManageDictionariesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ManageDictionariesDialog(object):
    def setupUi(self, ManageDictionariesDialog):
        ManageDictionariesDialog.setObjectName("ManageDictionariesDialog")
        ManageDictionariesDialog.resize(676, 653)
        ManageDictionariesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ManageDictionariesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(parent=ManageDictionariesDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.locationComboBox = QtWidgets.QComboBox(parent=ManageDictionariesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.locationComboBox.sizePolicy().hasHeightForWidth())
        self.locationComboBox.setSizePolicy(sizePolicy)
        self.locationComboBox.setObjectName("locationComboBox")
        self.horizontalLayout_2.addWidget(self.locationComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.dictionariesList = QtWidgets.QListWidget(parent=ManageDictionariesDialog)
        self.dictionariesList.setAlternatingRowColors(True)
        self.dictionariesList.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.dictionariesList.setObjectName("dictionariesList")
        self.verticalLayout.addWidget(self.dictionariesList)
        self.line = QtWidgets.QFrame(parent=ManageDictionariesDialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.downloadProgress = QtWidgets.QProgressBar(parent=ManageDictionariesDialog)
        self.downloadProgress.setProperty("value", 0)
        self.downloadProgress.setObjectName("downloadProgress")
        self.verticalLayout.addWidget(self.downloadProgress)
        self.statusLabel = QtWidgets.QLabel(parent=ManageDictionariesDialog)
        self.statusLabel.setText("")
        self.statusLabel.setObjectName("statusLabel")
        self.verticalLayout.addWidget(self.statusLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(parent=ManageDictionariesDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.dictionariesUrlEdit = QtWidgets.QLineEdit(parent=ManageDictionariesDialog)
        self.dictionariesUrlEdit.setReadOnly(True)
        self.dictionariesUrlEdit.setObjectName("dictionariesUrlEdit")
        self.horizontalLayout.addWidget(self.dictionariesUrlEdit)
        self.dictionariesUrlEditButton = QtWidgets.QPushButton(parent=ManageDictionariesDialog)
        self.dictionariesUrlEditButton.setCheckable(True)
        self.dictionariesUrlEditButton.setObjectName("dictionariesUrlEditButton")
        self.horizontalLayout.addWidget(self.dictionariesUrlEditButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=ManageDictionariesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ManageDictionariesDialog)
        self.buttonBox.accepted.connect(ManageDictionariesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(ManageDictionariesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ManageDictionariesDialog)
        ManageDictionariesDialog.setTabOrder(self.locationComboBox, self.dictionariesList)
        ManageDictionariesDialog.setTabOrder(self.dictionariesList, self.dictionariesUrlEdit)
        ManageDictionariesDialog.setTabOrder(self.dictionariesUrlEdit, self.dictionariesUrlEditButton)

    def retranslateUi(self, ManageDictionariesDialog):
        _translate = QtCore.QCoreApplication.translate
        ManageDictionariesDialog.setWindowTitle(_translate("ManageDictionariesDialog", "Spell Check Dictionaries"))
        self.label.setText(_translate("ManageDictionariesDialog", "Installation Location:"))
        self.locationComboBox.setToolTip(_translate("ManageDictionariesDialog", "Select the location for the dictionaries installation"))
        self.dictionariesList.setToolTip(_translate("ManageDictionariesDialog", "Shows the list of available dictionaries"))
        self.dictionariesList.setSortingEnabled(True)
        self.downloadProgress.setToolTip(_translate("ManageDictionariesDialog", "Shows the progress of the current download"))
        self.label_4.setText(_translate("ManageDictionariesDialog", "Dictionaries URL:"))
        self.dictionariesUrlEdit.setToolTip(_translate("ManageDictionariesDialog", "Shows the dictionaries URL"))
        self.dictionariesUrlEditButton.setToolTip(_translate("ManageDictionariesDialog", "Press to edit the dictionaries URL"))
        self.dictionariesUrlEditButton.setText(_translate("ManageDictionariesDialog", "Edit URL"))
