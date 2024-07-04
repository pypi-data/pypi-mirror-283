# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to preview refactoring changes.
"""

from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from eric7.UI.DiffHighlighter import DiffHighlighter

from .Ui_RefactoringPreviewDialog import Ui_RefactoringPreviewDialog


class RefactoringPreviewDialog(QDialog, Ui_RefactoringPreviewDialog):
    """
    Class implementing a dialog to preview refactoring changes.
    """

    def __init__(self, title, diff, parent=None):
        """
        Constructor

        @param title title string to be shown above the diff
        @type str
        @param diff changes to be shown (unified diff)
        @type str
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)

        self.buttonBox.addButton(
            self.tr("&Apply Changes"), QDialogButtonBox.ButtonRole.AcceptRole
        )

        self.highlighter = DiffHighlighter(self.previewEdit.document())

        self.titleLabel.setText(title)
        self.previewEdit.setPlainText(diff)
