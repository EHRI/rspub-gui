#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style
from rsapp.gui.widgets import ParaLine, ParaStrategyDrop, ParaCheck, ParaWidget

LOG = logging.getLogger(__name__)


class ConfigureFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)

        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_title, 1)
        hbox.setContentsMargins(0, 0, 0, 5)
        grid.addLayout(hbox, 1, 1, 1, 3)

        self.para_widgets = {
            "resource_dir": ParaLine(self, "resource_dir", ParaWidget.str_conv(), grid, 3, True),
            "metadata_dir": ParaLine(self, "metadata_dir", ParaWidget.str_conv(), grid, 5, False),
            "description_dir": ParaLine(self, "description_dir", ParaWidget.str_conv(), grid, 7, True),
            "plugin_dir": ParaLine(self, "plugin_dir", ParaWidget.str_conv(), grid, 9, True),
            "url_prefix": ParaLine(self, "url_prefix", ParaWidget.str_conv(), grid, 11, False),
            "strategy": ParaStrategyDrop(self, "strategy", grid, 15),
            "max_items_in_list": ParaLine(self, "max_items_in_list", ParaWidget.int_conv(), grid, 17, False, width=100),
            "zero_fill_filename": ParaLine(self, "zero_fill_filename", ParaWidget.int_conv(), grid, 19, False, width=100),
            "is_saving_pretty_xml": ParaCheck(self, "is_saving_pretty_xml", grid, 21),
            "is_saving_sitemaps": ParaCheck(self, "is_saving_sitemaps", grid, 22),
            "has_wellknown_at_root": ParaCheck(self, "has_wellknown_at_root", grid, 23)
        }

        self.button_reset = QPushButton(_("Reset"), self)
        self.button_reset.clicked.connect(self.on_button_reset_clicked)
        grid.addWidget(self.button_reset, 24, 3)

        vbl_0.addLayout(grid)
        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Configure parameters: '%s'") % self.paras.configuration_name())

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.label_title.setText(_("Configure parameters: '%s'") % self.paras.configuration_name())

    def on_button_reset_clicked(self):
        msg_box = QMessageBox()
        msg_box.setText(_("Reset current parameters"))
        msg_box.setInformativeText(_("Reset '%s' parameters to default values?") % self.paras.configuration_name())
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.No| QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        exe = msg_box.exec()
        if exe == QMessageBox.Yes:
            self.ctrl.reset_configuration()

    def count_errors(self):
        return len([p for p in self.para_widgets.values() if not p.is_accepted()])

    def on_about_to_change(self, window_title):
        ok_to_change = True
        error_count = self.count_errors()
        if error_count > 0:
            msg_box = QMessageBox()
            msg_box.setText(window_title)
            i_text = _("Parameters '%s' has %d error(s).") % (self.paras.configuration_name(), error_count)
            i_text += "\n\n"
            i_text += _("Ok to proceed?")
            msg_box.setInformativeText(i_text)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg_box.setDefaultButton(QMessageBox.Yes)
            exe = msg_box.exec()
            if exe == QMessageBox.No:
                ok_to_change = False
        LOG.debug("Configure ok_to_change=%s" % ok_to_change)
        return ok_to_change

    def translatables(self):
        # parameter labels
        _("resource_dir_label")
        _("metadata_dir_label")
        _("description_dir_label")
        _("plugin_dir_label")
        _("url_prefix_label")
        _("strategy_label")
        _("max_items_in_list_label")
        _("zero_fill_filename_label")
        _("is_saving_pretty_xml_label")
        _("is_saving_sitemaps_label")
        _("has_wellknown_at_root_label")






