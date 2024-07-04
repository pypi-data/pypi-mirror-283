# Form implementation generated from reading ui file 'src/eric7/WebBrowser/SafeBrowsing/SafeBrowsingDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SafeBrowsingDialog(object):
    def setupUi(self, SafeBrowsingDialog):
        SafeBrowsingDialog.setObjectName("SafeBrowsingDialog")
        SafeBrowsingDialog.resize(650, 597)
        SafeBrowsingDialog.setSizeGripEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(SafeBrowsingDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.iconLabel = QtWidgets.QLabel(parent=SafeBrowsingDialog)
        self.iconLabel.setMinimumSize(QtCore.QSize(48, 48))
        self.iconLabel.setText("Icon")
        self.iconLabel.setObjectName("iconLabel")
        self.horizontalLayout_3.addWidget(self.iconLabel)
        self.label_2 = QtWidgets.QLabel(parent=SafeBrowsingDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gsbGroupBox = QtWidgets.QGroupBox(parent=SafeBrowsingDialog)
        self.gsbGroupBox.setCheckable(True)
        self.gsbGroupBox.setObjectName("gsbGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gsbGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gsbFilterPlatformCheckBox = QtWidgets.QCheckBox(parent=self.gsbGroupBox)
        self.gsbFilterPlatformCheckBox.setObjectName("gsbFilterPlatformCheckBox")
        self.verticalLayout_2.addWidget(self.gsbFilterPlatformCheckBox)
        self.gsbAutoUpdateCheckBox = QtWidgets.QCheckBox(parent=self.gsbGroupBox)
        self.gsbAutoUpdateCheckBox.setObjectName("gsbAutoUpdateCheckBox")
        self.verticalLayout_2.addWidget(self.gsbAutoUpdateCheckBox)
        self.gsbLookupCheckBox = QtWidgets.QCheckBox(parent=self.gsbGroupBox)
        self.gsbLookupCheckBox.setObjectName("gsbLookupCheckBox")
        self.verticalLayout_2.addWidget(self.gsbLookupCheckBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_14 = QtWidgets.QLabel(parent=self.gsbGroupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_4.addWidget(self.label_14)
        self.gsbApiKeyEdit = QtWidgets.QLineEdit(parent=self.gsbGroupBox)
        self.gsbApiKeyEdit.setClearButtonEnabled(True)
        self.gsbApiKeyEdit.setObjectName("gsbApiKeyEdit")
        self.horizontalLayout_4.addWidget(self.gsbApiKeyEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gsbHelpButton = QtWidgets.QPushButton(parent=self.gsbGroupBox)
        self.gsbHelpButton.setObjectName("gsbHelpButton")
        self.verticalLayout_2.addWidget(self.gsbHelpButton)
        self.verticalLayout_3.addWidget(self.gsbGroupBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.saveButton = QtWidgets.QPushButton(parent=SafeBrowsingDialog)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(parent=SafeBrowsingDialog)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.manageCacheGroupBox = QtWidgets.QGroupBox(parent=SafeBrowsingDialog)
        self.manageCacheGroupBox.setObjectName("manageCacheGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.manageCacheGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateCacheButton = QtWidgets.QPushButton(parent=self.manageCacheGroupBox)
        self.updateCacheButton.setObjectName("updateCacheButton")
        self.horizontalLayout.addWidget(self.updateCacheButton)
        self.clearCacheButton = QtWidgets.QPushButton(parent=self.manageCacheGroupBox)
        self.clearCacheButton.setObjectName("clearCacheButton")
        self.horizontalLayout.addWidget(self.clearCacheButton)
        self.line_3 = QtWidgets.QFrame(parent=self.manageCacheGroupBox)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.showUpdateTimeButton = QtWidgets.QPushButton(parent=self.manageCacheGroupBox)
        self.showUpdateTimeButton.setObjectName("showUpdateTimeButton")
        self.horizontalLayout.addWidget(self.showUpdateTimeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressLabel = QtWidgets.QLabel(parent=self.manageCacheGroupBox)
        self.progressLabel.setText("")
        self.progressLabel.setWordWrap(True)
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout.addWidget(self.progressLabel)
        self.progressBar = QtWidgets.QProgressBar(parent=self.manageCacheGroupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.verticalLayout_3.addWidget(self.manageCacheGroupBox)
        self.line_2 = QtWidgets.QFrame(parent=SafeBrowsingDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=SafeBrowsingDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.urlEdit = QtWidgets.QLineEdit(parent=self.groupBox_2)
        self.urlEdit.setClearButtonEnabled(True)
        self.urlEdit.setObjectName("urlEdit")
        self.gridLayout_2.addWidget(self.urlEdit, 0, 1, 1, 1)
        self.urlCheckButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.urlCheckButton.setEnabled(False)
        self.urlCheckButton.setObjectName("urlCheckButton")
        self.gridLayout_2.addWidget(self.urlCheckButton, 1, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SafeBrowsingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(SafeBrowsingDialog)
        self.gsbLookupCheckBox.toggled['bool'].connect(self.manageCacheGroupBox.setDisabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SafeBrowsingDialog)
        SafeBrowsingDialog.setTabOrder(self.gsbGroupBox, self.gsbFilterPlatformCheckBox)
        SafeBrowsingDialog.setTabOrder(self.gsbFilterPlatformCheckBox, self.gsbAutoUpdateCheckBox)
        SafeBrowsingDialog.setTabOrder(self.gsbAutoUpdateCheckBox, self.gsbLookupCheckBox)
        SafeBrowsingDialog.setTabOrder(self.gsbLookupCheckBox, self.gsbApiKeyEdit)
        SafeBrowsingDialog.setTabOrder(self.gsbApiKeyEdit, self.gsbHelpButton)
        SafeBrowsingDialog.setTabOrder(self.gsbHelpButton, self.saveButton)
        SafeBrowsingDialog.setTabOrder(self.saveButton, self.updateCacheButton)
        SafeBrowsingDialog.setTabOrder(self.updateCacheButton, self.clearCacheButton)
        SafeBrowsingDialog.setTabOrder(self.clearCacheButton, self.showUpdateTimeButton)
        SafeBrowsingDialog.setTabOrder(self.showUpdateTimeButton, self.urlEdit)
        SafeBrowsingDialog.setTabOrder(self.urlEdit, self.urlCheckButton)

    def retranslateUi(self, SafeBrowsingDialog):
        _translate = QtCore.QCoreApplication.translate
        SafeBrowsingDialog.setWindowTitle(_translate("SafeBrowsingDialog", "Safe Browsing Management"))
        self.label_2.setText(_translate("SafeBrowsingDialog", "<h2>Google Safe Browsing</h2>"))
        self.gsbGroupBox.setToolTip(_translate("SafeBrowsingDialog", "Select to enable the Google safe browsing support"))
        self.gsbGroupBox.setTitle(_translate("SafeBrowsingDialog", "Enable Google Safe Browsing"))
        self.gsbFilterPlatformCheckBox.setToolTip(_translate("SafeBrowsingDialog", "Select to check against the current platform only"))
        self.gsbFilterPlatformCheckBox.setText(_translate("SafeBrowsingDialog", "Adjust threat lists to current platform"))
        self.gsbAutoUpdateCheckBox.setToolTip(_translate("SafeBrowsingDialog", "Select to update the threat lists automatically when fair use period has expired"))
        self.gsbAutoUpdateCheckBox.setText(_translate("SafeBrowsingDialog", "Update threat lists automatically (Update API only)"))
        self.gsbLookupCheckBox.setText(_translate("SafeBrowsingDialog", "Use \'Lookup API\' (Note: each URL is sent to Google for checking)"))
        self.label_14.setText(_translate("SafeBrowsingDialog", "API Key:"))
        self.gsbApiKeyEdit.setToolTip(_translate("SafeBrowsingDialog", "Enter the Google Safe Browsing API key"))
        self.gsbHelpButton.setToolTip(_translate("SafeBrowsingDialog", "Press to get some help about obtaining the API key"))
        self.gsbHelpButton.setText(_translate("SafeBrowsingDialog", "Google Safe Browsing API Help"))
        self.saveButton.setToolTip(_translate("SafeBrowsingDialog", "Press to save the current configuration settings"))
        self.saveButton.setText(_translate("SafeBrowsingDialog", "Save Configuration"))
        self.manageCacheGroupBox.setTitle(_translate("SafeBrowsingDialog", "Manage Local Cache (Update API only)"))
        self.updateCacheButton.setToolTip(_translate("SafeBrowsingDialog", "Press to update the local cache database"))
        self.updateCacheButton.setText(_translate("SafeBrowsingDialog", "Update Cache"))
        self.clearCacheButton.setToolTip(_translate("SafeBrowsingDialog", "Press to clear the local cache database"))
        self.clearCacheButton.setText(_translate("SafeBrowsingDialog", "Clear Cache"))
        self.showUpdateTimeButton.setToolTip(_translate("SafeBrowsingDialog", "Press to see, when the next threat list update will be done"))
        self.showUpdateTimeButton.setText(_translate("SafeBrowsingDialog", "Show Update Time"))
        self.progressBar.setFormat(_translate("SafeBrowsingDialog", "%v/%m"))
        self.groupBox_2.setTitle(_translate("SafeBrowsingDialog", "URL Check"))
        self.label.setText(_translate("SafeBrowsingDialog", "URL:"))
        self.urlCheckButton.setToolTip(_translate("SafeBrowsingDialog", "Press to check the entered URL"))
        self.urlCheckButton.setText(_translate("SafeBrowsingDialog", "Check URL"))
