# Form implementation generated from reading ui file 'src/eric7/WebBrowser/Sync/SyncDataPage.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SyncDataPage(object):
    def setupUi(self, SyncDataPage):
        SyncDataPage.setObjectName("SyncDataPage")
        SyncDataPage.resize(650, 400)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SyncDataPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.activeCheckBox = QtWidgets.QCheckBox(parent=SyncDataPage)
        self.activeCheckBox.setObjectName("activeCheckBox")
        self.verticalLayout_2.addWidget(self.activeCheckBox)
        self.syncDataBox = QtWidgets.QGroupBox(parent=SyncDataPage)
        self.syncDataBox.setEnabled(False)
        self.syncDataBox.setObjectName("syncDataBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.syncDataBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.bookmarksCheckBox = QtWidgets.QCheckBox(parent=self.syncDataBox)
        self.bookmarksCheckBox.setObjectName("bookmarksCheckBox")
        self.verticalLayout.addWidget(self.bookmarksCheckBox)
        self.historyCheckBox = QtWidgets.QCheckBox(parent=self.syncDataBox)
        self.historyCheckBox.setObjectName("historyCheckBox")
        self.verticalLayout.addWidget(self.historyCheckBox)
        self.passwordsCheckBox = QtWidgets.QCheckBox(parent=self.syncDataBox)
        self.passwordsCheckBox.setObjectName("passwordsCheckBox")
        self.verticalLayout.addWidget(self.passwordsCheckBox)
        self.userAgentsCheckBox = QtWidgets.QCheckBox(parent=self.syncDataBox)
        self.userAgentsCheckBox.setObjectName("userAgentsCheckBox")
        self.verticalLayout.addWidget(self.userAgentsCheckBox)
        self.speedDialCheckBox = QtWidgets.QCheckBox(parent=self.syncDataBox)
        self.speedDialCheckBox.setObjectName("speedDialCheckBox")
        self.verticalLayout.addWidget(self.speedDialCheckBox)
        self.verticalLayout_2.addWidget(self.syncDataBox)
        spacerItem = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(SyncDataPage)
        self.activeCheckBox.toggled['bool'].connect(self.syncDataBox.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SyncDataPage)

    def retranslateUi(self, SyncDataPage):
        _translate = QtCore.QCoreApplication.translate
        SyncDataPage.setTitle(_translate("SyncDataPage", "Basic synchronization settings"))
        SyncDataPage.setSubTitle(_translate("SyncDataPage", "Please select, if synchronization should be enabled and which data should be synchronized."))
        self.activeCheckBox.setToolTip(_translate("SyncDataPage", "Select to activate data synchronization"))
        self.activeCheckBox.setText(_translate("SyncDataPage", "Activate synchronization"))
        self.syncDataBox.setTitle(_translate("SyncDataPage", "Data to be synchronized"))
        self.bookmarksCheckBox.setToolTip(_translate("SyncDataPage", "Select to synchronize bookmarks"))
        self.bookmarksCheckBox.setText(_translate("SyncDataPage", "Bookmarks"))
        self.historyCheckBox.setToolTip(_translate("SyncDataPage", "Select to synchronize history"))
        self.historyCheckBox.setText(_translate("SyncDataPage", "History"))
        self.passwordsCheckBox.setToolTip(_translate("SyncDataPage", "Select to synchronize passwords"))
        self.passwordsCheckBox.setText(_translate("SyncDataPage", "Passwords"))
        self.userAgentsCheckBox.setToolTip(_translate("SyncDataPage", "Select to synchronize user agent settings"))
        self.userAgentsCheckBox.setText(_translate("SyncDataPage", "User Agent Settings"))
        self.speedDialCheckBox.setToolTip(_translate("SyncDataPage", "Select to synchronize the speed dial data"))
        self.speedDialCheckBox.setText(_translate("SyncDataPage", "Speed Dial Settings"))
