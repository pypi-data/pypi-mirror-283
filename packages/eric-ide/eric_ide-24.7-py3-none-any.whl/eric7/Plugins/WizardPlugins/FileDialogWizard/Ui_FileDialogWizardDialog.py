# Form implementation generated from reading ui file 'src/eric7/Plugins/WizardPlugins/FileDialogWizard/FileDialogWizardDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FileDialogWizardDialog(object):
    def setupUi(self, FileDialogWizardDialog):
        FileDialogWizardDialog.setObjectName("FileDialogWizardDialog")
        FileDialogWizardDialog.resize(645, 946)
        FileDialogWizardDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileDialogWizardDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=FileDialogWizardDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pyqtComboBox = QtWidgets.QComboBox(parent=FileDialogWizardDialog)
        self.pyqtComboBox.setMinimumSize(QtCore.QSize(150, 0))
        self.pyqtComboBox.setObjectName("pyqtComboBox")
        self.horizontalLayout.addWidget(self.pyqtComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.typeGroupBox = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.typeGroupBox.setObjectName("typeGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.typeGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.rOpenFile = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rOpenFile.setChecked(True)
        self.rOpenFile.setObjectName("rOpenFile")
        self.gridLayout.addWidget(self.rOpenFile, 0, 0, 1, 1)
        self.rOpenFiles = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rOpenFiles.setObjectName("rOpenFiles")
        self.gridLayout.addWidget(self.rOpenFiles, 0, 1, 1, 1)
        self.rSaveFile = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rSaveFile.setObjectName("rSaveFile")
        self.gridLayout.addWidget(self.rSaveFile, 0, 2, 1, 1)
        self.rDirectory = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rDirectory.setObjectName("rDirectory")
        self.gridLayout.addWidget(self.rDirectory, 0, 3, 1, 1)
        self.rfOpenFile = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rfOpenFile.setChecked(False)
        self.rfOpenFile.setObjectName("rfOpenFile")
        self.gridLayout.addWidget(self.rfOpenFile, 1, 0, 1, 1)
        self.rfOpenFiles = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rfOpenFiles.setObjectName("rfOpenFiles")
        self.gridLayout.addWidget(self.rfOpenFiles, 1, 1, 1, 1)
        self.rfSaveFile = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rfSaveFile.setObjectName("rfSaveFile")
        self.gridLayout.addWidget(self.rfSaveFile, 1, 2, 1, 1)
        self.rOpenFileUrl = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rOpenFileUrl.setChecked(False)
        self.rOpenFileUrl.setObjectName("rOpenFileUrl")
        self.gridLayout.addWidget(self.rOpenFileUrl, 2, 0, 1, 1)
        self.rOpenFileUrls = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rOpenFileUrls.setObjectName("rOpenFileUrls")
        self.gridLayout.addWidget(self.rOpenFileUrls, 2, 1, 1, 1)
        self.rSaveFileUrl = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rSaveFileUrl.setObjectName("rSaveFileUrl")
        self.gridLayout.addWidget(self.rSaveFileUrl, 2, 2, 1, 1)
        self.rDirectoryUrl = QtWidgets.QRadioButton(parent=self.typeGroupBox)
        self.rDirectoryUrl.setObjectName("rDirectoryUrl")
        self.gridLayout.addWidget(self.rDirectoryUrl, 2, 3, 1, 1)
        self.verticalLayout.addWidget(self.typeGroupBox)
        self.groupBox = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.eNameVariable = QtWidgets.QLineEdit(parent=self.groupBox)
        self.eNameVariable.setClearButtonEnabled(False)
        self.eNameVariable.setObjectName("eNameVariable")
        self.gridLayout_4.addWidget(self.eNameVariable, 0, 1, 1, 1)
        self.lFilterVariable = QtWidgets.QLabel(parent=self.groupBox)
        self.lFilterVariable.setObjectName("lFilterVariable")
        self.gridLayout_4.addWidget(self.lFilterVariable, 1, 0, 1, 1)
        self.eFilterVariable = QtWidgets.QLineEdit(parent=self.groupBox)
        self.eFilterVariable.setClearButtonEnabled(False)
        self.eFilterVariable.setObjectName("eFilterVariable")
        self.gridLayout_4.addWidget(self.eFilterVariable, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TextLabel1 = QtWidgets.QLabel(parent=FileDialogWizardDialog)
        self.TextLabel1.setObjectName("TextLabel1")
        self.horizontalLayout_3.addWidget(self.TextLabel1)
        self.eCaption = QtWidgets.QLineEdit(parent=FileDialogWizardDialog)
        self.eCaption.setClearButtonEnabled(True)
        self.eCaption.setObjectName("eCaption")
        self.horizontalLayout_3.addWidget(self.eCaption)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.cSymlinks = QtWidgets.QCheckBox(parent=FileDialogWizardDialog)
        self.cSymlinks.setChecked(True)
        self.cSymlinks.setObjectName("cSymlinks")
        self.verticalLayout.addWidget(self.cSymlinks)
        self.parentGroup = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.parentGroup.setObjectName("parentGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.parentGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.parentSelf = QtWidgets.QRadioButton(parent=self.parentGroup)
        self.parentSelf.setChecked(True)
        self.parentSelf.setObjectName("parentSelf")
        self.gridLayout_3.addWidget(self.parentSelf, 0, 0, 1, 1)
        self.parentNone = QtWidgets.QRadioButton(parent=self.parentGroup)
        self.parentNone.setObjectName("parentNone")
        self.gridLayout_3.addWidget(self.parentNone, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.parentOther = QtWidgets.QRadioButton(parent=self.parentGroup)
        self.parentOther.setObjectName("parentOther")
        self.horizontalLayout_2.addWidget(self.parentOther)
        self.parentEdit = QtWidgets.QLineEdit(parent=self.parentGroup)
        self.parentEdit.setEnabled(False)
        self.parentEdit.setClearButtonEnabled(True)
        self.parentEdit.setObjectName("parentEdit")
        self.horizontalLayout_2.addWidget(self.parentEdit)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.verticalLayout.addWidget(self.parentGroup)
        self.filePropertiesGroup = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.filePropertiesGroup.setObjectName("filePropertiesGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.filePropertiesGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TextLabel3 = QtWidgets.QLabel(parent=self.filePropertiesGroup)
        self.TextLabel3.setObjectName("TextLabel3")
        self.gridLayout_2.addWidget(self.TextLabel3, 0, 0, 1, 2)
        self.eStartWith = QtWidgets.QLineEdit(parent=self.filePropertiesGroup)
        self.eStartWith.setClearButtonEnabled(True)
        self.eStartWith.setObjectName("eStartWith")
        self.gridLayout_2.addWidget(self.eStartWith, 1, 0, 1, 1)
        self.cStartWith = QtWidgets.QCheckBox(parent=self.filePropertiesGroup)
        self.cStartWith.setObjectName("cStartWith")
        self.gridLayout_2.addWidget(self.cStartWith, 1, 1, 1, 1)
        self.TextLabel2 = QtWidgets.QLabel(parent=self.filePropertiesGroup)
        self.TextLabel2.setObjectName("TextLabel2")
        self.gridLayout_2.addWidget(self.TextLabel2, 2, 0, 1, 2)
        self.eFilters = QtWidgets.QLineEdit(parent=self.filePropertiesGroup)
        self.eFilters.setClearButtonEnabled(True)
        self.eFilters.setObjectName("eFilters")
        self.gridLayout_2.addWidget(self.eFilters, 3, 0, 1, 1)
        self.cFilters = QtWidgets.QCheckBox(parent=self.filePropertiesGroup)
        self.cFilters.setObjectName("cFilters")
        self.gridLayout_2.addWidget(self.cFilters, 3, 1, 1, 1)
        self.lInitialFilter = QtWidgets.QLabel(parent=self.filePropertiesGroup)
        self.lInitialFilter.setObjectName("lInitialFilter")
        self.gridLayout_2.addWidget(self.lInitialFilter, 4, 0, 1, 2)
        self.eInitialFilter = QtWidgets.QLineEdit(parent=self.filePropertiesGroup)
        self.eInitialFilter.setClearButtonEnabled(True)
        self.eInitialFilter.setObjectName("eInitialFilter")
        self.gridLayout_2.addWidget(self.eInitialFilter, 5, 0, 1, 1)
        self.cInitialFilter = QtWidgets.QCheckBox(parent=self.filePropertiesGroup)
        self.cInitialFilter.setObjectName("cInitialFilter")
        self.gridLayout_2.addWidget(self.cInitialFilter, 5, 1, 1, 1)
        self.cConfirmOverwrite = QtWidgets.QCheckBox(parent=self.filePropertiesGroup)
        self.cConfirmOverwrite.setEnabled(False)
        self.cConfirmOverwrite.setObjectName("cConfirmOverwrite")
        self.gridLayout_2.addWidget(self.cConfirmOverwrite, 6, 0, 1, 2)
        self.verticalLayout.addWidget(self.filePropertiesGroup)
        self.dirPropertiesGroup = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.dirPropertiesGroup.setEnabled(False)
        self.dirPropertiesGroup.setObjectName("dirPropertiesGroup")
        self.gridlayout = QtWidgets.QGridLayout(self.dirPropertiesGroup)
        self.gridlayout.setObjectName("gridlayout")
        self.eWorkDir = QtWidgets.QLineEdit(parent=self.dirPropertiesGroup)
        self.eWorkDir.setClearButtonEnabled(True)
        self.eWorkDir.setObjectName("eWorkDir")
        self.gridlayout.addWidget(self.eWorkDir, 1, 0, 1, 1)
        self.TextLabel4 = QtWidgets.QLabel(parent=self.dirPropertiesGroup)
        self.TextLabel4.setObjectName("TextLabel4")
        self.gridlayout.addWidget(self.TextLabel4, 0, 0, 1, 2)
        self.cWorkDir = QtWidgets.QCheckBox(parent=self.dirPropertiesGroup)
        self.cWorkDir.setObjectName("cWorkDir")
        self.gridlayout.addWidget(self.cWorkDir, 1, 1, 1, 1)
        self.cDirOnly = QtWidgets.QCheckBox(parent=self.dirPropertiesGroup)
        self.cDirOnly.setChecked(True)
        self.cDirOnly.setObjectName("cDirOnly")
        self.gridlayout.addWidget(self.cDirOnly, 2, 0, 1, 2)
        self.verticalLayout.addWidget(self.dirPropertiesGroup)
        self.urlPropertiesGroup = QtWidgets.QGroupBox(parent=FileDialogWizardDialog)
        self.urlPropertiesGroup.setObjectName("urlPropertiesGroup")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.urlPropertiesGroup)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(parent=self.urlPropertiesGroup)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.schemesEdit = QtWidgets.QLineEdit(parent=self.urlPropertiesGroup)
        self.schemesEdit.setClearButtonEnabled(True)
        self.schemesEdit.setObjectName("schemesEdit")
        self.horizontalLayout_4.addWidget(self.schemesEdit)
        self.verticalLayout.addWidget(self.urlPropertiesGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=FileDialogWizardDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(FileDialogWizardDialog)
        self.buttonBox.accepted.connect(FileDialogWizardDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(FileDialogWizardDialog.reject) # type: ignore
        self.parentOther.toggled['bool'].connect(self.parentEdit.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(FileDialogWizardDialog)
        FileDialogWizardDialog.setTabOrder(self.pyqtComboBox, self.rOpenFile)
        FileDialogWizardDialog.setTabOrder(self.rOpenFile, self.rOpenFiles)
        FileDialogWizardDialog.setTabOrder(self.rOpenFiles, self.rSaveFile)
        FileDialogWizardDialog.setTabOrder(self.rSaveFile, self.rDirectory)
        FileDialogWizardDialog.setTabOrder(self.rDirectory, self.rfOpenFile)
        FileDialogWizardDialog.setTabOrder(self.rfOpenFile, self.rfOpenFiles)
        FileDialogWizardDialog.setTabOrder(self.rfOpenFiles, self.rfSaveFile)
        FileDialogWizardDialog.setTabOrder(self.rfSaveFile, self.rOpenFileUrl)
        FileDialogWizardDialog.setTabOrder(self.rOpenFileUrl, self.rOpenFileUrls)
        FileDialogWizardDialog.setTabOrder(self.rOpenFileUrls, self.rSaveFileUrl)
        FileDialogWizardDialog.setTabOrder(self.rSaveFileUrl, self.rDirectoryUrl)
        FileDialogWizardDialog.setTabOrder(self.rDirectoryUrl, self.eNameVariable)
        FileDialogWizardDialog.setTabOrder(self.eNameVariable, self.eFilterVariable)
        FileDialogWizardDialog.setTabOrder(self.eFilterVariable, self.eCaption)
        FileDialogWizardDialog.setTabOrder(self.eCaption, self.cSymlinks)
        FileDialogWizardDialog.setTabOrder(self.cSymlinks, self.parentSelf)
        FileDialogWizardDialog.setTabOrder(self.parentSelf, self.parentNone)
        FileDialogWizardDialog.setTabOrder(self.parentNone, self.parentOther)
        FileDialogWizardDialog.setTabOrder(self.parentOther, self.parentEdit)
        FileDialogWizardDialog.setTabOrder(self.parentEdit, self.eStartWith)
        FileDialogWizardDialog.setTabOrder(self.eStartWith, self.cStartWith)
        FileDialogWizardDialog.setTabOrder(self.cStartWith, self.eFilters)
        FileDialogWizardDialog.setTabOrder(self.eFilters, self.cFilters)
        FileDialogWizardDialog.setTabOrder(self.cFilters, self.eInitialFilter)
        FileDialogWizardDialog.setTabOrder(self.eInitialFilter, self.cInitialFilter)
        FileDialogWizardDialog.setTabOrder(self.cInitialFilter, self.cConfirmOverwrite)
        FileDialogWizardDialog.setTabOrder(self.cConfirmOverwrite, self.eWorkDir)
        FileDialogWizardDialog.setTabOrder(self.eWorkDir, self.cWorkDir)
        FileDialogWizardDialog.setTabOrder(self.cWorkDir, self.cDirOnly)
        FileDialogWizardDialog.setTabOrder(self.cDirOnly, self.schemesEdit)

    def retranslateUi(self, FileDialogWizardDialog):
        _translate = QtCore.QCoreApplication.translate
        FileDialogWizardDialog.setWindowTitle(_translate("FileDialogWizardDialog", "QFileDialog Wizard"))
        self.label.setText(_translate("FileDialogWizardDialog", "Variant:"))
        self.typeGroupBox.setTitle(_translate("FileDialogWizardDialog", "Type"))
        self.rOpenFile.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open File\' dialog"))
        self.rOpenFile.setText(_translate("FileDialogWizardDialog", "Open File"))
        self.rOpenFiles.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open Files\' dialog"))
        self.rOpenFiles.setText(_translate("FileDialogWizardDialog", "Open Files"))
        self.rSaveFile.setToolTip(_translate("FileDialogWizardDialog", "Select to create a \'Save File\' dialog"))
        self.rSaveFile.setText(_translate("FileDialogWizardDialog", "Save File"))
        self.rDirectory.setToolTip(_translate("FileDialogWizardDialog", "Select to create a \'Select Directory\' dialog"))
        self.rDirectory.setText(_translate("FileDialogWizardDialog", "Select Directory"))
        self.rfOpenFile.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open File\' dialog capturing the selected filter"))
        self.rfOpenFile.setText(_translate("FileDialogWizardDialog", "Open File and Filter"))
        self.rfOpenFiles.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open Files\' dialog capturing the selected filter"))
        self.rfOpenFiles.setText(_translate("FileDialogWizardDialog", "Open Files and Filter"))
        self.rfSaveFile.setToolTip(_translate("FileDialogWizardDialog", "Select to create a \'Save File\' dialog capturing the selected filter"))
        self.rfSaveFile.setText(_translate("FileDialogWizardDialog", "Save File and Filter"))
        self.rOpenFileUrl.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open File\' dialog"))
        self.rOpenFileUrl.setText(_translate("FileDialogWizardDialog", "Open File URL"))
        self.rOpenFileUrls.setToolTip(_translate("FileDialogWizardDialog", "Select to create an \'Open Files\' dialog"))
        self.rOpenFileUrls.setText(_translate("FileDialogWizardDialog", "Open Files URL"))
        self.rSaveFileUrl.setToolTip(_translate("FileDialogWizardDialog", "Select to create a \'Save File\' dialog"))
        self.rSaveFileUrl.setText(_translate("FileDialogWizardDialog", "Save File URL"))
        self.rDirectoryUrl.setToolTip(_translate("FileDialogWizardDialog", "Select to create a \'Select Directory\' dialog"))
        self.rDirectoryUrl.setText(_translate("FileDialogWizardDialog", "Select Directory URL"))
        self.groupBox.setTitle(_translate("FileDialogWizardDialog", "Results"))
        self.label_2.setText(_translate("FileDialogWizardDialog", "Name Variable:"))
        self.eNameVariable.setToolTip(_translate("FileDialogWizardDialog", "Enter the result variable name"))
        self.lFilterVariable.setText(_translate("FileDialogWizardDialog", "Filter Variable:"))
        self.eFilterVariable.setToolTip(_translate("FileDialogWizardDialog", "Enter the name of the filter variable"))
        self.TextLabel1.setText(_translate("FileDialogWizardDialog", "Title:"))
        self.eCaption.setToolTip(_translate("FileDialogWizardDialog", "Enter the title text"))
        self.cSymlinks.setToolTip(_translate("FileDialogWizardDialog", "Check to resolve symbolic links"))
        self.cSymlinks.setText(_translate("FileDialogWizardDialog", "Resolve Symlinks"))
        self.parentGroup.setTitle(_translate("FileDialogWizardDialog", "Parent"))
        self.parentSelf.setToolTip(_translate("FileDialogWizardDialog", "Select \"self\" as parent"))
        self.parentSelf.setText(_translate("FileDialogWizardDialog", "self"))
        self.parentNone.setToolTip(_translate("FileDialogWizardDialog", "Select \"None\" as parent"))
        self.parentNone.setText(_translate("FileDialogWizardDialog", "None"))
        self.parentOther.setToolTip(_translate("FileDialogWizardDialog", "Select to enter a parent expression"))
        self.parentOther.setText(_translate("FileDialogWizardDialog", "Expression:"))
        self.parentEdit.setToolTip(_translate("FileDialogWizardDialog", "Enter the parent expression"))
        self.filePropertiesGroup.setTitle(_translate("FileDialogWizardDialog", "File Dialog Properties"))
        self.TextLabel3.setText(_translate("FileDialogWizardDialog", "Start With / Working Directory"))
        self.eStartWith.setToolTip(_translate("FileDialogWizardDialog", "Enter the working directory or a filename"))
        self.cStartWith.setToolTip(_translate("FileDialogWizardDialog", "Check this if the contents of the edit names a variable or variable function"))
        self.cStartWith.setText(_translate("FileDialogWizardDialog", "Is Variable"))
        self.TextLabel2.setText(_translate("FileDialogWizardDialog", "Filters"))
        self.eFilters.setToolTip(_translate("FileDialogWizardDialog", "Enter the filter specifications separated by \';;\'"))
        self.cFilters.setToolTip(_translate("FileDialogWizardDialog", "Check this if the contents of the edit names a variable or variable function"))
        self.cFilters.setText(_translate("FileDialogWizardDialog", "Is Variable"))
        self.lInitialFilter.setText(_translate("FileDialogWizardDialog", "Initial Filter"))
        self.eInitialFilter.setToolTip(_translate("FileDialogWizardDialog", "Enter the initial filter"))
        self.cInitialFilter.setToolTip(_translate("FileDialogWizardDialog", "Check this if the contents of the edit names a variable or variable function"))
        self.cInitialFilter.setText(_translate("FileDialogWizardDialog", "Is Variable"))
        self.cConfirmOverwrite.setToolTip(_translate("FileDialogWizardDialog", "Select to show an overwrite confirmation dialog"))
        self.cConfirmOverwrite.setText(_translate("FileDialogWizardDialog", "Show overwrite confirmation"))
        self.dirPropertiesGroup.setTitle(_translate("FileDialogWizardDialog", "Directory Dialog Properties"))
        self.eWorkDir.setToolTip(_translate("FileDialogWizardDialog", "Enter the working directory"))
        self.TextLabel4.setText(_translate("FileDialogWizardDialog", "Working Directory"))
        self.cWorkDir.setToolTip(_translate("FileDialogWizardDialog", "Check this if the contents of the edit names a variable or variable function"))
        self.cWorkDir.setText(_translate("FileDialogWizardDialog", "Is Variable"))
        self.cDirOnly.setToolTip(_translate("FileDialogWizardDialog", "Check to display directories only"))
        self.cDirOnly.setText(_translate("FileDialogWizardDialog", "Show Directories Only"))
        self.urlPropertiesGroup.setTitle(_translate("FileDialogWizardDialog", "URL Properties"))
        self.label_3.setText(_translate("FileDialogWizardDialog", "Supported Schemes:"))
        self.schemesEdit.setToolTip(_translate("FileDialogWizardDialog", "Enter the list of supported schemes separated by spaces"))
