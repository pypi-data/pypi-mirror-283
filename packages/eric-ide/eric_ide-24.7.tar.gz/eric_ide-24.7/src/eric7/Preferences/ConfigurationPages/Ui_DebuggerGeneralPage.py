# Form implementation generated from reading ui file 'src/eric7/Preferences/ConfigurationPages/DebuggerGeneralPage.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DebuggerGeneralPage(object):
    def setupUi(self, DebuggerGeneralPage):
        DebuggerGeneralPage.setObjectName("DebuggerGeneralPage")
        DebuggerGeneralPage.resize(550, 1900)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(DebuggerGeneralPage)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.headerLabel = QtWidgets.QLabel(parent=DebuggerGeneralPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_9.addWidget(self.headerLabel)
        self.line11 = QtWidgets.QFrame(parent=DebuggerGeneralPage)
        self.line11.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line11.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line11.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line11.setObjectName("line11")
        self.verticalLayout_9.addWidget(self.line11)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.TextLabel1_2_3 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.TextLabel1_2_3.setWordWrap(True)
        self.TextLabel1_2_3.setObjectName("TextLabel1_2_3")
        self.verticalLayout_7.addWidget(self.TextLabel1_2_3)
        self.interfaceSelectorComboBox = QtWidgets.QComboBox(parent=self.groupBox_3)
        self.interfaceSelectorComboBox.setObjectName("interfaceSelectorComboBox")
        self.verticalLayout_7.addWidget(self.interfaceSelectorComboBox)
        self.interfacesCombo = QtWidgets.QComboBox(parent=self.groupBox_3)
        self.interfacesCombo.setEnabled(False)
        self.interfacesCombo.setObjectName("interfacesCombo")
        self.verticalLayout_7.addWidget(self.interfacesCombo)
        self.serverPortStaticGroup = QtWidgets.QGroupBox(parent=self.groupBox_3)
        self.serverPortStaticGroup.setCheckable(True)
        self.serverPortStaticGroup.setChecked(False)
        self.serverPortStaticGroup.setObjectName("serverPortStaticGroup")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.serverPortStaticGroup)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_5 = QtWidgets.QLabel(parent=self.serverPortStaticGroup)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.serverPortSpinBox = QtWidgets.QSpinBox(parent=self.serverPortStaticGroup)
        self.serverPortSpinBox.setMinimum(1025)
        self.serverPortSpinBox.setMaximum(65535)
        self.serverPortSpinBox.setSingleStep(1)
        self.serverPortSpinBox.setProperty("value", 35000)
        self.serverPortSpinBox.setObjectName("serverPortSpinBox")
        self.gridLayout_5.addWidget(self.serverPortSpinBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(333, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 2, 1, 1)
        self.serverPortIncrementCheckBox = QtWidgets.QCheckBox(parent=self.serverPortStaticGroup)
        self.serverPortIncrementCheckBox.setObjectName("serverPortIncrementCheckBox")
        self.gridLayout_5.addWidget(self.serverPortIncrementCheckBox, 1, 0, 1, 3)
        self.verticalLayout_7.addWidget(self.serverPortStaticGroup)
        self.verticalLayout_9.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridlayout = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridlayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.deleteAllowedHostButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.deleteAllowedHostButton.setEnabled(False)
        self.deleteAllowedHostButton.setObjectName("deleteAllowedHostButton")
        self.gridlayout.addWidget(self.deleteAllowedHostButton, 2, 1, 1, 1)
        self.editAllowedHostButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.editAllowedHostButton.setEnabled(False)
        self.editAllowedHostButton.setObjectName("editAllowedHostButton")
        self.gridlayout.addWidget(self.editAllowedHostButton, 1, 1, 1, 1)
        self.addAllowedHostButton = QtWidgets.QPushButton(parent=self.groupBox_4)
        self.addAllowedHostButton.setObjectName("addAllowedHostButton")
        self.gridlayout.addWidget(self.addAllowedHostButton, 0, 1, 1, 1)
        self.allowedHostsList = QtWidgets.QListWidget(parent=self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allowedHostsList.sizePolicy().hasHeightForWidth())
        self.allowedHostsList.setSizePolicy(sizePolicy)
        self.allowedHostsList.setObjectName("allowedHostsList")
        self.gridlayout.addWidget(self.allowedHostsList, 0, 0, 4, 1)
        self.verticalLayout_9.addWidget(self.groupBox_4)
        self.groupBox_12 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox_12)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.passiveDbgGroup = QtWidgets.QGroupBox(parent=self.groupBox_12)
        self.passiveDbgGroup.setCheckable(True)
        self.passiveDbgGroup.setChecked(False)
        self.passiveDbgGroup.setObjectName("passiveDbgGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.passiveDbgGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.TextLabel1_2_2 = QtWidgets.QLabel(parent=self.passiveDbgGroup)
        self.TextLabel1_2_2.setWordWrap(True)
        self.TextLabel1_2_2.setObjectName("TextLabel1_2_2")
        self.gridLayout.addWidget(self.TextLabel1_2_2, 0, 0, 1, 4)
        self.passiveDbgCheckBox = QtWidgets.QCheckBox(parent=self.passiveDbgGroup)
        self.passiveDbgCheckBox.setObjectName("passiveDbgCheckBox")
        self.gridLayout.addWidget(self.passiveDbgCheckBox, 1, 0, 1, 4)
        self.passiveDbgPortLabel = QtWidgets.QLabel(parent=self.passiveDbgGroup)
        self.passiveDbgPortLabel.setEnabled(False)
        self.passiveDbgPortLabel.setObjectName("passiveDbgPortLabel")
        self.gridLayout.addWidget(self.passiveDbgPortLabel, 2, 0, 1, 1)
        self.passiveDbgPortSpinBox = QtWidgets.QSpinBox(parent=self.passiveDbgGroup)
        self.passiveDbgPortSpinBox.setEnabled(False)
        self.passiveDbgPortSpinBox.setMinimum(1024)
        self.passiveDbgPortSpinBox.setMaximum(65535)
        self.passiveDbgPortSpinBox.setProperty("value", 42424)
        self.passiveDbgPortSpinBox.setObjectName("passiveDbgPortSpinBox")
        self.gridLayout.addWidget(self.passiveDbgPortSpinBox, 2, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.passiveDbgGroup)
        self.label.setEnabled(False)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.passiveDbgBackendCombo = QtWidgets.QComboBox(parent=self.passiveDbgGroup)
        self.passiveDbgBackendCombo.setEnabled(False)
        self.passiveDbgBackendCombo.setObjectName("passiveDbgBackendCombo")
        self.gridLayout.addWidget(self.passiveDbgBackendCombo, 3, 1, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 3, 1, 1)
        self.verticalLayout_2.addWidget(self.passiveDbgGroup)
        self.remoteDebuggerGroup = QtWidgets.QGroupBox(parent=self.groupBox_12)
        self.remoteDebuggerGroup.setCheckable(True)
        self.remoteDebuggerGroup.setChecked(False)
        self.remoteDebuggerGroup.setObjectName("remoteDebuggerGroup")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.remoteDebuggerGroup)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.hostLabel = QtWidgets.QLabel(parent=self.remoteDebuggerGroup)
        self.hostLabel.setObjectName("hostLabel")
        self.gridLayout_2.addWidget(self.hostLabel, 0, 0, 1, 1)
        self.hostLineEdit = QtWidgets.QLineEdit(parent=self.remoteDebuggerGroup)
        self.hostLineEdit.setObjectName("hostLineEdit")
        self.gridLayout_2.addWidget(self.hostLineEdit, 0, 1, 2, 1)
        self.execLabel = QtWidgets.QLabel(parent=self.remoteDebuggerGroup)
        self.execLabel.setObjectName("execLabel")
        self.gridLayout_2.addWidget(self.execLabel, 1, 0, 2, 1)
        self.execLineEdit = QtWidgets.QLineEdit(parent=self.remoteDebuggerGroup)
        self.execLineEdit.setObjectName("execLineEdit")
        self.gridLayout_2.addWidget(self.execLineEdit, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.remoteDebuggerGroup)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.remoteDebugClientEdit = QtWidgets.QLineEdit(parent=self.remoteDebuggerGroup)
        self.remoteDebugClientEdit.setClearButtonEnabled(True)
        self.remoteDebugClientEdit.setObjectName("remoteDebugClientEdit")
        self.gridLayout_2.addWidget(self.remoteDebugClientEdit, 3, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.remoteDebuggerGroup)
        self.dbgPathTranslationGroup = QtWidgets.QGroupBox(parent=self.groupBox_12)
        self.dbgPathTranslationGroup.setCheckable(True)
        self.dbgPathTranslationGroup.setChecked(False)
        self.dbgPathTranslationGroup.setObjectName("dbgPathTranslationGroup")
        self._2 = QtWidgets.QGridLayout(self.dbgPathTranslationGroup)
        self._2.setObjectName("_2")
        self.textLabel2_9 = QtWidgets.QLabel(parent=self.dbgPathTranslationGroup)
        self.textLabel2_9.setObjectName("textLabel2_9")
        self._2.addWidget(self.textLabel2_9, 1, 0, 1, 1)
        self.dbgTranslationLocalEdit = QtWidgets.QLineEdit(parent=self.dbgPathTranslationGroup)
        self.dbgTranslationLocalEdit.setObjectName("dbgTranslationLocalEdit")
        self._2.addWidget(self.dbgTranslationLocalEdit, 1, 1, 1, 1)
        self.dbgTranslationRemoteEdit = QtWidgets.QLineEdit(parent=self.dbgPathTranslationGroup)
        self.dbgTranslationRemoteEdit.setObjectName("dbgTranslationRemoteEdit")
        self._2.addWidget(self.dbgTranslationRemoteEdit, 0, 1, 1, 1)
        self.textLabel1_18 = QtWidgets.QLabel(parent=self.dbgPathTranslationGroup)
        self.textLabel1_18.setObjectName("textLabel1_18")
        self._2.addWidget(self.textLabel1_18, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.dbgPathTranslationGroup)
        self.verticalLayout_9.addWidget(self.groupBox_12)
        self.consoleDebuggerGroup = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.consoleDebuggerGroup.setCheckable(True)
        self.consoleDebuggerGroup.setObjectName("consoleDebuggerGroup")
        self._4 = QtWidgets.QGridLayout(self.consoleDebuggerGroup)
        self._4.setObjectName("_4")
        self.consoleDbgEdit = QtWidgets.QLineEdit(parent=self.consoleDebuggerGroup)
        self.consoleDbgEdit.setObjectName("consoleDbgEdit")
        self._4.addWidget(self.consoleDbgEdit, 0, 1, 1, 1)
        self.textLabel1_17 = QtWidgets.QLabel(parent=self.consoleDebuggerGroup)
        self.textLabel1_17.setObjectName("textLabel1_17")
        self._4.addWidget(self.textLabel1_17, 0, 0, 1, 1)
        self.verticalLayout_9.addWidget(self.consoleDebuggerGroup)
        self.groupBox_5 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_5.setObjectName("groupBox_5")
        self._3 = QtWidgets.QGridLayout(self.groupBox_5)
        self._3.setObjectName("_3")
        self.debugEnvironReplaceCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_5)
        self.debugEnvironReplaceCheckBox.setObjectName("debugEnvironReplaceCheckBox")
        self._3.addWidget(self.debugEnvironReplaceCheckBox, 0, 0, 1, 2)
        self.textLabel1_16 = QtWidgets.QLabel(parent=self.groupBox_5)
        self.textLabel1_16.setObjectName("textLabel1_16")
        self._3.addWidget(self.textLabel1_16, 1, 0, 1, 1)
        self.debugEnvironEdit = QtWidgets.QLineEdit(parent=self.groupBox_5)
        self.debugEnvironEdit.setObjectName("debugEnvironEdit")
        self._3.addWidget(self.debugEnvironEdit, 1, 1, 1, 1)
        self.verticalLayout_9.addWidget(self.groupBox_5)
        self.groupBox = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.debugAutoSaveScriptsCheckBox = QtWidgets.QCheckBox(parent=self.groupBox)
        self.debugAutoSaveScriptsCheckBox.setObjectName("debugAutoSaveScriptsCheckBox")
        self.verticalLayout.addWidget(self.debugAutoSaveScriptsCheckBox)
        self.verticalLayout_9.addWidget(self.groupBox)
        self.groupBox_7 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.automaticResetCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_7)
        self.automaticResetCheckBox.setObjectName("automaticResetCheckBox")
        self.verticalLayout_3.addWidget(self.automaticResetCheckBox)
        self.verticalLayout_9.addWidget(self.groupBox_7)
        self.groupBox_6 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.multiprocessCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_6)
        self.multiprocessCheckBox.setObjectName("multiprocessCheckBox")
        self.verticalLayout_8.addWidget(self.multiprocessCheckBox)
        self.verticalLayout_9.addWidget(self.groupBox_6)
        self.groupBox_8 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.debugThreeStateBreakPoint = QtWidgets.QCheckBox(parent=self.groupBox_8)
        self.debugThreeStateBreakPoint.setObjectName("debugThreeStateBreakPoint")
        self.gridLayout_4.addWidget(self.debugThreeStateBreakPoint, 0, 0, 1, 1)
        self.intelligentBreakPointCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_8)
        self.intelligentBreakPointCheckBox.setObjectName("intelligentBreakPointCheckBox")
        self.gridLayout_4.addWidget(self.intelligentBreakPointCheckBox, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox_8)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.recentFilesSpinBox = QtWidgets.QSpinBox(parent=self.groupBox_8)
        self.recentFilesSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.recentFilesSpinBox.setMinimum(5)
        self.recentFilesSpinBox.setMaximum(50)
        self.recentFilesSpinBox.setObjectName("recentFilesSpinBox")
        self.horizontalLayout_2.addWidget(self.recentFilesSpinBox)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.verticalLayout_9.addWidget(self.groupBox_8)
        self.groupBox_9 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_9.setObjectName("groupBox_9")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.exceptionBreakCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_9)
        self.exceptionBreakCheckBox.setObjectName("exceptionBreakCheckBox")
        self.verticalLayout_4.addWidget(self.exceptionBreakCheckBox)
        self.exceptionShellCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_9)
        self.exceptionShellCheckBox.setObjectName("exceptionShellCheckBox")
        self.verticalLayout_4.addWidget(self.exceptionShellCheckBox)
        self.verticalLayout_9.addWidget(self.groupBox_9)
        self.groupBox_11 = QtWidgets.QGroupBox(parent=DebuggerGeneralPage)
        self.groupBox_11.setObjectName("groupBox_11")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_11)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox_11)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.maxSizeSpinBox = QtWidgets.QSpinBox(parent=self.groupBox_11)
        self.maxSizeSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.maxSizeSpinBox.setProperty("showGroupSeparator", True)
        self.maxSizeSpinBox.setMaximum(1063256064)
        self.maxSizeSpinBox.setSingleStep(16384)
        self.maxSizeSpinBox.setObjectName("maxSizeSpinBox")
        self.horizontalLayout.addWidget(self.maxSizeSpinBox)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.groupBox_11)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(-1, 8, -1, 8)
        self.gridLayout_3.setVerticalSpacing(16)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.backgroundChangedButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.backgroundChangedButton.setMinimumSize(QtCore.QSize(100, 0))
        self.backgroundChangedButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.backgroundChangedButton.setText("")
        self.backgroundChangedButton.setObjectName("backgroundChangedButton")
        self.gridLayout_3.addWidget(self.backgroundChangedButton, 1, 1, 1, 1)
        self.label_bgChangedItems = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_bgChangedItems.setObjectName("label_bgChangedItems")
        self.gridLayout_3.addWidget(self.label_bgChangedItems, 1, 0, 1, 1)
        self.label_bgFirstLoaded = QtWidgets.QLabel(parent=self.groupBox_2)
        self.label_bgFirstLoaded.setObjectName("label_bgFirstLoaded")
        self.gridLayout_3.addWidget(self.label_bgFirstLoaded, 0, 0, 1, 1)
        self.backgroundNewButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.backgroundNewButton.setMinimumSize(QtCore.QSize(100, 0))
        self.backgroundNewButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.backgroundNewButton.setText("")
        self.backgroundNewButton.setObjectName("backgroundNewButton")
        self.gridLayout_3.addWidget(self.backgroundNewButton, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 0, 2, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_3)
        self.preView = QtWidgets.QListView(parent=self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preView.sizePolicy().hasHeightForWidth())
        self.preView.setSizePolicy(sizePolicy)
        self.preView.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.preView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preView.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.preView.setAlternatingRowColors(True)
        self.preView.setObjectName("preView")
        self.horizontalLayout_3.addWidget(self.preView)
        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.groupBox_10 = QtWidgets.QGroupBox(parent=self.groupBox_11)
        self.groupBox_10.setObjectName("groupBox_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.autoViewSourcecodeCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_10)
        self.autoViewSourcecodeCheckBox.setObjectName("autoViewSourcecodeCheckBox")
        self.verticalLayout_5.addWidget(self.autoViewSourcecodeCheckBox)
        self.verticalLayout_6.addWidget(self.groupBox_10)
        self.verticalLayout_9.addWidget(self.groupBox_11)
        self.hostLabel.setBuddy(self.hostLineEdit)
        self.execLabel.setBuddy(self.execLineEdit)

        self.retranslateUi(DebuggerGeneralPage)
        self.passiveDbgCheckBox.toggled['bool'].connect(self.passiveDbgPortLabel.setEnabled) # type: ignore
        self.passiveDbgCheckBox.toggled['bool'].connect(self.passiveDbgPortSpinBox.setEnabled) # type: ignore
        self.passiveDbgCheckBox.toggled['bool'].connect(self.label.setEnabled) # type: ignore
        self.passiveDbgCheckBox.toggled['bool'].connect(self.passiveDbgBackendCombo.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DebuggerGeneralPage)
        DebuggerGeneralPage.setTabOrder(self.interfaceSelectorComboBox, self.interfacesCombo)
        DebuggerGeneralPage.setTabOrder(self.interfacesCombo, self.serverPortStaticGroup)
        DebuggerGeneralPage.setTabOrder(self.serverPortStaticGroup, self.serverPortSpinBox)
        DebuggerGeneralPage.setTabOrder(self.serverPortSpinBox, self.serverPortIncrementCheckBox)
        DebuggerGeneralPage.setTabOrder(self.serverPortIncrementCheckBox, self.allowedHostsList)
        DebuggerGeneralPage.setTabOrder(self.allowedHostsList, self.addAllowedHostButton)
        DebuggerGeneralPage.setTabOrder(self.addAllowedHostButton, self.editAllowedHostButton)
        DebuggerGeneralPage.setTabOrder(self.editAllowedHostButton, self.deleteAllowedHostButton)
        DebuggerGeneralPage.setTabOrder(self.deleteAllowedHostButton, self.passiveDbgGroup)
        DebuggerGeneralPage.setTabOrder(self.passiveDbgGroup, self.passiveDbgCheckBox)
        DebuggerGeneralPage.setTabOrder(self.passiveDbgCheckBox, self.passiveDbgPortSpinBox)
        DebuggerGeneralPage.setTabOrder(self.passiveDbgPortSpinBox, self.passiveDbgBackendCombo)
        DebuggerGeneralPage.setTabOrder(self.passiveDbgBackendCombo, self.remoteDebuggerGroup)
        DebuggerGeneralPage.setTabOrder(self.remoteDebuggerGroup, self.hostLineEdit)
        DebuggerGeneralPage.setTabOrder(self.hostLineEdit, self.execLineEdit)
        DebuggerGeneralPage.setTabOrder(self.execLineEdit, self.remoteDebugClientEdit)
        DebuggerGeneralPage.setTabOrder(self.remoteDebugClientEdit, self.dbgPathTranslationGroup)
        DebuggerGeneralPage.setTabOrder(self.dbgPathTranslationGroup, self.dbgTranslationRemoteEdit)
        DebuggerGeneralPage.setTabOrder(self.dbgTranslationRemoteEdit, self.dbgTranslationLocalEdit)
        DebuggerGeneralPage.setTabOrder(self.dbgTranslationLocalEdit, self.consoleDebuggerGroup)
        DebuggerGeneralPage.setTabOrder(self.consoleDebuggerGroup, self.consoleDbgEdit)
        DebuggerGeneralPage.setTabOrder(self.consoleDbgEdit, self.debugEnvironReplaceCheckBox)
        DebuggerGeneralPage.setTabOrder(self.debugEnvironReplaceCheckBox, self.debugEnvironEdit)
        DebuggerGeneralPage.setTabOrder(self.debugEnvironEdit, self.debugAutoSaveScriptsCheckBox)
        DebuggerGeneralPage.setTabOrder(self.debugAutoSaveScriptsCheckBox, self.automaticResetCheckBox)
        DebuggerGeneralPage.setTabOrder(self.automaticResetCheckBox, self.multiprocessCheckBox)
        DebuggerGeneralPage.setTabOrder(self.multiprocessCheckBox, self.debugThreeStateBreakPoint)
        DebuggerGeneralPage.setTabOrder(self.debugThreeStateBreakPoint, self.intelligentBreakPointCheckBox)
        DebuggerGeneralPage.setTabOrder(self.intelligentBreakPointCheckBox, self.recentFilesSpinBox)
        DebuggerGeneralPage.setTabOrder(self.recentFilesSpinBox, self.exceptionBreakCheckBox)
        DebuggerGeneralPage.setTabOrder(self.exceptionBreakCheckBox, self.exceptionShellCheckBox)
        DebuggerGeneralPage.setTabOrder(self.exceptionShellCheckBox, self.maxSizeSpinBox)
        DebuggerGeneralPage.setTabOrder(self.maxSizeSpinBox, self.backgroundNewButton)
        DebuggerGeneralPage.setTabOrder(self.backgroundNewButton, self.backgroundChangedButton)
        DebuggerGeneralPage.setTabOrder(self.backgroundChangedButton, self.autoViewSourcecodeCheckBox)

    def retranslateUi(self, DebuggerGeneralPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("DebuggerGeneralPage", "<b>Configure general debugger settings</b>"))
        self.groupBox_3.setTitle(_translate("DebuggerGeneralPage", "Network Interface"))
        self.TextLabel1_2_3.setText(_translate("DebuggerGeneralPage", "<font color=\"#FF0000\"><b>Note:</b> These settings are activated at the next startup of the application.</font>"))
        self.interfaceSelectorComboBox.setToolTip(_translate("DebuggerGeneralPage", "Select the interface(s) to listen on"))
        self.interfacesCombo.setToolTip(_translate("DebuggerGeneralPage", "Select the network interface to listen on"))
        self.serverPortStaticGroup.setToolTip(_translate("DebuggerGeneralPage", "Select to listen on a fixed network port"))
        self.serverPortStaticGroup.setTitle(_translate("DebuggerGeneralPage", "Static Server Port"))
        self.label_5.setText(_translate("DebuggerGeneralPage", "Server Port:"))
        self.serverPortSpinBox.setToolTip(_translate("DebuggerGeneralPage", "Enter the port number to listen on"))
        self.serverPortIncrementCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select to increment the server port to listen on if the configured one is unavailable"))
        self.serverPortIncrementCheckBox.setText(_translate("DebuggerGeneralPage", "Increment server port if unavailable"))
        self.groupBox_4.setTitle(_translate("DebuggerGeneralPage", "Allowed hosts"))
        self.deleteAllowedHostButton.setText(_translate("DebuggerGeneralPage", "Delete"))
        self.editAllowedHostButton.setText(_translate("DebuggerGeneralPage", "Edit..."))
        self.addAllowedHostButton.setText(_translate("DebuggerGeneralPage", "Add..."))
        self.groupBox_12.setTitle(_translate("DebuggerGeneralPage", "Remote Debugging"))
        self.label_3.setText(_translate("DebuggerGeneralPage", "<font color=\"#FF0000\"><b>Note:</b> Only one or none of \'Passive\' or \'Remote Debugger must be activated.</font>"))
        self.passiveDbgGroup.setTitle(_translate("DebuggerGeneralPage", "Passive Debugger"))
        self.TextLabel1_2_2.setText(_translate("DebuggerGeneralPage", "<font color=\"#FF0000\"><b>Note:</b> These settings are activated at the next startup of the application.</font>"))
        self.passiveDbgCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Enables the passive debug mode"))
        self.passiveDbgCheckBox.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Passive Debugger Enabled</b>\n"
"<p>This enables the passive debugging mode. In this mode the debug client (the script) connects to the debug server (the IDE). The script is started outside the IDE. This way mod_python or Zope scripts can be debugged.</p>"))
        self.passiveDbgCheckBox.setText(_translate("DebuggerGeneralPage", "Passive Debugger Enabled"))
        self.passiveDbgPortLabel.setText(_translate("DebuggerGeneralPage", "Debug Server Port:"))
        self.passiveDbgPortSpinBox.setToolTip(_translate("DebuggerGeneralPage", "Enter the port the debugger should listen on"))
        self.passiveDbgPortSpinBox.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Debug Server Port</b>\n"
"<p>Enter the port the debugger should listen on.</p>"))
        self.label.setText(_translate("DebuggerGeneralPage", "Debugger Type:"))
        self.passiveDbgBackendCombo.setToolTip(_translate("DebuggerGeneralPage", "Select the debugger type of the backend"))
        self.remoteDebuggerGroup.setToolTip(_translate("DebuggerGeneralPage", "Select, if the debugger should be run remotely"))
        self.remoteDebuggerGroup.setTitle(_translate("DebuggerGeneralPage", "Remote Debugger"))
        self.hostLabel.setText(_translate("DebuggerGeneralPage", "Remote Host:"))
        self.hostLineEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the hostname of the remote machine."))
        self.hostLineEdit.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Remote Host</b>\n"
"<p>Enter the hostname of the remote machine.</p>"))
        self.execLabel.setText(_translate("DebuggerGeneralPage", "Remote Execution:"))
        self.execLineEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the remote execution command."))
        self.execLineEdit.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Remote Execution</b>\n"
"<p>Enter the remote execution command (e.g. ssh). This command is used to log into the remote host and execute the remote debugger.</p>"))
        self.label_6.setText(_translate("DebuggerGeneralPage", "Remote Debug Client:"))
        self.remoteDebugClientEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the absolute path of the debug client of the remote host."))
        self.dbgPathTranslationGroup.setToolTip(_translate("DebuggerGeneralPage", "Select, if path translation for remote debugging should be done"))
        self.dbgPathTranslationGroup.setTitle(_translate("DebuggerGeneralPage", "Perform Path Translation"))
        self.textLabel2_9.setText(_translate("DebuggerGeneralPage", "Local Path:"))
        self.dbgTranslationLocalEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the local path"))
        self.dbgTranslationRemoteEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the remote path"))
        self.textLabel1_18.setText(_translate("DebuggerGeneralPage", "Remote Path:"))
        self.consoleDebuggerGroup.setToolTip(_translate("DebuggerGeneralPage", "Select, if the debugger should be executed in a console window"))
        self.consoleDebuggerGroup.setTitle(_translate("DebuggerGeneralPage", "Console Debugger"))
        self.consoleDbgEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the console command (e.g. xterm -e)"))
        self.consoleDbgEdit.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Console Command</b>\n"
"<p>Enter the console command (e.g. xterm -e). This command is used to open a command window for the debugger.</p>"))
        self.textLabel1_17.setText(_translate("DebuggerGeneralPage", "Console Command:"))
        self.groupBox_5.setTitle(_translate("DebuggerGeneralPage", "Environment Variables for Debug Client"))
        self.debugEnvironReplaceCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select, if the environment should be replaced."))
        self.debugEnvironReplaceCheckBox.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Replace Environment</b>\n"
"<p>If this entry is checked, the environment of the debugger will be replaced by the entries of the environment variables field. If it is unchecked, the environment will be ammended by these settings.</p>"))
        self.debugEnvironReplaceCheckBox.setText(_translate("DebuggerGeneralPage", "Replace Environment Variables"))
        self.textLabel1_16.setText(_translate("DebuggerGeneralPage", "Environment Variables:"))
        self.debugEnvironEdit.setToolTip(_translate("DebuggerGeneralPage", "Enter the environment variables to be set."))
        self.debugEnvironEdit.setWhatsThis(_translate("DebuggerGeneralPage", "<b>Environment Variables</b>\n"
"<p>Enter the environment variables to be set for the debugger. The individual settings must be separated by whitespace and be given in the form \'var=value\'.</p>\n"
"<p>Example: var1=1 var2=\"hello world\"</p>"))
        self.groupBox.setTitle(_translate("DebuggerGeneralPage", "Start Debugging"))
        self.debugAutoSaveScriptsCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select, whether changed scripts should be saved upon a debug, run, ... action."))
        self.debugAutoSaveScriptsCheckBox.setText(_translate("DebuggerGeneralPage", "Autosave changed scripts"))
        self.groupBox_7.setTitle(_translate("DebuggerGeneralPage", "Debug Client Exit"))
        self.automaticResetCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select, whether a reset of the debug client should be performed after a client exit"))
        self.automaticResetCheckBox.setText(_translate("DebuggerGeneralPage", "Automatic Reset after Client Exit"))
        self.groupBox_6.setTitle(_translate("DebuggerGeneralPage", "Multi Process Debugging"))
        self.multiprocessCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select to enable multiprocess debugging support globally"))
        self.multiprocessCheckBox.setText(_translate("DebuggerGeneralPage", "Enable Multi Process Debugging Support"))
        self.groupBox_8.setTitle(_translate("DebuggerGeneralPage", "Breakpoints"))
        self.debugThreeStateBreakPoint.setToolTip(_translate("DebuggerGeneralPage", "Select to change the breakpoint toggle order from Off->On->Off to Off->On (permanent)->On (temporary)->Off"))
        self.debugThreeStateBreakPoint.setText(_translate("DebuggerGeneralPage", "Three state breakpoint"))
        self.intelligentBreakPointCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select to move a breakpoint to a line generating executable code"))
        self.intelligentBreakPointCheckBox.setText(_translate("DebuggerGeneralPage", "Intelligent breakpoint"))
        self.label_4.setText(_translate("DebuggerGeneralPage", "Number of recent files and conditions:"))
        self.recentFilesSpinBox.setToolTip(_translate("DebuggerGeneralPage", "Enter the number of recent files and breakpoint conditions to remember"))
        self.groupBox_9.setTitle(_translate("DebuggerGeneralPage", "Exceptions"))
        self.exceptionBreakCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select to always break at exceptions"))
        self.exceptionBreakCheckBox.setText(_translate("DebuggerGeneralPage", "Always break at exceptions"))
        self.exceptionShellCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Select to show exception information in the shell window"))
        self.exceptionShellCheckBox.setText(_translate("DebuggerGeneralPage", "Show exceptions in Shell"))
        self.groupBox_11.setTitle(_translate("DebuggerGeneralPage", "Variables Viewer"))
        self.label_2.setText(_translate("DebuggerGeneralPage", "Max. Variable Size:"))
        self.maxSizeSpinBox.setToolTip(_translate("DebuggerGeneralPage", "Enter the maximum size of a variable to be shown (0 = no limit)"))
        self.maxSizeSpinBox.setSpecialValueText(_translate("DebuggerGeneralPage", "no limit"))
        self.maxSizeSpinBox.setSuffix(_translate("DebuggerGeneralPage", " Bytes"))
        self.groupBox_2.setTitle(_translate("DebuggerGeneralPage", "Background Colors"))
        self.backgroundChangedButton.setToolTip(_translate("DebuggerGeneralPage", "Select the background color for changed items."))
        self.label_bgChangedItems.setText(_translate("DebuggerGeneralPage", "Changed elements:"))
        self.label_bgFirstLoaded.setText(_translate("DebuggerGeneralPage", "First time opened elements:"))
        self.backgroundNewButton.setToolTip(_translate("DebuggerGeneralPage", "Select the background color for elements which are loaded for the first time."))
        self.groupBox_10.setTitle(_translate("DebuggerGeneralPage", "Local Variables Viewer"))
        self.autoViewSourcecodeCheckBox.setToolTip(_translate("DebuggerGeneralPage", "Automatically view source code when user changes the callstack frame in the callstack viewer."))
        self.autoViewSourcecodeCheckBox.setText(_translate("DebuggerGeneralPage", "Automatically view source code"))
