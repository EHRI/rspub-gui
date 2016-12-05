#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style

LOG = logging.getLogger(__name__)


class InspectFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.paras = self.ctrl.paras
        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(2)
        grid.setHorizontalSpacing(2)

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
        #
        ordinal = 3
        self.widgets = []
        for tup in self.paras.describe():
            para_name = QLabel(self)
            para_value = QLabel(self)
            para_name.setContentsMargins(5, 1, 5, 1)
            para_value.setContentsMargins(5, 1, 5, 1)
            para_name.setTextInteractionFlags(Qt.TextSelectableByMouse)
            para_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
            # special colors for parameters and derived values
            if tup[0]:
                para_name.setStyleSheet(Style.parameter())
                para_value.setStyleSheet(Style.parameter())
            else:
                para_name.setStyleSheet(Style.derived())
                para_value.setStyleSheet(Style.derived())
            # Make urls clickable
            if isinstance(tup[2], str) and tup[2].startswith("http"):
                para_value.linkActivated.connect(self.on_link_activated)
            self.widgets.append([para_name, para_value])
            grid.addWidget(para_name, ordinal, 1)
            grid.addWidget(para_value, ordinal, 2)
            ordinal += 1
        #
        hbox = QHBoxLayout()
        hbox.addLayout(grid)
        hbox.addStretch(1)
        vbl_0.addLayout(hbox)
        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Inspect configuration: '%s'") % self.paras.configuration_name())
        self.render()

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.label_title.setText(_("Inspect configuration: '%s'") % self.paras.configuration_name())
        self.render()

    def render(self):
        t = 0
        for tup in self.paras.describe():
            wline = self.widgets[t]
            para_name = wline[0]
            para_value = wline[1]
            para_name.setText(_(tup[1] + "_label"))
            value = str(tup[2])
            if value == "":
                value = "None"
            if value.startswith("http"):
                para_value.setText("<a href=\"" + value + "\">" + value + "</a>")
            else:
                para_value.setText(_(value))
            t += 1

    def on_link_activated(self, link):
        QDesktopServices.openUrl(QUrl(link))

    def on_switch_tab(self, from_index, to_index):
        if to_index == self.index:
            self.render()

    def translatables(self):
        names = [
            _("configuration_name_label"),
            _("resource_dir_label"),
            _("metadata_dir_label"),
            _("abs_metadata_dir_label"),
            _("description_dir_label"),
            _("abs_description_path_label"),
            _("url_prefix_label"),
            _("has_wellknown_at_root_label"),
            _("description_url_label"),
            _("capabilitylist_url_label"),
            _("strategy_label"),
            _("selector_file_label"),
            _("simple_select_file_label"),
            _("select_mode_label"),
            _("plugin_dir_label"),
            _("max_items_in_list_label"),
            _("zero_fill_filename_label"),
            _("example_filename_label"),
            _("is_saving_pretty_xml_label"),
            _("is_saving_sitemaps_label"),
            _("last_execution_label")
        ]

        values = [
            _("Strategy.resourcelist"),
            _("Strategy.new_changelist"),
            _("Strategy.inc_changelist"),
            _("True"),
            _("False"),
            _("None"),
            _("SelectMode.simple"),
            _("SelectMode.selector")
        ]
