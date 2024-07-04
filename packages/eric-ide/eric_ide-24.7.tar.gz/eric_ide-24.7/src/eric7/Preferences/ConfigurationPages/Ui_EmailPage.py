# Form implementation generated from reading ui file 'src/eric7/Preferences/ConfigurationPages/EmailPage.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EmailPage(object):
    def setupUi(self, EmailPage):
        EmailPage.setObjectName("EmailPage")
        EmailPage.resize(485, 580)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(EmailPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.headerLabel = QtWidgets.QLabel(parent=EmailPage)
        self.headerLabel.setObjectName("headerLabel")
        self.verticalLayout_3.addWidget(self.headerLabel)
        self.line16 = QtWidgets.QFrame(parent=EmailPage)
        self.line16.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line16.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line16.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line16.setObjectName("line16")
        self.verticalLayout_3.addWidget(self.line16)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.textLabel1_5 = QtWidgets.QLabel(parent=EmailPage)
        self.textLabel1_5.setObjectName("textLabel1_5")
        self.gridLayout_3.addWidget(self.textLabel1_5, 0, 0, 1, 1)
        self.emailEdit = QtWidgets.QLineEdit(parent=EmailPage)
        self.emailEdit.setObjectName("emailEdit")
        self.gridLayout_3.addWidget(self.emailEdit, 0, 1, 1, 1)
        self.textLabel1_6 = QtWidgets.QLabel(parent=EmailPage)
        self.textLabel1_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.textLabel1_6.setObjectName("textLabel1_6")
        self.gridLayout_3.addWidget(self.textLabel1_6, 1, 0, 1, 1)
        self.signatureEdit = QtWidgets.QTextEdit(parent=EmailPage)
        self.signatureEdit.setAcceptRichText(False)
        self.signatureEdit.setObjectName("signatureEdit")
        self.gridLayout_3.addWidget(self.signatureEdit, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=EmailPage)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.googleMailCheckBox = QtWidgets.QCheckBox(parent=self.groupBox_2)
        self.googleMailCheckBox.setObjectName("googleMailCheckBox")
        self.verticalLayout_2.addWidget(self.googleMailCheckBox)
        self.googleMailInfoLabel = QtWidgets.QLabel(parent=self.groupBox_2)
        self.googleMailInfoLabel.setWordWrap(True)
        self.googleMailInfoLabel.setObjectName("googleMailInfoLabel")
        self.verticalLayout_2.addWidget(self.googleMailInfoLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.googleHelpButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.googleHelpButton.setObjectName("googleHelpButton")
        self.horizontalLayout.addWidget(self.googleHelpButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.googleInstallButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.googleInstallButton.setObjectName("googleInstallButton")
        self.horizontalLayout.addWidget(self.googleInstallButton)
        self.googleCheckAgainButton = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.googleCheckAgainButton.setObjectName("googleCheckAgainButton")
        self.horizontalLayout.addWidget(self.googleCheckAgainButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(parent=EmailPage)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.textLabel2_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.textLabel2_2.setObjectName("textLabel2_2")
        self.gridLayout_2.addWidget(self.textLabel2_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)
        self.portSpin = QtWidgets.QSpinBox(parent=self.groupBox)
        self.portSpin.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.portSpin.setMinimum(1)
        self.portSpin.setMaximum(65535)
        self.portSpin.setProperty("value", 25)
        self.portSpin.setObjectName("portSpin")
        self.gridLayout_2.addWidget(self.portSpin, 2, 1, 1, 1)
        self.mailServerEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.mailServerEdit.setObjectName("mailServerEdit")
        self.gridLayout_2.addWidget(self.mailServerEdit, 0, 1, 1, 2)
        self.frame = QtWidgets.QFrame(parent=self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.noEncryptionButton = QtWidgets.QRadioButton(parent=self.frame)
        self.noEncryptionButton.setChecked(True)
        self.noEncryptionButton.setObjectName("noEncryptionButton")
        self.horizontalLayout_2.addWidget(self.noEncryptionButton)
        self.useSslButton = QtWidgets.QRadioButton(parent=self.frame)
        self.useSslButton.setObjectName("useSslButton")
        self.horizontalLayout_2.addWidget(self.useSslButton)
        self.useTlsButton = QtWidgets.QRadioButton(parent=self.frame)
        self.useTlsButton.setObjectName("useTlsButton")
        self.horizontalLayout_2.addWidget(self.useTlsButton)
        self.gridLayout_2.addWidget(self.frame, 1, 1, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.mailAuthenticationGroup = QtWidgets.QGroupBox(parent=self.groupBox)
        self.mailAuthenticationGroup.setCheckable(True)
        self.mailAuthenticationGroup.setObjectName("mailAuthenticationGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.mailAuthenticationGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.textLabel1_15 = QtWidgets.QLabel(parent=self.mailAuthenticationGroup)
        self.textLabel1_15.setObjectName("textLabel1_15")
        self.gridLayout.addWidget(self.textLabel1_15, 0, 0, 1, 1)
        self.mailUserEdit = QtWidgets.QLineEdit(parent=self.mailAuthenticationGroup)
        self.mailUserEdit.setObjectName("mailUserEdit")
        self.gridLayout.addWidget(self.mailUserEdit, 0, 1, 1, 1)
        self.textLabel2_7 = QtWidgets.QLabel(parent=self.mailAuthenticationGroup)
        self.textLabel2_7.setObjectName("textLabel2_7")
        self.gridLayout.addWidget(self.textLabel2_7, 1, 0, 1, 1)
        self.mailPasswordEdit = QtWidgets.QLineEdit(parent=self.mailAuthenticationGroup)
        self.mailPasswordEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.mailPasswordEdit.setObjectName("mailPasswordEdit")
        self.gridLayout.addWidget(self.mailPasswordEdit, 1, 1, 1, 1)
        self.testButton = QtWidgets.QPushButton(parent=self.mailAuthenticationGroup)
        self.testButton.setObjectName("testButton")
        self.gridLayout.addWidget(self.testButton, 2, 0, 1, 2)
        self.verticalLayout.addWidget(self.mailAuthenticationGroup)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)

        self.retranslateUi(EmailPage)
        self.googleMailCheckBox.toggled['bool'].connect(self.groupBox.setDisabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(EmailPage)
        EmailPage.setTabOrder(self.emailEdit, self.signatureEdit)
        EmailPage.setTabOrder(self.signatureEdit, self.googleMailCheckBox)
        EmailPage.setTabOrder(self.googleMailCheckBox, self.googleHelpButton)
        EmailPage.setTabOrder(self.googleHelpButton, self.googleInstallButton)
        EmailPage.setTabOrder(self.googleInstallButton, self.googleCheckAgainButton)
        EmailPage.setTabOrder(self.googleCheckAgainButton, self.mailServerEdit)
        EmailPage.setTabOrder(self.mailServerEdit, self.noEncryptionButton)
        EmailPage.setTabOrder(self.noEncryptionButton, self.useSslButton)
        EmailPage.setTabOrder(self.useSslButton, self.useTlsButton)
        EmailPage.setTabOrder(self.useTlsButton, self.portSpin)
        EmailPage.setTabOrder(self.portSpin, self.mailAuthenticationGroup)
        EmailPage.setTabOrder(self.mailAuthenticationGroup, self.mailUserEdit)
        EmailPage.setTabOrder(self.mailUserEdit, self.mailPasswordEdit)
        EmailPage.setTabOrder(self.mailPasswordEdit, self.testButton)

    def retranslateUi(self, EmailPage):
        _translate = QtCore.QCoreApplication.translate
        self.headerLabel.setText(_translate("EmailPage", "<b>Configure Email</b>"))
        self.textLabel1_5.setText(_translate("EmailPage", "Email address:"))
        self.emailEdit.setToolTip(_translate("EmailPage", "Enter your email address"))
        self.textLabel1_6.setText(_translate("EmailPage", "Signature:"))
        self.signatureEdit.setToolTip(_translate("EmailPage", "Enter your email signature"))
        self.groupBox_2.setTitle(_translate("EmailPage", "Google Mail"))
        self.googleMailCheckBox.setText(_translate("EmailPage", "Use Google Mail with OAuth2 authentication via Gmail API"))
        self.googleHelpButton.setToolTip(_translate("EmailPage", "Press to get some help for enabling the Google Mail API"))
        self.googleHelpButton.setText(_translate("EmailPage", "Google Mail API Help"))
        self.googleInstallButton.setToolTip(_translate("EmailPage", "Press to install the required Google API packages"))
        self.googleInstallButton.setText(_translate("EmailPage", "Install Google API Packages"))
        self.googleCheckAgainButton.setToolTip(_translate("EmailPage", "Press to check the availability again"))
        self.googleCheckAgainButton.setText(_translate("EmailPage", "Check Again"))
        self.groupBox.setTitle(_translate("EmailPage", "Standard Email"))
        self.label_2.setText(_translate("EmailPage", "Encryption Method:"))
        self.textLabel2_2.setText(_translate("EmailPage", "Outgoing mail server (SMTP):"))
        self.label.setText(_translate("EmailPage", "Port:"))
        self.portSpin.setToolTip(_translate("EmailPage", "Enter the port of the mail server"))
        self.mailServerEdit.setToolTip(_translate("EmailPage", "Enter the address of your mail server"))
        self.noEncryptionButton.setToolTip(_translate("EmailPage", "Select to use no encryption"))
        self.noEncryptionButton.setText(_translate("EmailPage", "None"))
        self.useSslButton.setToolTip(_translate("EmailPage", "Select to use SSL"))
        self.useSslButton.setText(_translate("EmailPage", "SSL"))
        self.useTlsButton.setToolTip(_translate("EmailPage", "Select to use TLS"))
        self.useTlsButton.setText(_translate("EmailPage", "TLS"))
        self.mailAuthenticationGroup.setToolTip(_translate("EmailPage", "Select to authenticatate against the mail server"))
        self.mailAuthenticationGroup.setTitle(_translate("EmailPage", "Mail server needs authentication"))
        self.textLabel1_15.setText(_translate("EmailPage", "Username:"))
        self.mailUserEdit.setToolTip(_translate("EmailPage", "Enter your mail server username"))
        self.textLabel2_7.setText(_translate("EmailPage", "Password:"))
        self.mailPasswordEdit.setToolTip(_translate("EmailPage", "Enter your password for accessing the mail server"))
        self.testButton.setToolTip(_translate("EmailPage", "Press to test the login data"))
        self.testButton.setText(_translate("EmailPage", "Test Login"))
