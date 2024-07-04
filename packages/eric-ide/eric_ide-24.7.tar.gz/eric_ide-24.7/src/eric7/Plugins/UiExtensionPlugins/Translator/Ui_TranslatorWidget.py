# Form implementation generated from reading ui file 'src/eric7/Plugins/UiExtensionPlugins/Translator/TranslatorWidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TranslatorWidget(object):
    def setupUi(self, TranslatorWidget):
        TranslatorWidget.setObjectName("TranslatorWidget")
        TranslatorWidget.resize(817, 144)
        self.verticalLayout = QtWidgets.QVBoxLayout(TranslatorWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.engineComboBox = QtWidgets.QComboBox(parent=TranslatorWidget)
        self.engineComboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.engineComboBox.setObjectName("engineComboBox")
        self.horizontalLayout.addWidget(self.engineComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.preferencesButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.preferencesButton.setObjectName("preferencesButton")
        self.horizontalLayout.addWidget(self.preferencesButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pronounceOrigButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.pronounceOrigButton.setObjectName("pronounceOrigButton")
        self.gridLayout.addWidget(self.pronounceOrigButton, 0, 0, 1, 1)
        self.origLanguageComboBox = QtWidgets.QComboBox(parent=TranslatorWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.origLanguageComboBox.sizePolicy().hasHeightForWidth())
        self.origLanguageComboBox.setSizePolicy(sizePolicy)
        self.origLanguageComboBox.setObjectName("origLanguageComboBox")
        self.gridLayout.addWidget(self.origLanguageComboBox, 0, 1, 1, 1)
        self.swapButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.swapButton.setObjectName("swapButton")
        self.gridLayout.addWidget(self.swapButton, 0, 2, 1, 1)
        self.transLanguageComboBox = QtWidgets.QComboBox(parent=TranslatorWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transLanguageComboBox.sizePolicy().hasHeightForWidth())
        self.transLanguageComboBox.setSizePolicy(sizePolicy)
        self.transLanguageComboBox.setObjectName("transLanguageComboBox")
        self.gridLayout.addWidget(self.transLanguageComboBox, 0, 3, 1, 1)
        self.pronounceTransButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.pronounceTransButton.setObjectName("pronounceTransButton")
        self.gridLayout.addWidget(self.pronounceTransButton, 0, 4, 1, 1)
        self.origEdit = QtWidgets.QPlainTextEdit(parent=TranslatorWidget)
        self.origEdit.setTabChangesFocus(True)
        self.origEdit.setObjectName("origEdit")
        self.gridLayout.addWidget(self.origEdit, 1, 0, 4, 2)
        spacerItem1 = QtWidgets.QSpacerItem(23, 68, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.transEdit = QtWidgets.QTextEdit(parent=TranslatorWidget)
        self.transEdit.setTabChangesFocus(True)
        self.transEdit.setReadOnly(True)
        self.transEdit.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.transEdit.setObjectName("transEdit")
        self.gridLayout.addWidget(self.transEdit, 1, 3, 4, 2)
        self.translateButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.translateButton.setObjectName("translateButton")
        self.gridLayout.addWidget(self.translateButton, 2, 2, 1, 1)
        self.clearButton = QtWidgets.QToolButton(parent=TranslatorWidget)
        self.clearButton.setObjectName("clearButton")
        self.gridLayout.addWidget(self.clearButton, 3, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(23, 28, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(TranslatorWidget)
        QtCore.QMetaObject.connectSlotsByName(TranslatorWidget)
        TranslatorWidget.setTabOrder(self.engineComboBox, self.pronounceOrigButton)
        TranslatorWidget.setTabOrder(self.pronounceOrigButton, self.origLanguageComboBox)
        TranslatorWidget.setTabOrder(self.origLanguageComboBox, self.swapButton)
        TranslatorWidget.setTabOrder(self.swapButton, self.transLanguageComboBox)
        TranslatorWidget.setTabOrder(self.transLanguageComboBox, self.pronounceTransButton)
        TranslatorWidget.setTabOrder(self.pronounceTransButton, self.origEdit)
        TranslatorWidget.setTabOrder(self.origEdit, self.translateButton)
        TranslatorWidget.setTabOrder(self.translateButton, self.transEdit)
        TranslatorWidget.setTabOrder(self.transEdit, self.clearButton)

    def retranslateUi(self, TranslatorWidget):
        _translate = QtCore.QCoreApplication.translate
        self.engineComboBox.setToolTip(_translate("TranslatorWidget", "Select the translation service"))
        self.preferencesButton.setToolTip(_translate("TranslatorWidget", "Press to open the Translator configuration page"))
        self.pronounceOrigButton.setToolTip(_translate("TranslatorWidget", "Press to pronounce the entered text"))
        self.origLanguageComboBox.setToolTip(_translate("TranslatorWidget", "Select the language of the original text"))
        self.swapButton.setToolTip(_translate("TranslatorWidget", "Press to swap the translation direction"))
        self.transLanguageComboBox.setToolTip(_translate("TranslatorWidget", "Select the language for the translated text"))
        self.pronounceTransButton.setToolTip(_translate("TranslatorWidget", "Press to pronounce the translated text"))
        self.origEdit.setToolTip(_translate("TranslatorWidget", "Enter the text to be translated"))
        self.transEdit.setToolTip(_translate("TranslatorWidget", "Shows the translated text"))
        self.translateButton.setToolTip(_translate("TranslatorWidget", "Press to translate the entered text"))
        self.clearButton.setToolTip(_translate("TranslatorWidget", "Press to clear the text fields"))
