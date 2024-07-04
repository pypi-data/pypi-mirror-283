# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsMercurial/HgDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_HgDialog(object):
    def setupUi(self, HgDialog):
        HgDialog.setObjectName("HgDialog")
        HgDialog.resize(593, 499)
        HgDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(HgDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.outputGroup = QtWidgets.QGroupBox(parent=HgDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.outputGroup.sizePolicy().hasHeightForWidth())
        self.outputGroup.setSizePolicy(sizePolicy)
        self.outputGroup.setObjectName("outputGroup")
        self.vboxlayout = QtWidgets.QVBoxLayout(self.outputGroup)
        self.vboxlayout.setObjectName("vboxlayout")
        self.resultbox = QtWidgets.QTextEdit(parent=self.outputGroup)
        self.resultbox.setReadOnly(True)
        self.resultbox.setAcceptRichText(False)
        self.resultbox.setObjectName("resultbox")
        self.vboxlayout.addWidget(self.resultbox)
        self.verticalLayout.addWidget(self.outputGroup)
        self.errorGroup = QtWidgets.QGroupBox(parent=HgDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.vboxlayout1 = QtWidgets.QVBoxLayout(self.errorGroup)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.errors = QtWidgets.QTextEdit(parent=self.errorGroup)
        self.errors.setReadOnly(True)
        self.errors.setAcceptRichText(False)
        self.errors.setObjectName("errors")
        self.vboxlayout1.addWidget(self.errors)
        self.verticalLayout.addWidget(self.errorGroup)
        self.inputGroup = QtWidgets.QGroupBox(parent=HgDialog)
        self.inputGroup.setObjectName("inputGroup")
        self._2 = QtWidgets.QGridLayout(self.inputGroup)
        self._2.setObjectName("_2")
        spacerItem = QtWidgets.QSpacerItem(327, 29, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self._2.addItem(spacerItem, 1, 1, 1, 1)
        self.sendButton = QtWidgets.QPushButton(parent=self.inputGroup)
        self.sendButton.setObjectName("sendButton")
        self._2.addWidget(self.sendButton, 1, 2, 1, 1)
        self.input = QtWidgets.QLineEdit(parent=self.inputGroup)
        self.input.setObjectName("input")
        self._2.addWidget(self.input, 0, 0, 1, 3)
        self.passwordCheckBox = QtWidgets.QCheckBox(parent=self.inputGroup)
        self.passwordCheckBox.setObjectName("passwordCheckBox")
        self._2.addWidget(self.passwordCheckBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.inputGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=HgDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(HgDialog)
        QtCore.QMetaObject.connectSlotsByName(HgDialog)
        HgDialog.setTabOrder(self.resultbox, self.errors)
        HgDialog.setTabOrder(self.errors, self.passwordCheckBox)
        HgDialog.setTabOrder(self.passwordCheckBox, self.input)
        HgDialog.setTabOrder(self.input, self.sendButton)

    def retranslateUi(self, HgDialog):
        _translate = QtCore.QCoreApplication.translate
        HgDialog.setWindowTitle(_translate("HgDialog", "Mercurial"))
        self.outputGroup.setTitle(_translate("HgDialog", "Output"))
        self.errorGroup.setTitle(_translate("HgDialog", "Errors"))
        self.inputGroup.setTitle(_translate("HgDialog", "Input"))
        self.sendButton.setToolTip(_translate("HgDialog", "Press to send the input to the Mercurial process"))
        self.sendButton.setText(_translate("HgDialog", "&Send"))
        self.sendButton.setShortcut(_translate("HgDialog", "Alt+S"))
        self.input.setToolTip(_translate("HgDialog", "Enter data to be sent to the Mercurial process"))
        self.passwordCheckBox.setToolTip(_translate("HgDialog", "Select to switch the input field to password mode"))
        self.passwordCheckBox.setText(_translate("HgDialog", "&Password Mode"))
        self.passwordCheckBox.setShortcut(_translate("HgDialog", "Alt+P"))
