# Form implementation generated from reading ui file 'src/eric7/WebBrowser/GreaseMonkey/GreaseMonkeyConfiguration/GreaseMonkeyConfigurationDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GreaseMonkeyConfigurationDialog(object):
    def setupUi(self, GreaseMonkeyConfigurationDialog):
        GreaseMonkeyConfigurationDialog.setObjectName("GreaseMonkeyConfigurationDialog")
        GreaseMonkeyConfigurationDialog.resize(550, 450)
        GreaseMonkeyConfigurationDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreaseMonkeyConfigurationDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.iconLabel = QtWidgets.QLabel(parent=GreaseMonkeyConfigurationDialog)
        self.iconLabel.setMinimumSize(QtCore.QSize(48, 48))
        self.iconLabel.setText("Icon")
        self.iconLabel.setObjectName("iconLabel")
        self.horizontalLayout.addWidget(self.iconLabel)
        self.label_2 = QtWidgets.QLabel(parent=GreaseMonkeyConfigurationDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_4 = QtWidgets.QLabel(parent=GreaseMonkeyConfigurationDialog)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.scriptsList = GreaseMonkeyConfigurationListWidget(parent=GreaseMonkeyConfigurationDialog)
        self.scriptsList.setAlternatingRowColors(True)
        self.scriptsList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.scriptsList.setUniformItemSizes(True)
        self.scriptsList.setSelectionRectVisible(True)
        self.scriptsList.setObjectName("scriptsList")
        self.verticalLayout.addWidget(self.scriptsList)
        self.downloadLabel = QtWidgets.QLabel(parent=GreaseMonkeyConfigurationDialog)
        self.downloadLabel.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.downloadLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.downloadLabel.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard|QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.downloadLabel.setObjectName("downloadLabel")
        self.verticalLayout.addWidget(self.downloadLabel)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.openDirectoryButton = QtWidgets.QPushButton(parent=GreaseMonkeyConfigurationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDirectoryButton.sizePolicy().hasHeightForWidth())
        self.openDirectoryButton.setSizePolicy(sizePolicy)
        self.openDirectoryButton.setObjectName("openDirectoryButton")
        self.horizontalLayout_4.addWidget(self.openDirectoryButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GreaseMonkeyConfigurationDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_4.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(GreaseMonkeyConfigurationDialog)
        self.buttonBox.accepted.connect(GreaseMonkeyConfigurationDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GreaseMonkeyConfigurationDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GreaseMonkeyConfigurationDialog)
        GreaseMonkeyConfigurationDialog.setTabOrder(self.scriptsList, self.openDirectoryButton)
        GreaseMonkeyConfigurationDialog.setTabOrder(self.openDirectoryButton, self.buttonBox)

    def retranslateUi(self, GreaseMonkeyConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        GreaseMonkeyConfigurationDialog.setWindowTitle(_translate("GreaseMonkeyConfigurationDialog", "GreaseMonkey Scripts Configuration"))
        self.label_2.setText(_translate("GreaseMonkeyConfigurationDialog", "<h2>GreaseMonkey Scripts</h2>"))
        self.label_4.setText(_translate("GreaseMonkeyConfigurationDialog", "Double clicking script will show additional information."))
        self.downloadLabel.setText(_translate("GreaseMonkeyConfigurationDialog", "<p>Get more scripts from <a href=\"https://greasyfork.org/\">greasyfork.org</a> or via <a href=\"http://wiki.greasespot.net/User_Script_Hosting\">Greasespot Wiki.</a></p>"))
        self.openDirectoryButton.setToolTip(_translate("GreaseMonkeyConfigurationDialog", "Press to open the scripts directory"))
        self.openDirectoryButton.setText(_translate("GreaseMonkeyConfigurationDialog", "Open Scripts Directory"))
from .GreaseMonkeyConfigurationListWidget import GreaseMonkeyConfigurationListWidget
