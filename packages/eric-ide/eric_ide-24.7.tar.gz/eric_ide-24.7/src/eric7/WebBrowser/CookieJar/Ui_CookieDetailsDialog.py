# Form implementation generated from reading ui file 'src/eric7/WebBrowser/CookieJar/CookieDetailsDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_CookieDetailsDialog(object):
    def setupUi(self, CookieDetailsDialog):
        CookieDetailsDialog.setObjectName("CookieDetailsDialog")
        CookieDetailsDialog.resize(400, 300)
        CookieDetailsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CookieDetailsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.domainEdit = QtWidgets.QLineEdit(parent=CookieDetailsDialog)
        self.domainEdit.setReadOnly(True)
        self.domainEdit.setObjectName("domainEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.domainEdit)
        self.label_2 = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.nameEdit = QtWidgets.QLineEdit(parent=CookieDetailsDialog)
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.nameEdit)
        self.label_3 = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.pathEdit = QtWidgets.QLineEdit(parent=CookieDetailsDialog)
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setObjectName("pathEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.pathEdit)
        self.label_6 = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.secureCheckBox = QtWidgets.QCheckBox(parent=CookieDetailsDialog)
        self.secureCheckBox.setText("")
        self.secureCheckBox.setCheckable(False)
        self.secureCheckBox.setObjectName("secureCheckBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.secureCheckBox)
        self.label_4 = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.expirationEdit = QtWidgets.QLineEdit(parent=CookieDetailsDialog)
        self.expirationEdit.setReadOnly(True)
        self.expirationEdit.setObjectName("expirationEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.expirationEdit)
        self.label_5 = QtWidgets.QLabel(parent=CookieDetailsDialog)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.valueEdit = QtWidgets.QPlainTextEdit(parent=CookieDetailsDialog)
        self.valueEdit.setReadOnly(True)
        self.valueEdit.setObjectName("valueEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.valueEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=CookieDetailsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CookieDetailsDialog)
        self.buttonBox.accepted.connect(CookieDetailsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(CookieDetailsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(CookieDetailsDialog)
        CookieDetailsDialog.setTabOrder(self.domainEdit, self.nameEdit)
        CookieDetailsDialog.setTabOrder(self.nameEdit, self.pathEdit)
        CookieDetailsDialog.setTabOrder(self.pathEdit, self.secureCheckBox)
        CookieDetailsDialog.setTabOrder(self.secureCheckBox, self.expirationEdit)
        CookieDetailsDialog.setTabOrder(self.expirationEdit, self.valueEdit)
        CookieDetailsDialog.setTabOrder(self.valueEdit, self.buttonBox)

    def retranslateUi(self, CookieDetailsDialog):
        _translate = QtCore.QCoreApplication.translate
        CookieDetailsDialog.setWindowTitle(_translate("CookieDetailsDialog", "Cookie Details"))
        self.label.setText(_translate("CookieDetailsDialog", "Domain:"))
        self.label_2.setText(_translate("CookieDetailsDialog", "Name:"))
        self.label_3.setText(_translate("CookieDetailsDialog", "Path:"))
        self.label_6.setText(_translate("CookieDetailsDialog", "Secure:"))
        self.label_4.setText(_translate("CookieDetailsDialog", "Expires:"))
        self.label_5.setText(_translate("CookieDetailsDialog", "Contents:"))
