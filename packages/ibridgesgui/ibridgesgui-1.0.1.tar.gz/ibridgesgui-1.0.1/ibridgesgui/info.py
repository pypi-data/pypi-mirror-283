"""Provide the GUI with iRODS information."""

import sys

import PyQt6
import PyQt6.QtWidgets
import PyQt6.uic
from ibridges.resources import Resources

from ibridgesgui.config import CONFIG_DIR
from ibridgesgui.gui_utils import UI_FILE_DIR, populate_table, populate_textfield
from ibridgesgui.ui_files.tabInfo import Ui_tabInfo


class Info(PyQt6.QtWidgets.QWidget, Ui_tabInfo):
    """Set iRODS information in the GUI."""

    def __init__(self, session):
        """Initialise the tab."""
        super().__init__()
        if getattr(sys, "frozen", False):
            super().setupUi(self)
        else:
            PyQt6.uic.loadUi(UI_FILE_DIR / "tabInfo.ui", self)
        self.session = session

        self.refresh_button.clicked.connect(self.refresh_info)
        self.refresh_info()

    def refresh_info(self):
        """Find and set the information of the connected iRODS system."""
        self.resc_table.setRowCount(0)
        self.setCursor(PyQt6.QtGui.QCursor(PyQt6.QtCore.Qt.CursorShape.WaitCursor))
        # irods Zone
        self.zone_label.setText(self.session.zone)
        # irods user
        self.user_label.setText(self.session.username)
        # irods user type and groups
        user_type, user_groups = self.session.get_user_info()
        self.type_label.setText(user_type)
        populate_textfield(self.groups_browser, user_groups)
        # ibridges log location
        self.log_label.setText(str(CONFIG_DIR))
        # default resource
        self.resc_label.setText(self.session.default_resc)
        # irods server and version
        self.server_label.setText(self.session.host)
        self.version_label.setText(".".join((str(num) for num in self.session.server_version)))
        # irods resources
        resc_info = Resources(self.session).root_resources
        populate_table(self.resc_table, len(resc_info[0]), resc_info)
        self.resc_table.resizeColumnsToContents()
        self.setCursor(PyQt6.QtGui.QCursor(PyQt6.QtCore.Qt.CursorShape.ArrowCursor))
