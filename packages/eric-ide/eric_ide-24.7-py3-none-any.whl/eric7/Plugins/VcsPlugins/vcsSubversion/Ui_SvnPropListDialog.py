# Form implementation generated from reading ui file 'src/eric7/Plugins/VcsPlugins/vcsSubversion/SvnPropListDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_SvnPropListDialog(object):
    def setupUi(self, SvnPropListDialog):
        SvnPropListDialog.setObjectName("SvnPropListDialog")
        SvnPropListDialog.resize(826, 569)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(SvnPropListDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.propsList = QtWidgets.QTreeWidget(parent=SvnPropListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.propsList.sizePolicy().hasHeightForWidth())
        self.propsList.setSizePolicy(sizePolicy)
        self.propsList.setAlternatingRowColors(True)
        self.propsList.setRootIsDecorated(False)
        self.propsList.setItemsExpandable(False)
        self.propsList.setObjectName("propsList")
        self.verticalLayout_2.addWidget(self.propsList)
        self.errorGroup = QtWidgets.QGroupBox(parent=SvnPropListDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.errorGroup.sizePolicy().hasHeightForWidth())
        self.errorGroup.setSizePolicy(sizePolicy)
        self.errorGroup.setObjectName("errorGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.errorGroup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.errors = QtWidgets.QTextEdit(parent=self.errorGroup)
        self.errors.setObjectName("errors")
        self.verticalLayout.addWidget(self.errors)
        self.verticalLayout_2.addWidget(self.errorGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=SvnPropListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SvnPropListDialog)
        QtCore.QMetaObject.connectSlotsByName(SvnPropListDialog)
        SvnPropListDialog.setTabOrder(self.propsList, self.errors)
        SvnPropListDialog.setTabOrder(self.errors, self.buttonBox)

    def retranslateUi(self, SvnPropListDialog):
        _translate = QtCore.QCoreApplication.translate
        SvnPropListDialog.setWindowTitle(_translate("SvnPropListDialog", "Subversion List Properties"))
        SvnPropListDialog.setWhatsThis(_translate("SvnPropListDialog", "<b>Subversion List Prperties</b>\n"
"<p>This dialog shows the properties of the selected file or project.</p>"))
        self.propsList.setWhatsThis(_translate("SvnPropListDialog", "<b>Properties List</b>\n"
"<p>This shows the properties of the selected file or project.</p>"))
        self.propsList.setSortingEnabled(True)
        self.propsList.headerItem().setText(0, _translate("SvnPropListDialog", "Path"))
        self.propsList.headerItem().setText(1, _translate("SvnPropListDialog", "Name"))
        self.propsList.headerItem().setText(2, _translate("SvnPropListDialog", "Value"))
        self.errorGroup.setTitle(_translate("SvnPropListDialog", "Errors"))
        self.errors.setWhatsThis(_translate("SvnPropListDialog", "<b>Subversion proplist errors</b>\n"
"<p>This shows possible error messages of the subversion proplist command.</p>"))
