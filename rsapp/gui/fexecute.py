#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame


class ExecuteFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.retranslate_ui)

    @pyqtSlot(str)
    def retranslate_ui(self, code=None):
        pass