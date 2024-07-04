# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsSubversion/SvnPropSetDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SvnPropSetDialog(object):
    def setupUi(self, SvnPropSetDialog):
        SvnPropSetDialog.setObjectName("SvnPropSetDialog")
        SvnPropSetDialog.resize(494, 385)
        SvnPropSetDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SvnPropSetDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1 = QtWidgets.QLabel(parent=SvnPropSetDialog)
        self.textLabel1.setObjectName("textLabel1")
        self.hboxlayout.addWidget(self.textLabel1)
        self.propNameEdit = QtWidgets.QLineEdit(parent=SvnPropSetDialog)
        self.propNameEdit.setObjectName("propNameEdit")
        self.hboxlayout.addWidget(self.propNameEdit)
        self.verticalLayout_2.addLayout(self.hboxlayout)
        self.groupBox = QtWidgets.QGroupBox(parent=SvnPropSetDialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textRadioButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.textRadioButton.setChecked(True)
        self.textRadioButton.setObjectName("textRadioButton")
        self.verticalLayout.addWidget(self.textRadioButton)
        self.propTextEdit = QtWidgets.QTextEdit(parent=self.groupBox)
        self.propTextEdit.setTabChangesFocus(True)
        self.propTextEdit.setAcceptRichText(False)
        self.propTextEdit.setObjectName("propTextEdit")
        self.verticalLayout.addWidget(self.propTextEdit)
        self.fileRadioButton = QtWidgets.QRadioButton(parent=self.groupBox)
        self.fileRadioButton.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.fileRadioButton.setObjectName("fileRadioButton")
        self.verticalLayout.addWidget(self.fileRadioButton)
        self.propFilePicker = EricPathPicker(parent=self.groupBox)
        self.propFilePicker.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propFilePicker.sizePolicy().hasHeightForWidth())
        self.propFilePicker.setSizePolicy(sizePolicy)
        self.propFilePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.propFilePicker.setObjectName("propFilePicker")
        self.verticalLayout.addWidget(self.propFilePicker)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SvnPropSetDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SvnPropSetDialog)
        self.textRadioButton.toggled['bool'].connect(self.propTextEdit.setEnabled) # type: ignore
        self.buttonBox.accepted.connect(SvnPropSetDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SvnPropSetDialog.reject) # type: ignore
        self.fileRadioButton.toggled['bool'].connect(self.propFilePicker.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SvnPropSetDialog)
        SvnPropSetDialog.setTabOrder(self.propNameEdit, self.textRadioButton)
        SvnPropSetDialog.setTabOrder(self.textRadioButton, self.propTextEdit)
        SvnPropSetDialog.setTabOrder(self.propTextEdit, self.propFilePicker)

    def retranslateUi(self, SvnPropSetDialog):
        _translate = QtCore.QCoreApplication.translate
        SvnPropSetDialog.setWindowTitle(_translate("SvnPropSetDialog", "Set Subversion Property"))
        self.textLabel1.setText(_translate("SvnPropSetDialog", "Property Name:"))
        self.propNameEdit.setToolTip(_translate("SvnPropSetDialog", "Enter the name of the property to be set"))
        self.groupBox.setTitle(_translate("SvnPropSetDialog", "Select property source"))
        self.textRadioButton.setText(_translate("SvnPropSetDialog", "Text"))
        self.propTextEdit.setToolTip(_translate("SvnPropSetDialog", "Enter text of the property"))
        self.fileRadioButton.setText(_translate("SvnPropSetDialog", "File"))
        self.propFilePicker.setToolTip(_translate("SvnPropSetDialog", "Enter the name of a file for the property"))
from eric7.EricWidgets.EricPathPicker import EricPathPicker
