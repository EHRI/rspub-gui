#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style
from rspub.core.rs_enum import SelectMode


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
        self.reset_paras()

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
        self.grp_simple.toggled.connect(self.on_grp_simple_toggle)
        self.lbl_simple = QLabel(_("Location"))
        self.edt_simple = QLineEdit()
        self.edt_simple.editingFinished.connect(self.on_edt_simple_finished)
        self.btn_simple_brws = QPushButton(_("Browse"))
        self.btn_simple_brws.clicked.connect(self.on_btn_simple_brws_clicked)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lbl_simple)
        hbox2.addWidget(self.edt_simple)
        hbox2.addWidget(self.btn_simple_brws)
        self.grp_simple.setLayout(hbox2)
        vbl_0.addWidget(self.grp_simple)

        self.grp_selector = QGroupBox(_("Advanced: Create a selector"))
        self.grp_selector.setCheckable(True)
        self.grp_selector.toggled.connect(self.on_grp_selector_toggle)
        grid = QGridLayout()
        self.lbl_includes = QLabel(_("Includes"))
        self.lbl_includes.setAlignment(Qt.AlignTop)
        self.txt_includes = QTextEdit()
        self.btn_incl_brws = QPushButton(_("Browse"))
        self.btn_incl_brws.clicked.connect(self.on_btn_incl_brws_clicked)
        self.btn_incl_imp = QPushButton(_("Import"))
        grid.addWidget(self.lbl_includes, 1, 1)
        grid.addWidget(self.txt_includes, 1, 2)
        vbox_inc = QVBoxLayout()
        vbox_inc.addWidget(self.btn_incl_brws)
        vbox_inc.addWidget(self.btn_incl_imp)
        vbox_inc.addStretch(1)
        grid.addLayout(vbox_inc, 1, 3)

        self.lbl_excludes = QLabel(_("Excludes"))
        self.lbl_excludes.setAlignment(Qt.AlignTop)
        self.txt_excludes = QTextEdit()
        self.btn_excl_brws = QPushButton(_("Browse"))
        self.btn_excl_brws.clicked.connect(self.on_btn_excl_brws_clicked)
        self.btn_excl_imp = QPushButton(_("Import"))
        grid.addWidget(self.lbl_excludes, 2, 1)
        grid.addWidget(self.txt_excludes, 2, 2)
        vbox_exc = QVBoxLayout()
        vbox_exc.addWidget(self.btn_excl_brws)
        vbox_exc.addWidget(self.btn_excl_imp)
        vbox_exc.addStretch(1)
        grid.addLayout(vbox_exc, 2, 3)

        self.lbl_saved_as = QLabel(_("Saved as"))
        self.lbl_selector_file = QLabel()
        grid.addWidget(self.lbl_saved_as, 3, 1)
        grid.addWidget(self.lbl_selector_file, 3, 2, 1, 2)

        self.btn_import = QPushButton(_("Import"))
        self.btn_export = QPushButton(_("Export"))
        self.btn_relativize = QPushButton(_("Relativize"))
        self.btn_play_selected = QPushButton(_("Play"))
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn_import)
        hbox3.addWidget(self.btn_export)
        hbox3.addWidget(self.btn_relativize)
        hbox3.addWidget(self.btn_play_selected)
        grid.addLayout(hbox3, 4, 1, 1, 3)

        self.grp_selector.setLayout(grid)
        vbl_0.addWidget(self.grp_selector)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def retranslate_ui(self, code=None):
        self.label_title.setText(_("Select resources"))
        self.grp_simple.setTitle(_("Simpel selection: One file or directory"))
        self.lbl_simple.setText(_("Location"))
        self.btn_simple_brws.setText(_("Browse"))
        self.grp_selector.setTitle(_("Advanced: Create a selector"))
        self.lbl_includes.setText(_("Includes"))
        self.btn_incl_brws.setText(_("Browse"))
        self.btn_incl_imp.setText(_("Import"))
        self.lbl_excludes.setText(_("Excludes"))
        self.btn_excl_brws.setText(_("Browse"))
        self.btn_excl_imp.setText(_("Import"))
        self.lbl_saved_as.setText(_("Saved as"))
        self.btn_import.setText(_("Import"))
        self.btn_export.setText(_("Export"))
        self.btn_relativize.setText(_("Relativize"))
        self.btn_play_selected.setText(_("Play"))

    def reset_paras(self, name=None):
        self.paras = self.ctrl.paras
        self.grp_simple.setChecked(self.paras.select_mode == SelectMode.simple)
        self.grp_selector.setChecked(self.paras.select_mode == SelectMode.selector)
        self.edt_simple.setText(self.paras.simple_select_file)
        self.lbl_selector_file.setText(self.paras.selector_file)
        self.lbl_saved_as.setVisible(self.lbl_selector_file.text() != "")
        self.selector = self.ctrl.get_selector()
        self.txt_includes.setPlainText("\n".join(self.selector.get_included_entries()))
        self.txt_excludes.setPlainText("\n".join(self.selector.get_excluded_entries()))


    def on_tab_switch(self, index):
        pass

    def on_grp_simple_toggle(self, on):
        self.grp_selector.setChecked(not on)
        if on:
            self.paras.select_mode = SelectMode.simple
            self.paras.save_configuration()

    def on_grp_selector_toggle(self, on):
        self.grp_simple.setChecked(not on)
        if on:
            self.paras.select_mode = SelectMode.selector
            self.paras.save_configuration()

    def on_btn_simple_brws_clicked(self):
        self.edt_simple.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.edt_simple.text())
        result = dlg.exec()
        if result > 0:
            filename = dlg.selectedFiles()[0]
            self.edt_simple.setText(filename)

    def on_edt_simple_finished(self):
        self.paras.simple_select_file = self.edt_simple.text()
        self.paras.save_configuration()

    def on_btn_incl_brws_clicked(self):
        self.txt_includes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.AnyFile)
        result = dlg.exec()
        if result > 0:
            self.selector.include(dlg.selectedFiles())
            self.txt_includes.setPlainText("\n".join(self.selector.get_included_entries()))

    def on_btn_excl_brws_clicked(self):
        pass

    def on_btn_incl_relativize_clicked(self):
        pass
