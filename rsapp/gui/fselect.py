#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style


class SelectFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.retranslate_ui)
        self.ctrl.switch_configuration.connect(self.reset_paras)
        self.ctrl.switch_tab.connect(self.on_tab_switch)
        self.paras = self.ctrl.paras
        self.init_ui()
        self.retranslate_ui()

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        self.label_title = QLabel(_("Select resources"), self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_title, 1)
        hbox.setContentsMargins(0, 0, 0, 5)   # left, top, right, bottom
        vbl_0.addLayout(hbox)

        self.grp_simple = QGroupBox(_("Simpel selection: One file or directory"))
        self.grp_simple.setCheckable(True)
        self.lbl_simple = QLabel(_("Location"))
        self.edt_simple = QLineEdit()
        self.btn_simple = QPushButton(_("Browse"))
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lbl_simple)
        hbox2.addWidget(self.edt_simple)
        hbox2.addWidget(self.btn_simple)
        self.grp_simple.setLayout(hbox2)
        vbl_0.addWidget(self.grp_simple)

        self.grp_selector = QGroupBox(_("Advanced: Create a selector"))
        self.grp_selector.setCheckable(True)
        self.grp_selector.setChecked(False)
        grid = QGridLayout()
        self.lbl_includes = QLabel(_("Includes"))
        self.lbl_includes.setAlignment(Qt.AlignTop)
        self.txt_includes = QTextEdit()
        self.btn_includes = QPushButton(_("Browse"))
        self.btn_incl_imp = QPushButton(_("Import"))
        grid.addWidget(self.lbl_includes, 1, 1)
        grid.addWidget(self.txt_includes, 1, 2)
        vbox_inc = QVBoxLayout()
        vbox_inc.addWidget(self.btn_includes)
        vbox_inc.addWidget(self.btn_incl_imp)
        vbox_inc.addStretch(1)
        grid.addLayout(vbox_inc, 1, 3)

        self.lbl_excludes = QLabel(_("Excludes"))
        self.lbl_excludes.setAlignment(Qt.AlignTop)
        self.txt_excludes = QTextEdit()
        self.btn_excludes = QPushButton(_("Browse"))
        self.btn_excl_imp = QPushButton(_("Import"))
        grid.addWidget(self.lbl_excludes, 2, 1)
        grid.addWidget(self.txt_excludes, 2, 2)
        vbox_exc = QVBoxLayout()
        vbox_exc.addWidget(self.btn_excludes)
        vbox_exc.addWidget(self.btn_excl_imp)
        vbox_exc.addStretch(1)
        grid.addLayout(vbox_exc, 2, 3)

        self.grp_selector.setLayout(grid)
        vbl_0.addWidget(self.grp_selector)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def retranslate_ui(self, code=None):
        self.label_title.setText(_("Select resources"))

    def reset_paras(self, name=None):
        pass

    def on_tab_switch(self, index):
        pass