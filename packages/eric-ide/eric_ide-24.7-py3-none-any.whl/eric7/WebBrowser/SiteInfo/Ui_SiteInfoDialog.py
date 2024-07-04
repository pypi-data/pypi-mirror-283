# Form implementation generated from reading ui file 'src/eric7/WebBrowser/SiteInfo/SiteInfoDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SiteInfoDialog(object):
    def setupUi(self, SiteInfoDialog):
        SiteInfoDialog.setObjectName("SiteInfoDialog")
        SiteInfoDialog.resize(700, 550)
        SiteInfoDialog.setSizeGripEnabled(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SiteInfoDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.heading = QtWidgets.QLabel(parent=SiteInfoDialog)
        self.heading.setText("")
        self.heading.setWordWrap(True)
        self.heading.setObjectName("heading")
        self.verticalLayout_2.addWidget(self.heading)
        self.tabWidget = QtWidgets.QTabWidget(parent=SiteInfoDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.generalTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.generalTab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.siteAddressLabel = QtWidgets.QLabel(parent=self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.siteAddressLabel.sizePolicy().hasHeightForWidth())
        self.siteAddressLabel.setSizePolicy(sizePolicy)
        self.siteAddressLabel.setObjectName("siteAddressLabel")
        self.gridLayout.addWidget(self.siteAddressLabel, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.generalTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.encodingLabel = QtWidgets.QLabel(parent=self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.encodingLabel.sizePolicy().hasHeightForWidth())
        self.encodingLabel.setSizePolicy(sizePolicy)
        self.encodingLabel.setObjectName("encodingLabel")
        self.gridLayout.addWidget(self.encodingLabel, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_9 = QtWidgets.QLabel(parent=self.generalTab)
        self.label_9.setObjectName("label_9")
        self.verticalLayout.addWidget(self.label_9)
        self.tagsTree = QtWidgets.QTreeWidget(parent=self.generalTab)
        self.tagsTree.setAlternatingRowColors(True)
        self.tagsTree.setRootIsDecorated(False)
        self.tagsTree.setItemsExpandable(False)
        self.tagsTree.setWordWrap(False)
        self.tagsTree.setObjectName("tagsTree")
        self.verticalLayout.addWidget(self.tagsTree)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 3, 1, 1)
        self.securityIconLabel = QtWidgets.QLabel(parent=self.generalTab)
        self.securityIconLabel.setObjectName("securityIconLabel")
        self.gridLayout_2.addWidget(self.securityIconLabel, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 4)
        self.securityLabel = QtWidgets.QLabel(parent=self.generalTab)
        self.securityLabel.setText("")
        self.securityLabel.setObjectName("securityLabel")
        self.gridLayout_2.addWidget(self.securityLabel, 1, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.securityDetailsButton = QtWidgets.QPushButton(parent=self.generalTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.securityDetailsButton.sizePolicy().hasHeightForWidth())
        self.securityDetailsButton.setSizePolicy(sizePolicy)
        self.securityDetailsButton.setAutoDefault(False)
        self.securityDetailsButton.setObjectName("securityDetailsButton")
        self.gridLayout_2.addWidget(self.securityDetailsButton, 1, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.tabWidget.addTab(self.generalTab, "")
        self.mediaTab = QtWidgets.QWidget()
        self.mediaTab.setObjectName("mediaTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.mediaTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.imagesTree = QtWidgets.QTreeWidget(parent=self.mediaTab)
        self.imagesTree.setAlternatingRowColors(True)
        self.imagesTree.setRootIsDecorated(False)
        self.imagesTree.setItemsExpandable(False)
        self.imagesTree.setObjectName("imagesTree")
        self.verticalLayout_4.addWidget(self.imagesTree)
        self.label_5 = QtWidgets.QLabel(parent=self.mediaTab)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.imagePreview = QtWidgets.QGraphicsView(parent=self.mediaTab)
        self.imagePreview.setObjectName("imagePreview")
        self.verticalLayout_4.addWidget(self.imagePreview)
        self.tabWidget.addTab(self.mediaTab, "")
        self.securityTab = QtWidgets.QWidget()
        self.securityTab.setObjectName("securityTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.securityTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sslWidget = EricSslCertificatesInfoWidget(parent=self.securityTab)
        self.sslWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.sslWidget.setObjectName("sslWidget")
        self.verticalLayout_3.addWidget(self.sslWidget)
        self.tabWidget.addTab(self.securityTab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SiteInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SiteInfoDialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(SiteInfoDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SiteInfoDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SiteInfoDialog)
        SiteInfoDialog.setTabOrder(self.tabWidget, self.tagsTree)
        SiteInfoDialog.setTabOrder(self.tagsTree, self.securityDetailsButton)
        SiteInfoDialog.setTabOrder(self.securityDetailsButton, self.imagesTree)
        SiteInfoDialog.setTabOrder(self.imagesTree, self.imagePreview)
        SiteInfoDialog.setTabOrder(self.imagePreview, self.sslWidget)

    def retranslateUi(self, SiteInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        SiteInfoDialog.setWindowTitle(_translate("SiteInfoDialog", "Site Information"))
        self.label.setText(_translate("SiteInfoDialog", "Site Address:"))
        self.label_2.setText(_translate("SiteInfoDialog", "Encoding:"))
        self.label_9.setText(_translate("SiteInfoDialog", "Meta tags of site:"))
        self.tagsTree.headerItem().setText(0, _translate("SiteInfoDialog", "Tag"))
        self.tagsTree.headerItem().setText(1, _translate("SiteInfoDialog", "Value"))
        self.label_4.setText(_translate("SiteInfoDialog", "<b>Security information</b>"))
        self.securityDetailsButton.setText(_translate("SiteInfoDialog", "Details"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("SiteInfoDialog", "General"))
        self.imagesTree.headerItem().setText(0, _translate("SiteInfoDialog", "Image"))
        self.imagesTree.headerItem().setText(1, _translate("SiteInfoDialog", "Image Address"))
        self.label_5.setText(_translate("SiteInfoDialog", "<b>Preview</b>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mediaTab), _translate("SiteInfoDialog", "Media"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.securityTab), _translate("SiteInfoDialog", "Security"))
from eric7.EricNetwork.EricSslCertificatesInfoWidget import EricSslCertificatesInfoWidget
