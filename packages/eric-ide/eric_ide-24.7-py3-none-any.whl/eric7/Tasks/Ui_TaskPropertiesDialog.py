# Form implementation generated from reading ui file 'src/eric7/Tasks/TaskPropertiesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TaskPropertiesDialog(object):
    def setupUi(self, TaskPropertiesDialog):
        TaskPropertiesDialog.setObjectName("TaskPropertiesDialog")
        TaskPropertiesDialog.resize(600, 400)
        TaskPropertiesDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(TaskPropertiesDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(parent=TaskPropertiesDialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.summaryEdit = QtWidgets.QLineEdit(parent=TaskPropertiesDialog)
        self.summaryEdit.setObjectName("summaryEdit")
        self.gridLayout_2.addWidget(self.summaryEdit, 0, 1, 1, 1)
        self.descriptionLabel = QtWidgets.QLabel(parent=TaskPropertiesDialog)
        self.descriptionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.gridLayout_2.addWidget(self.descriptionLabel, 1, 0, 1, 1)
        self.descriptionEdit = EricSpellCheckedTextEdit(parent=TaskPropertiesDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridLayout_2.addWidget(self.descriptionEdit, 1, 1, 1, 1)
        self.manualTaskFrame = QtWidgets.QFrame(parent=TaskPropertiesDialog)
        self.manualTaskFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.manualTaskFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.manualTaskFrame.setObjectName("manualTaskFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.manualTaskFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.textLabel2 = QtWidgets.QLabel(parent=self.manualTaskFrame)
        self.textLabel2.setObjectName("textLabel2")
        self.horizontalLayout_2.addWidget(self.textLabel2)
        self.creationLabel = QtWidgets.QLabel(parent=self.manualTaskFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.creationLabel.sizePolicy().hasHeightForWidth())
        self.creationLabel.setSizePolicy(sizePolicy)
        self.creationLabel.setObjectName("creationLabel")
        self.horizontalLayout_2.addWidget(self.creationLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textLabel4 = QtWidgets.QLabel(parent=self.manualTaskFrame)
        self.textLabel4.setObjectName("textLabel4")
        self.horizontalLayout.addWidget(self.textLabel4)
        self.priorityCombo = QtWidgets.QComboBox(parent=self.manualTaskFrame)
        self.priorityCombo.setObjectName("priorityCombo")
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.priorityCombo.addItem("")
        self.horizontalLayout.addWidget(self.priorityCombo)
        self.label_2 = QtWidgets.QLabel(parent=self.manualTaskFrame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.typeCombo = QtWidgets.QComboBox(parent=self.manualTaskFrame)
        self.typeCombo.setObjectName("typeCombo")
        self.horizontalLayout.addWidget(self.typeCombo)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.completedCheckBox = QtWidgets.QCheckBox(parent=self.manualTaskFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.completedCheckBox.sizePolicy().hasHeightForWidth())
        self.completedCheckBox.setSizePolicy(sizePolicy)
        self.completedCheckBox.setObjectName("completedCheckBox")
        self.verticalLayout.addWidget(self.completedCheckBox)
        self.gridLayout_2.addWidget(self.manualTaskFrame, 2, 0, 1, 2)
        self.projectCheckBox = QtWidgets.QCheckBox(parent=TaskPropertiesDialog)
        self.projectCheckBox.setObjectName("projectCheckBox")
        self.gridLayout_2.addWidget(self.projectCheckBox, 3, 0, 1, 2)
        self.fileTaskFrame = QtWidgets.QFrame(parent=TaskPropertiesDialog)
        self.fileTaskFrame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.fileTaskFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.fileTaskFrame.setObjectName("fileTaskFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.fileTaskFrame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.linenoEdit = QtWidgets.QLineEdit(parent=self.fileTaskFrame)
        self.linenoEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.linenoEdit.setReadOnly(True)
        self.linenoEdit.setObjectName("linenoEdit")
        self.gridLayout.addWidget(self.linenoEdit, 1, 1, 1, 1)
        self.linenoLabel = QtWidgets.QLabel(parent=self.fileTaskFrame)
        self.linenoLabel.setObjectName("linenoLabel")
        self.gridLayout.addWidget(self.linenoLabel, 1, 0, 1, 1)
        self.filenameLabel = QtWidgets.QLabel(parent=self.fileTaskFrame)
        self.filenameLabel.setObjectName("filenameLabel")
        self.gridLayout.addWidget(self.filenameLabel, 0, 0, 1, 1)
        self.filenameEdit = QtWidgets.QLineEdit(parent=self.fileTaskFrame)
        self.filenameEdit.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.filenameEdit.setReadOnly(True)
        self.filenameEdit.setObjectName("filenameEdit")
        self.gridLayout.addWidget(self.filenameEdit, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.fileTaskFrame, 4, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=TaskPropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.label.setBuddy(self.summaryEdit)
        self.descriptionLabel.setBuddy(self.descriptionEdit)
        self.textLabel4.setBuddy(self.priorityCombo)

        self.retranslateUi(TaskPropertiesDialog)
        self.priorityCombo.setCurrentIndex(1)
        self.buttonBox.accepted.connect(TaskPropertiesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(TaskPropertiesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(TaskPropertiesDialog)
        TaskPropertiesDialog.setTabOrder(self.summaryEdit, self.descriptionEdit)
        TaskPropertiesDialog.setTabOrder(self.descriptionEdit, self.priorityCombo)
        TaskPropertiesDialog.setTabOrder(self.priorityCombo, self.typeCombo)
        TaskPropertiesDialog.setTabOrder(self.typeCombo, self.completedCheckBox)
        TaskPropertiesDialog.setTabOrder(self.completedCheckBox, self.projectCheckBox)

    def retranslateUi(self, TaskPropertiesDialog):
        _translate = QtCore.QCoreApplication.translate
        TaskPropertiesDialog.setWindowTitle(_translate("TaskPropertiesDialog", "Task Properties"))
        self.label.setText(_translate("TaskPropertiesDialog", "&Summary:"))
        self.summaryEdit.setToolTip(_translate("TaskPropertiesDialog", "Enter the task summary"))
        self.descriptionLabel.setText(_translate("TaskPropertiesDialog", "&Description:"))
        self.descriptionEdit.setToolTip(_translate("TaskPropertiesDialog", "Enter the task description"))
        self.textLabel2.setText(_translate("TaskPropertiesDialog", "Creation Time:"))
        self.textLabel4.setText(_translate("TaskPropertiesDialog", "&Priority:"))
        self.priorityCombo.setToolTip(_translate("TaskPropertiesDialog", "Select the task priority"))
        self.priorityCombo.setItemText(0, _translate("TaskPropertiesDialog", "High"))
        self.priorityCombo.setItemText(1, _translate("TaskPropertiesDialog", "Normal"))
        self.priorityCombo.setItemText(2, _translate("TaskPropertiesDialog", "Low"))
        self.label_2.setText(_translate("TaskPropertiesDialog", "Type:"))
        self.typeCombo.setToolTip(_translate("TaskPropertiesDialog", "Select the task type"))
        self.completedCheckBox.setToolTip(_translate("TaskPropertiesDialog", "Select to mark this task as completed"))
        self.completedCheckBox.setText(_translate("TaskPropertiesDialog", "T&ask completed"))
        self.projectCheckBox.setToolTip(_translate("TaskPropertiesDialog", "Select to indicate a task related to the current project"))
        self.projectCheckBox.setText(_translate("TaskPropertiesDialog", "Project &Task"))
        self.linenoLabel.setText(_translate("TaskPropertiesDialog", "Line:"))
        self.filenameLabel.setText(_translate("TaskPropertiesDialog", "Filename:"))
from eric7.EricWidgets.EricSpellCheckedTextEdit import EricSpellCheckedTextEdit
