# Form implementation generated from reading ui file 'src/eric7/Debugger/EditBreakpointDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EditBreakpointDialog(object):
    def setupUi(self, EditBreakpointDialog):
        EditBreakpointDialog.setObjectName("EditBreakpointDialog")
        EditBreakpointDialog.resize(428, 226)
        EditBreakpointDialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(EditBreakpointDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.textLabel1_2 = QtWidgets.QLabel(parent=EditBreakpointDialog)
        self.textLabel1_2.setObjectName("textLabel1_2")
        self.gridLayout.addWidget(self.textLabel1_2, 0, 0, 1, 1)
        self.filenamePicker = EricComboPathPicker(parent=EditBreakpointDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filenamePicker.sizePolicy().hasHeightForWidth())
        self.filenamePicker.setSizePolicy(sizePolicy)
        self.filenamePicker.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.filenamePicker.setObjectName("filenamePicker")
        self.gridLayout.addWidget(self.filenamePicker, 0, 1, 1, 2)
        self.textLabel2_2 = QtWidgets.QLabel(parent=EditBreakpointDialog)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridLayout.addWidget(self.textLabel2_2, 1, 0, 1, 1)
        self.linenoSpinBox = QtWidgets.QSpinBox(parent=EditBreakpointDialog)
        self.linenoSpinBox.setMinimum(1)
        self.linenoSpinBox.setMaximum(99999)
        self.linenoSpinBox.setObjectName("linenoSpinBox")
        self.gridLayout.addWidget(self.linenoSpinBox, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.textLabel1 = QtWidgets.QLabel(parent=EditBreakpointDialog)
        self.textLabel1.setObjectName("textLabel1")
        self.gridLayout.addWidget(self.textLabel1, 2, 0, 1, 1)
        self.conditionCombo = QtWidgets.QComboBox(parent=EditBreakpointDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.conditionCombo.sizePolicy().hasHeightForWidth())
        self.conditionCombo.setSizePolicy(sizePolicy)
        self.conditionCombo.setEditable(True)
        self.conditionCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.conditionCombo.setObjectName("conditionCombo")
        self.gridLayout.addWidget(self.conditionCombo, 2, 1, 1, 2)
        self.textLabel2 = QtWidgets.QLabel(parent=EditBreakpointDialog)
        self.textLabel2.setObjectName("textLabel2")
        self.gridLayout.addWidget(self.textLabel2, 3, 0, 1, 1)
        self.ignoreSpinBox = QtWidgets.QSpinBox(parent=EditBreakpointDialog)
        self.ignoreSpinBox.setMaximum(9999)
        self.ignoreSpinBox.setObjectName("ignoreSpinBox")
        self.gridLayout.addWidget(self.ignoreSpinBox, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        self.temporaryCheckBox = QtWidgets.QCheckBox(parent=EditBreakpointDialog)
        self.temporaryCheckBox.setObjectName("temporaryCheckBox")
        self.gridLayout.addWidget(self.temporaryCheckBox, 4, 0, 1, 3)
        self.enabledCheckBox = QtWidgets.QCheckBox(parent=EditBreakpointDialog)
        self.enabledCheckBox.setChecked(True)
        self.enabledCheckBox.setObjectName("enabledCheckBox")
        self.gridLayout.addWidget(self.enabledCheckBox, 5, 0, 1, 3)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=EditBreakpointDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)

        self.retranslateUi(EditBreakpointDialog)
        self.buttonBox.accepted.connect(EditBreakpointDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(EditBreakpointDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EditBreakpointDialog)
        EditBreakpointDialog.setTabOrder(self.filenamePicker, self.linenoSpinBox)
        EditBreakpointDialog.setTabOrder(self.linenoSpinBox, self.conditionCombo)
        EditBreakpointDialog.setTabOrder(self.conditionCombo, self.ignoreSpinBox)
        EditBreakpointDialog.setTabOrder(self.ignoreSpinBox, self.temporaryCheckBox)
        EditBreakpointDialog.setTabOrder(self.temporaryCheckBox, self.enabledCheckBox)

    def retranslateUi(self, EditBreakpointDialog):
        _translate = QtCore.QCoreApplication.translate
        EditBreakpointDialog.setWindowTitle(_translate("EditBreakpointDialog", "Edit Breakpoint"))
        self.textLabel1_2.setText(_translate("EditBreakpointDialog", "Filename:"))
        self.filenamePicker.setToolTip(_translate("EditBreakpointDialog", "Enter the filename of the breakpoint"))
        self.textLabel2_2.setText(_translate("EditBreakpointDialog", "Linenumber:"))
        self.linenoSpinBox.setToolTip(_translate("EditBreakpointDialog", "Enter the linenumber of the breakpoint"))
        self.textLabel1.setText(_translate("EditBreakpointDialog", "Condition:"))
        self.conditionCombo.setToolTip(_translate("EditBreakpointDialog", "Enter or select a condition for the breakpoint"))
        self.textLabel2.setText(_translate("EditBreakpointDialog", "Ignore Count:"))
        self.ignoreSpinBox.setToolTip(_translate("EditBreakpointDialog", "Enter an ignore count for the breakpoint"))
        self.temporaryCheckBox.setToolTip(_translate("EditBreakpointDialog", "Select whether this is a temporary breakpoint"))
        self.temporaryCheckBox.setText(_translate("EditBreakpointDialog", "Temporary Breakpoint"))
        self.enabledCheckBox.setToolTip(_translate("EditBreakpointDialog", "Select, whether the breakpoint is enabled"))
        self.enabledCheckBox.setText(_translate("EditBreakpointDialog", "Enabled"))
from eric7.EricWidgets.EricPathPicker import EricComboPathPicker
