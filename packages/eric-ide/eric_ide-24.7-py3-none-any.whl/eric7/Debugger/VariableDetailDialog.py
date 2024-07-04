# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2024 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the variable detail dialog.
"""

from PyQt6.QtWidgets import QDialog

from .Ui_VariableDetailDialog import Ui_VariableDetailDialog


class VariableDetailDialog(QDialog, Ui_VariableDetailDialog):
    """
    Class implementing the variable detail dialog.

    This dialog shows the name, the type and the value of a variable
    in a read only dialog. It is opened upon a double click in the
    variables viewer widget.
    """

    def __init__(self, var, vtype, value):
        """
        Constructor

        @param var the variables name
        @type str
        @param vtype the variables type
        @type str
        @param value the variables value
        @type str
        """
        super().__init__()
        self.setupUi(self)

        # set the different fields
        self.eName.setText(var)
        self.eType.setText(vtype)
        self.eValue.setPlainText(value)
