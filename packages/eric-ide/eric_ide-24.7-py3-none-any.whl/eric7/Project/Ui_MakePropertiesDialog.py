# Form implementation generated from reading ui file 'src/eric7/Project/MakePropertiesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MakePropertiesDialog(object):
    def setupUi(self, MakePropertiesDialog):
        MakePropertiesDialog.setObjectName("MakePropertiesDialog")
        MakePropertiesDialog.resize(600, 266)
        MakePropertiesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(MakePropertiesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=MakePropertiesDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.makePicker = EricPathPicker(parent=MakePropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.makePicker.sizePolicy().hasHeightForWidth())
        self.makePicker.setSizePolicy(sizePolicy)
        self.makePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.makePicker.setObjectName("makePicker")
        self.verticalLayout.addWidget(self.makePicker)
        self.label_2 = QtWidgets.QLabel(parent=MakePropertiesDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.makefilePicker = EricPathPicker(parent=MakePropertiesDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.makefilePicker.sizePolicy().hasHeightForWidth())
        self.makefilePicker.setSizePolicy(sizePolicy)
        self.makefilePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.makefilePicker.setObjectName("makefilePicker")
        self.verticalLayout.addWidget(self.makefilePicker)
        self.label_3 = QtWidgets.QLabel(parent=MakePropertiesDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.makeTargetEdit = QtWidgets.QLineEdit(parent=MakePropertiesDialog)
        self.makeTargetEdit.setClearButtonEnabled(True)
        self.makeTargetEdit.setObjectName("makeTargetEdit")
        self.verticalLayout.addWidget(self.makeTargetEdit)
        self.label_4 = QtWidgets.QLabel(parent=MakePropertiesDialog)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.makeParametersEdit = QtWidgets.QLineEdit(parent=MakePropertiesDialog)
        self.makeParametersEdit.setClearButtonEnabled(True)
        self.makeParametersEdit.setObjectName("makeParametersEdit")
        self.verticalLayout.addWidget(self.makeParametersEdit)
        self.testOnlyCheckBox = QtWidgets.QCheckBox(parent=MakePropertiesDialog)
        self.testOnlyCheckBox.setObjectName("testOnlyCheckBox")
        self.verticalLayout.addWidget(self.testOnlyCheckBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=MakePropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MakePropertiesDialog)
        self.buttonBox.accepted.connect(MakePropertiesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(MakePropertiesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MakePropertiesDialog)

    def retranslateUi(self, MakePropertiesDialog):
        _translate = QtCore.QCoreApplication.translate
        MakePropertiesDialog.setWindowTitle(_translate("MakePropertiesDialog", "Make Properties"))
        self.label.setText(_translate("MakePropertiesDialog", "\'make\' Executable (leave empty to use global \'make\'):"))
        self.makePicker.setToolTip(_translate("MakePropertiesDialog", "Enter the executable name of the make utility"))
        self.label_2.setText(_translate("MakePropertiesDialog", "\'makefile\' path or directory (without file name \'makefile\' will be used):"))
        self.makefilePicker.setToolTip(_translate("MakePropertiesDialog", "Enter the name and/or path of the makefile"))
        self.label_3.setText(_translate("MakePropertiesDialog", "Make Target:"))
        self.makeTargetEdit.setToolTip(_translate("MakePropertiesDialog", "Enter the make target to be built"))
        self.label_4.setText(_translate("MakePropertiesDialog", "Make Command Parameters (enclose parameters containing spaces in \"\"):"))
        self.makeParametersEdit.setToolTip(_translate("MakePropertiesDialog", "Enter the command parameters for make"))
        self.testOnlyCheckBox.setToolTip(_translate("MakePropertiesDialog", "Select to just test for changes needing a make run"))
        self.testOnlyCheckBox.setText(_translate("MakePropertiesDialog", "Test for changes only when run automatically"))
from eric7.EricWidgets.EricPathPicker import EricPathPicker
