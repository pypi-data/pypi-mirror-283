# -*- coding: utf-8 -*-

# Copyright (c) 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to manage server connection profiles.
"""

import copy

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QDialog, QListWidgetItem

from eric7.EricWidgets import EricMessageBox

from .EricServerConnectionDialog import EricServerConnectionDialog
from .Ui_EricServerProfilesDialog import Ui_EricServerProfilesDialog


class EricServerProfilesDialog(QDialog, Ui_EricServerProfilesDialog):
    """
    Class implementing a dialog to manage server connection profiles.
    """

    def __init__(self, profiles, parent=None):
        """
        Constructor

        @param profiles dictionary containing the server connection profiles
        @type dict
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)

        self.__profiles = copy.deepcopy(profiles)
        self.__populateProfilesList()

        self.on_connectionsList_itemSelectionChanged()

    def __populateProfilesList(self):
        """
        Private method to (re-) populate the list of server connection profiles.
        """
        self.connectionsList.clear()

        for profile in self.__profiles:
            itm = QListWidgetItem(profile, self.connectionsList)
            itm.setData(Qt.ItemDataRole.UserRole, self.__profiles[profile])

    def __getProfilesList(self):
        """
        Private method to get the list of defined profile names.

        @return list of defined profile names
        @rtype list of str
        """
        profileNames = []
        for row in range(self.connectionsList.count()):
            itm = self.connectionsList.item(row)
            profileNames.append(itm.text())

        return profileNames

    @pyqtSlot()
    def on_connectionsList_itemSelectionChanged(self):
        """
        Private slot to handle a change of selected items.
        """
        selectedItems = self.connectionsList.selectedItems()
        self.editButton.setEnabled(len(selectedItems) == 1)
        self.removeButton.setEnabled(len(selectedItems) > 0)

    @pyqtSlot()
    def on_addButton_clicked(self):
        """
        Private slot add a new connection profile.
        """
        dlg = EricServerConnectionDialog(
            profileNames=self.__getProfilesList(), parent=self
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            profileData = dlg.getProfileData()
            itm = QListWidgetItem(profileData[0], self.connectionsList)
            itm.setData(Qt.ItemDataRole.UserRole, profileData[1:])

    @pyqtSlot()
    def on_editButton_clicked(self):
        """
        Private slot to edit the selected entry.
        """
        selectedItems = self.connectionsList.selectedItems()
        if selectedItems:
            itm = selectedItems[0]
            dlg = EricServerConnectionDialog(
                profileNames=self.__getProfilesList(), parent=self
            )
            data = itm.data(Qt.ItemDataRole.UserRole)
            dlg.setProfileData(itm.text(), *data)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                profileData = dlg.getProfileData()
                itm.setText(profileData[0])
                itm.setData(Qt.ItemDataRole.UserRole, profileData[1:])

    @pyqtSlot()
    def on_removeButton_clicked(self):
        """
        Private slot to remove the selected connection profiles.
        """
        yes = EricMessageBox.yesNo(
            self,
            self.tr("Remove Selected Entries"),
            self.tr("Do you really want to remove the selected entries from the list?"),
        )
        if yes:
            for itm in self.connectionsList.selectedItems()[:]:
                self.connectionsList.takeItem(self.connectionsList.row(itm))
                del itm

    @pyqtSlot()
    def on_resetButton_clicked(self):
        """
        Private slot to reset all changes performed.
        """
        yes = EricMessageBox.yesNo(
            self,
            self.tr("Reset Changes"),
            self.tr(
                "Do you really want to reset all changes performed up to this point?"
            ),
        )
        if yes:
            self.__populateProfilesList()

    def getConnectionProfiles(self):
        """
        Public method to get the configured connection profiles.

        @return dictionary containing the configured connection profiles
        @rtype dict
        """
        profiles = {}

        for row in range(self.connectionsList.count()):
            itm = self.connectionsList.item(row)
            profiles[itm.text()] = itm.data(Qt.ItemDataRole.UserRole)

        return profiles
