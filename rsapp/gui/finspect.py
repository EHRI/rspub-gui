#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame


class InspectFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.retranslate_ui)
        self.ctrl.switch_configuration.connect(self.reset_paras)
        self.paras = self.ctrl.paras
        self.init_ui()
        self.retranslate_ui()

    def init_ui(self):
        pass

    def retranslate_ui(self, code=None):
        pass

    def reset_paras(self, name=None):
        pass