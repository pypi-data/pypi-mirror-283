# Form implementation generated from reading ui file 'src/eric7/MicroPython/IgnoredDevicesDialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_IgnoredDevicesDialog(object):
    def setupUi(self, IgnoredDevicesDialog):
        IgnoredDevicesDialog.setObjectName("IgnoredDevicesDialog")
        IgnoredDevicesDialog.resize(500, 350)
        IgnoredDevicesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(IgnoredDevicesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.devicesEditWidget = EricStringListEditWidget(parent=IgnoredDevicesDialog)
        self.devicesEditWidget.setObjectName("devicesEditWidget")
        self.verticalLayout.addWidget(self.devicesEditWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=IgnoredDevicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(IgnoredDevicesDialog)
        self.buttonBox.accepted.connect(IgnoredDevicesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(IgnoredDevicesDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(IgnoredDevicesDialog)

    def retranslateUi(self, IgnoredDevicesDialog):
        _translate = QtCore.QCoreApplication.translate
        IgnoredDevicesDialog.setWindowTitle(_translate("IgnoredDevicesDialog", "Ignored Serial Devices"))
from eric7.EricWidgets.EricStringListEditWidget import EricStringListEditWidget
