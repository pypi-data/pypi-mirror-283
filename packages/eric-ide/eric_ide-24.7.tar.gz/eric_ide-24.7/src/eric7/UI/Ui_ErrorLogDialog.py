# Form implementation generated from reading ui file 'src/eric7/UI/ErrorLogDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ErrorLogDialog(object):
    def setupUi(self, ErrorLogDialog):
        ErrorLogDialog.setObjectName("ErrorLogDialog")
        ErrorLogDialog.resize(500, 350)
        ErrorLogDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ErrorLogDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtWidgets.QLabel(parent=ErrorLogDialog)
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.label = QtWidgets.QLabel(parent=ErrorLogDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.logEdit = QtWidgets.QPlainTextEdit(parent=ErrorLogDialog)
        self.logEdit.setReadOnly(True)
        self.logEdit.setObjectName("logEdit")
        self.verticalLayout.addWidget(self.logEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.emailButton = QtWidgets.QPushButton(parent=ErrorLogDialog)
        self.emailButton.setDefault(True)
        self.emailButton.setObjectName("emailButton")
        self.horizontalLayout_2.addWidget(self.emailButton)
        self.deleteButton = QtWidgets.QPushButton(parent=ErrorLogDialog)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_2.addWidget(self.deleteButton)
        self.keepButton = QtWidgets.QPushButton(parent=ErrorLogDialog)
        self.keepButton.setObjectName("keepButton")
        self.horizontalLayout_2.addWidget(self.keepButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ErrorLogDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrorLogDialog)
        ErrorLogDialog.setTabOrder(self.logEdit, self.emailButton)
        ErrorLogDialog.setTabOrder(self.emailButton, self.deleteButton)
        ErrorLogDialog.setTabOrder(self.deleteButton, self.keepButton)

    def retranslateUi(self, ErrorLogDialog):
        _translate = QtCore.QCoreApplication.translate
        ErrorLogDialog.setWindowTitle(_translate("ErrorLogDialog", "Error Log Found"))
        self.label.setText(_translate("ErrorLogDialog", "<b>An error log file was found. What should be done with it?</b>"))
        self.emailButton.setToolTip(_translate("ErrorLogDialog", "Press to send an email"))
        self.emailButton.setText(_translate("ErrorLogDialog", "Send Bug Email"))
        self.deleteButton.setToolTip(_translate("ErrorLogDialog", "Press to ignore the error and delete the log file"))
        self.deleteButton.setText(_translate("ErrorLogDialog", "Ignore and Delete"))
        self.keepButton.setToolTip(_translate("ErrorLogDialog", "Press to ignore the error but keep the log file"))
        self.keepButton.setText(_translate("ErrorLogDialog", "Ignore but Keep"))
