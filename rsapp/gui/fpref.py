#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QComboBox, qApp
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui import utils

LOG = logging.getLogger(__name__)


class PreferencesFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.language_choice = QLabel(_("Interface Language"), self)
        self.init_ui()

    def init_ui(self):
        vert = QVBoxLayout(self)

        grid1 = QGridLayout()
        grid1.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom

        language_combo = QComboBox(self)
        for locale in utils.locales():
            language_combo.addItem(locale)
        language_combo.activated[str].connect(self.cb_language_changed)
        grid1.addWidget(self.language_choice, 3, 1)
        grid1.addWidget(language_combo, 3, 2)

        vert.addLayout(grid1)
        vert.addStretch(1)
        self.setLayout(vert)

    def cb_language_changed(self, language):
        LOG.debug(language)
        utils.set_language(language)

    def retranslate_ui(self):
        self.language_choice.setText(_("Interface Language"))



