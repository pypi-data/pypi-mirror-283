# Form implementation generated from reading ui file 'src/eric7/WebBrowser/CookieJar/CookiesConfigurationDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CookiesConfigurationDialog(object):
    def setupUi(self, CookiesConfigurationDialog):
        CookiesConfigurationDialog.setObjectName("CookiesConfigurationDialog")
        CookiesConfigurationDialog.resize(500, 160)
        CookiesConfigurationDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CookiesConfigurationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.headerLabel = QtWidgets.QLabel(parent=CookiesConfigurationDialog)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout.addWidget(self.headerLabel)
        self.line17 = QtWidgets.QFrame(parent=CookiesConfigurationDialog)
        self.line17.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line17.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line17.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line17.setObjectName("line17")
        self.verticalLayout.addWidget(self.line17)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(parent=CookiesConfigurationDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.acceptCombo = QtWidgets.QComboBox(parent=CookiesConfigurationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptCombo.sizePolicy().hasHeightForWidth())
        self.acceptCombo.setSizePolicy(sizePolicy)
        self.acceptCombo.setObjectName("acceptCombo")
        self.acceptCombo.addItem("")
        self.acceptCombo.addItem("")
        self.acceptCombo.addItem("")
        self.gridLayout.addWidget(self.acceptCombo, 0, 1, 1, 1)
        self.exceptionsButton = QtWidgets.QPushButton(parent=CookiesConfigurationDialog)
        self.exceptionsButton.setObjectName("exceptionsButton")
        self.gridLayout.addWidget(self.exceptionsButton, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(parent=CookiesConfigurationDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.keepUntilCombo = QtWidgets.QComboBox(parent=CookiesConfigurationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keepUntilCombo.sizePolicy().hasHeightForWidth())
        self.keepUntilCombo.setSizePolicy(sizePolicy)
        self.keepUntilCombo.setObjectName("keepUntilCombo")
        self.keepUntilCombo.addItem("")
        self.keepUntilCombo.addItem("")
        self.gridLayout.addWidget(self.keepUntilCombo, 1, 1, 1, 1)
        self.cookiesButton = QtWidgets.QPushButton(parent=CookiesConfigurationDialog)
        self.cookiesButton.setObjectName("cookiesButton")
        self.gridLayout.addWidget(self.cookiesButton, 1, 2, 1, 1)
        self.filterTrackingCookiesCheckbox = QtWidgets.QCheckBox(parent=CookiesConfigurationDialog)
        self.filterTrackingCookiesCheckbox.setObjectName("filterTrackingCookiesCheckbox")
        self.gridLayout.addWidget(self.filterTrackingCookiesCheckbox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=CookiesConfigurationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.label_2.setBuddy(self.acceptCombo)
        self.label.setBuddy(self.keepUntilCombo)

        self.retranslateUi(CookiesConfigurationDialog)
        self.buttonBox.accepted.connect(CookiesConfigurationDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(CookiesConfigurationDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CookiesConfigurationDialog)
        CookiesConfigurationDialog.setTabOrder(self.acceptCombo, self.exceptionsButton)
        CookiesConfigurationDialog.setTabOrder(self.exceptionsButton, self.keepUntilCombo)
        CookiesConfigurationDialog.setTabOrder(self.keepUntilCombo, self.cookiesButton)
        CookiesConfigurationDialog.setTabOrder(self.cookiesButton, self.filterTrackingCookiesCheckbox)
        CookiesConfigurationDialog.setTabOrder(self.filterTrackingCookiesCheckbox, self.buttonBox)

    def retranslateUi(self, CookiesConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        CookiesConfigurationDialog.setWindowTitle(_translate("CookiesConfigurationDialog", "Configure cookies"))
        self.headerLabel.setText(_translate("CookiesConfigurationDialog", "<b>Configure cookies</b>"))
        self.label_2.setText(_translate("CookiesConfigurationDialog", "&Accept Cookies:"))
        self.acceptCombo.setToolTip(_translate("CookiesConfigurationDialog", "Select the accept policy"))
        self.acceptCombo.setItemText(0, _translate("CookiesConfigurationDialog", "Always"))
        self.acceptCombo.setItemText(1, _translate("CookiesConfigurationDialog", "Never"))
        self.acceptCombo.setItemText(2, _translate("CookiesConfigurationDialog", "Only from sites you navigate to"))
        self.exceptionsButton.setToolTip(_translate("CookiesConfigurationDialog", "Show a dialog to configure exceptions"))
        self.exceptionsButton.setText(_translate("CookiesConfigurationDialog", "&Exceptions..."))
        self.label.setText(_translate("CookiesConfigurationDialog", "&Keep until:"))
        self.keepUntilCombo.setToolTip(_translate("CookiesConfigurationDialog", "Select the keep policy"))
        self.keepUntilCombo.setItemText(0, _translate("CookiesConfigurationDialog", "They expire"))
        self.keepUntilCombo.setItemText(1, _translate("CookiesConfigurationDialog", "I exit the application"))
        self.cookiesButton.setToolTip(_translate("CookiesConfigurationDialog", "Show a dialog listing all cookies"))
        self.cookiesButton.setText(_translate("CookiesConfigurationDialog", "&Show Cookies..."))
        self.filterTrackingCookiesCheckbox.setToolTip(_translate("CookiesConfigurationDialog", "Select to filter tracking cookies"))
        self.filterTrackingCookiesCheckbox.setText(_translate("CookiesConfigurationDialog", "&Filter Tracking Cookies"))
