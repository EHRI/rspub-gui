#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style

LOG = logging.getLogger(__name__)


class AuditFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl

        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.import_widget = None

        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())
        self.on_switch_configuration()

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        lbl_color = QLabel("   ", self)
        lbl_color.setStyleSheet(Style.audit_title())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_color)
        hbox1.addWidget(self.label_title, 1)
        hbox1.setContentsMargins(0, 0, 0, 5)
        vbl_0.addLayout(hbox1)
        vbl_0.insertSpacing(2, 25)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)

    def on_switch_tab(self, from_index, to_index):
        pass