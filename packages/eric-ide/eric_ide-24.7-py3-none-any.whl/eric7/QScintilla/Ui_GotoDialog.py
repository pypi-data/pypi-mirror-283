# Form implementation generated from reading ui file 'src/eric7/QScintilla/GotoDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_GotoDialog(object):
    def setupUi(self, GotoDialog):
        GotoDialog.setObjectName("GotoDialog")
        GotoDialog.resize(206, 77)
        self._3 = QtWidgets.QVBoxLayout(GotoDialog)
        self._3.setObjectName("_3")
        self._2 = QtWidgets.QHBoxLayout()
        self._2.setObjectName("_2")
        self.linenumberLabel = QtWidgets.QLabel(parent=GotoDialog)
        self.linenumberLabel.setObjectName("linenumberLabel")
        self._2.addWidget(self.linenumberLabel)
        self.linenumberSpinBox = QtWidgets.QSpinBox(parent=GotoDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linenumberSpinBox.sizePolicy().hasHeightForWidth())
        self.linenumberSpinBox.setSizePolicy(sizePolicy)
        self.linenumberSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.linenumberSpinBox.setMinimum(1)
        self.linenumberSpinBox.setMaximum(99999)
        self.linenumberSpinBox.setObjectName("linenumberSpinBox")
        self._2.addWidget(self.linenumberSpinBox)
        self._3.addLayout(self._2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=GotoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self._3.addWidget(self.buttonBox)
        self.linenumberLabel.setBuddy(self.linenumberSpinBox)

        self.retranslateUi(GotoDialog)
        self.buttonBox.accepted.connect(GotoDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(GotoDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GotoDialog)

    def retranslateUi(self, GotoDialog):
        _translate = QtCore.QCoreApplication.translate
        GotoDialog.setWindowTitle(_translate("GotoDialog", "Goto"))
        self.linenumberLabel.setText(_translate("GotoDialog", "&Line Number:"))
        self.linenumberSpinBox.setToolTip(_translate("GotoDialog", "Enter linenumber to go to"))
        self.linenumberSpinBox.setWhatsThis(_translate("GotoDialog", "<b>Linenumber</b>\n"
"<p>Enter the linenumber to go to in this entry field.</p>"))
