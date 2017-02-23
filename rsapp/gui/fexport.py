#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.fconfigure import ParaLine, ConfigureFrame
from rsapp.gui.style import Style

LOG = logging.getLogger(__name__)


class ExportFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl

        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())
        self.on_switch_configuration()

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        grid1 = QGridLayout()
        grid1.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid1.setVerticalSpacing(2)
        grid1.setHorizontalSpacing(2)

        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label_title, 1)
        hbox1.setContentsMargins(0, 0, 0, 5)
        grid1.addLayout(hbox1, 1, 1, 1, 3)

        self.lbl_metadata_key = QLabel(self)
        self.lbl_metadata_value = QLabel(self)
        self.lbl_metadata_key.setContentsMargins(5, 1, 5, 1)
        self.lbl_metadata_value.setContentsMargins(5, 1, 5, 1)
        self.lbl_metadata_key.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_metadata_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_metadata_key.setStyleSheet(Style.derived())
        self.lbl_metadata_value.setStyleSheet(Style.derived())
        grid1.addWidget(self.lbl_metadata_key, 2, 1)
        grid1.addWidget(self.lbl_metadata_value, 2, 2)

        self.lbl_last_execution_key = QLabel(self)
        self.lbl_last_execution_value = QLabel(self)
        self.lbl_last_execution_key.setContentsMargins(5, 1, 5, 1)
        self.lbl_last_execution_value.setContentsMargins(5, 1, 5, 1)
        self.lbl_last_execution_key.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_last_execution_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_last_execution_key.setStyleSheet(Style.derived())
        self.lbl_last_execution_value.setStyleSheet(Style.derived())
        grid1.addWidget(self.lbl_last_execution_key, 3, 1)
        grid1.addWidget(self.lbl_last_execution_value, 3, 2)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(grid1)
        hbox2.addStretch(1)
        vbl_0.addLayout(hbox2)
        vbl_0.insertSpacing(2, 25)

        # Group boxes
        str_conv = (ConfigureFrame.str2tx, ConfigureFrame.tx2str)
        int_conv = (ConfigureFrame.int2tx, ConfigureFrame.tx2int)

        # # scp group
        grid2 = QGridLayout()
        grid2.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid2.setVerticalSpacing(5)
        grid2.setHorizontalSpacing(10)

        self.grp_scp = QGroupBox(_("Transfer files with Secure Copy Protocol (scp)"))
        vbox3 = QVBoxLayout()

        self.para_scp_widgets = {
            "scp_server": ParaLine(self, "scp_server", str_conv, grid2, 3, False),
            "scp_port": ParaLine(self, "scp_port", int_conv, grid2, 5, False, width=100),
            "scp_user": ParaLine(self, "scp_user", str_conv, grid2, 7, False),
            "scp_document_root": ParaLine(self, "scp_document_root", str_conv, grid2, 9, False),
            "scp_document_path": ParaLine(self, "scp_document_path", str_conv, grid2, 11, False)
        }

        self.grp_scp.setLayout(vbox3)
        vbox3.addLayout(grid2)

        hbox_scp = QHBoxLayout()
        hbox_scp.addStretch(1)
        self.scp_radio_all = QRadioButton(_("Export all resources"))
        self.scp_radio_all.setChecked(False)
        self.scp_radio_latest = QRadioButton(_("Export latest changes"))
        self.scp_radio_latest.setChecked(True)
        hbox_scp.addWidget(self.scp_radio_all)
        hbox_scp.addWidget(self.scp_radio_latest)
        self.scp_button_start = QPushButton(_("Start"))
        hbox_scp.addWidget(self.scp_button_start)
        vbox3.addLayout(hbox_scp)

        vbl_0.addWidget(self.grp_scp)
        vbl_0.insertSpacing(4, 15)

        # # zip group
        grid3 = QGridLayout()
        grid3.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid3.setVerticalSpacing(5)
        grid3.setHorizontalSpacing(10)

        self.grp_zip = QGroupBox(_("Create a .zip file"))
        vbox4 = QVBoxLayout()

        self.para_zip_widgets = {
            "zip_filename": ParaLine(self, "zip_filename", str_conv, grid3, 3, browse="SaveFileName")
        }

        self.grp_zip.setLayout(vbox4)
        vbox4.addLayout(grid3)

        hbox_zip = QHBoxLayout()
        hbox_zip.addStretch(1)
        self.zip_radio_all = QRadioButton(_("Zip all resources"))
        self.zip_radio_all.setChecked(False)
        self.zip_radio_latest = QRadioButton(_("Zip latest changes"))
        self.zip_radio_latest.setChecked(True)
        hbox_zip.addWidget(self.zip_radio_all)
        hbox_zip.addWidget(self.zip_radio_latest)
        self.zip_button_start = QPushButton(_("Start"))
        hbox_zip.addWidget(self.zip_button_start)
        vbox4.addLayout(hbox_zip)

        vbl_0.addWidget(self.grp_zip)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Export: '%s'") % self.ctrl.paras.configuration_name())
        self.lbl_metadata_key.setText(_("Export based on"))
        self.lbl_last_execution_key.setText(_("last_execution_label"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.label_title.setText(_("Export: '%s'") % self.ctrl.paras.configuration_name())
        self.lbl_metadata_value.setText(self.ctrl.paras.abs_metadata_dir())
        value = self.ctrl.paras.last_execution
        if value is None:
            value = "None"
        self.lbl_last_execution_value.setText(_(value))

    def on_switch_tab(self, from_index, to_index):
        if to_index == self.index:
            self.on_switch_configuration()

    def translatables(self):
        # parameter labels
        _("scp_server_label")
        _("scp_port_label")
        _("scp_user_label")
        _("scp_document_root_label")
        _("scp_document_path_label")
        _("zip_filename_label")
