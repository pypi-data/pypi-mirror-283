# Form implementation generated from reading ui file 'src/eric7/EricNetwork/EricSslCertificatesInfoWidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_EricSslCertificatesInfoWidget(object):
    def setupUi(self, EricSslCertificatesInfoWidget):
        EricSslCertificatesInfoWidget.setObjectName("EricSslCertificatesInfoWidget")
        EricSslCertificatesInfoWidget.resize(500, 512)
        self.verticalLayout = QtWidgets.QVBoxLayout(EricSslCertificatesInfoWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_17 = QtWidgets.QLabel(parent=EricSslCertificatesInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.verticalLayout.addWidget(self.label_17)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chainLabel = QtWidgets.QLabel(parent=EricSslCertificatesInfoWidget)
        self.chainLabel.setObjectName("chainLabel")
        self.horizontalLayout.addWidget(self.chainLabel)
        self.chainComboBox = QtWidgets.QComboBox(parent=EricSslCertificatesInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chainComboBox.sizePolicy().hasHeightForWidth())
        self.chainComboBox.setSizePolicy(sizePolicy)
        self.chainComboBox.setObjectName("chainComboBox")
        self.horizontalLayout.addWidget(self.chainComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.prohibitedLabel = QtWidgets.QLabel(parent=EricSslCertificatesInfoWidget)
        self.prohibitedLabel.setObjectName("prohibitedLabel")
        self.verticalLayout.addWidget(self.prohibitedLabel)
        self.groupBox = QtWidgets.QGroupBox(parent=EricSslCertificatesInfoWidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.subjectCommonNameLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectCommonNameLabel.sizePolicy().hasHeightForWidth())
        self.subjectCommonNameLabel.setSizePolicy(sizePolicy)
        self.subjectCommonNameLabel.setText("")
        self.subjectCommonNameLabel.setObjectName("subjectCommonNameLabel")
        self.gridLayout.addWidget(self.subjectCommonNameLabel, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.subjectOrganizationLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectOrganizationLabel.sizePolicy().hasHeightForWidth())
        self.subjectOrganizationLabel.setSizePolicy(sizePolicy)
        self.subjectOrganizationLabel.setText("")
        self.subjectOrganizationLabel.setObjectName("subjectOrganizationLabel")
        self.gridLayout.addWidget(self.subjectOrganizationLabel, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.subjectOrganizationalUnitLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectOrganizationalUnitLabel.sizePolicy().hasHeightForWidth())
        self.subjectOrganizationalUnitLabel.setSizePolicy(sizePolicy)
        self.subjectOrganizationalUnitLabel.setText("")
        self.subjectOrganizationalUnitLabel.setObjectName("subjectOrganizationalUnitLabel")
        self.gridLayout.addWidget(self.subjectOrganizationalUnitLabel, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.serialNumberLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serialNumberLabel.sizePolicy().hasHeightForWidth())
        self.serialNumberLabel.setSizePolicy(sizePolicy)
        self.serialNumberLabel.setText("")
        self.serialNumberLabel.setObjectName("serialNumberLabel")
        self.gridLayout.addWidget(self.serialNumberLabel, 4, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 1)
        self.issuerCommonNameLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerCommonNameLabel.sizePolicy().hasHeightForWidth())
        self.issuerCommonNameLabel.setSizePolicy(sizePolicy)
        self.issuerCommonNameLabel.setText("")
        self.issuerCommonNameLabel.setObjectName("issuerCommonNameLabel")
        self.gridLayout.addWidget(self.issuerCommonNameLabel, 7, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)
        self.issuerOrganizationLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerOrganizationLabel.sizePolicy().hasHeightForWidth())
        self.issuerOrganizationLabel.setSizePolicy(sizePolicy)
        self.issuerOrganizationLabel.setText("")
        self.issuerOrganizationLabel.setObjectName("issuerOrganizationLabel")
        self.gridLayout.addWidget(self.issuerOrganizationLabel, 8, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 1)
        self.issuerOrganizationalUnitLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.issuerOrganizationalUnitLabel.sizePolicy().hasHeightForWidth())
        self.issuerOrganizationalUnitLabel.setSizePolicy(sizePolicy)
        self.issuerOrganizationalUnitLabel.setText("")
        self.issuerOrganizationalUnitLabel.setObjectName("issuerOrganizationalUnitLabel")
        self.gridLayout.addWidget(self.issuerOrganizationalUnitLabel, 9, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 9, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 10, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 11, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 12, 0, 1, 1)
        self.effectiveLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.effectiveLabel.sizePolicy().hasHeightForWidth())
        self.effectiveLabel.setSizePolicy(sizePolicy)
        self.effectiveLabel.setText("")
        self.effectiveLabel.setObjectName("effectiveLabel")
        self.gridLayout.addWidget(self.effectiveLabel, 12, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 13, 0, 1, 1)
        self.expiresLabel = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expiresLabel.sizePolicy().hasHeightForWidth())
        self.expiresLabel.setSizePolicy(sizePolicy)
        self.expiresLabel.setText("")
        self.expiresLabel.setObjectName("expiresLabel")
        self.gridLayout.addWidget(self.expiresLabel, 13, 1, 1, 1)
        self.expiredLabel = QtWidgets.QLabel(parent=self.groupBox)
        self.expiredLabel.setObjectName("expiredLabel")
        self.gridLayout.addWidget(self.expiredLabel, 14, 0, 1, 2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 15, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 16, 0, 1, 2)
        self.label_14 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 17, 0, 1, 1)
        self.sha1Label = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sha1Label.sizePolicy().hasHeightForWidth())
        self.sha1Label.setSizePolicy(sizePolicy)
        self.sha1Label.setText("")
        self.sha1Label.setObjectName("sha1Label")
        self.gridLayout.addWidget(self.sha1Label, 17, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 18, 0, 1, 1)
        self.md5Label = QtWidgets.QLabel(parent=self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.md5Label.sizePolicy().hasHeightForWidth())
        self.md5Label.setSizePolicy(sizePolicy)
        self.md5Label.setText("")
        self.md5Label.setObjectName("md5Label")
        self.gridLayout.addWidget(self.md5Label, 18, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(EricSslCertificatesInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(EricSslCertificatesInfoWidget)

    def retranslateUi(self, EricSslCertificatesInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        self.label_17.setText(_translate("EricSslCertificatesInfoWidget", "<h2>Certificate Information</h2>"))
        self.chainLabel.setText(_translate("EricSslCertificatesInfoWidget", "Certificate Chain:"))
        self.prohibitedLabel.setText(_translate("EricSslCertificatesInfoWidget", "This certificate is on the prohibited list."))
        self.label.setText(_translate("EricSslCertificatesInfoWidget", "<b>Issued for:</b>"))
        self.label_2.setText(_translate("EricSslCertificatesInfoWidget", "Common Name (CN):"))
        self.label_3.setText(_translate("EricSslCertificatesInfoWidget", "Organization (O):"))
        self.label_4.setText(_translate("EricSslCertificatesInfoWidget", "Organizational Unit (OU):"))
        self.label_5.setText(_translate("EricSslCertificatesInfoWidget", "Serialnumber:"))
        self.label_6.setText(_translate("EricSslCertificatesInfoWidget", "<b>Issued by:</b>"))
        self.label_9.setText(_translate("EricSslCertificatesInfoWidget", "Common Name (CN):"))
        self.label_8.setText(_translate("EricSslCertificatesInfoWidget", "Organization (O):"))
        self.label_7.setText(_translate("EricSslCertificatesInfoWidget", "Organizational Unit (OU):"))
        self.label_10.setText(_translate("EricSslCertificatesInfoWidget", "<b>Validity:</b>"))
        self.label_11.setText(_translate("EricSslCertificatesInfoWidget", "Issued on:"))
        self.label_12.setText(_translate("EricSslCertificatesInfoWidget", "Expires on:"))
        self.expiredLabel.setText(_translate("EricSslCertificatesInfoWidget", "This certificate is not valid yet or has expired."))
        self.label_13.setText(_translate("EricSslCertificatesInfoWidget", "<b>Fingerprints:</b>"))
        self.label_14.setText(_translate("EricSslCertificatesInfoWidget", "SHA1-Fingerprint:"))
        self.label_15.setText(_translate("EricSslCertificatesInfoWidget", "MD5-Fingerprint:"))
