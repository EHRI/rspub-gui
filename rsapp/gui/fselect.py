#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rsapp.gui.style import Style
from rspub.core.rs_enum import SelectMode
from rspub.core.selector import Selector

LOG = logging.getLogger(__name__)


class SelectFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_selector.connect(self.on_switch_selector)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.paras = self.ctrl.paras
        self.selector = self.ctrl.selector
        self.includes = self.selector.get_included_entries()
        self.excludes = self.selector.get_excluded_entries()
        self.init_ui()
        self.play_widget_simple = None
        self.play_widget_selector = None
        self.on_switch_language(self.ctrl.current_language())
        self.on_switch_configuration(self.ctrl.paras.configuration_name())
        self.on_switch_selector()

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

        # simple group
        self.lbl_simple = QLabel(_("Location"))
        self.edt_simple = QLineEdit()
        self.edt_simple.editingFinished.connect(self.on_edt_simple_finished)
        vbox_simple = QVBoxLayout()
        vbox_simple.setSpacing(0)
        self.btn_simple_brws = QPushButton(_("Browse"))
        self.btn_simple_brws.clicked.connect(self.on_btn_simple_brws_clicked)
        vbox_simple.addWidget(self.btn_simple_brws)
        self.btn_simple_play = QPushButton(_("Play"))
        self.btn_simple_play.clicked.connect(self.on_btn_simple_play_clicked)
        vbox_simple.addWidget(self.btn_simple_play)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lbl_simple)
        hbox2.addWidget(self.edt_simple)
        hbox2.addLayout(vbox_simple)
        self.grp_simple.setLayout(hbox2)
        vbl_0.addWidget(self.grp_simple)

        self.grp_selector = QGroupBox(_("Advanced: Create a selector"))
        self.grp_selector.setCheckable(True)
        self.grp_selector.toggled.connect(self.on_grp_selector_toggle)
        grid = QGridLayout()

        # selector group: includes
        self.lbl_includes = QLabel(_("Includes"))
        self.lbl_includes.setAlignment(Qt.AlignTop)
        self.txt_includes = QPlainTextEdit()
        self.btn_incl_brws = QPushButton(_("Browse"))
        self.btn_incl_brws.clicked.connect(self.on_btn_incl_brws_clicked)
        self.btn_incl_imp = QPushButton(_("Import"))
        self.btn_incl_imp.clicked.connect(self.on_btn_incl_import_clicked)
        grid.addWidget(self.lbl_includes, 1, 1)
        grid.addWidget(self.txt_includes, 1, 2)
        vbox_inc = QVBoxLayout()
        vbox_inc.setSpacing(0)
        vbox_inc.addWidget(self.btn_incl_brws)
        vbox_inc.addWidget(self.btn_incl_imp)
        vbox_inc.addStretch(1)
        grid.addLayout(vbox_inc, 1, 3)

        # selector group: excludes
        self.lbl_excludes = QLabel(_("Excludes"))
        self.lbl_excludes.setAlignment(Qt.AlignTop)
        self.txt_excludes = QPlainTextEdit()
        self.btn_excl_brws = QPushButton(_("Browse"))
        self.btn_excl_brws.clicked.connect(self.on_btn_excl_brws_clicked)
        self.btn_excl_imp = QPushButton(_("Import"))
        self.btn_excl_imp.clicked.connect(self.on_btn_excl_import_clicked)
        grid.addWidget(self.lbl_excludes, 2, 1)
        grid.addWidget(self.txt_excludes, 2, 2)
        vbox_exc = QVBoxLayout()
        vbox_exc.setSpacing(0)
        vbox_exc.addWidget(self.btn_excl_brws)
        vbox_exc.addWidget(self.btn_excl_imp)
        vbox_exc.addStretch(1)
        grid.addLayout(vbox_exc, 2, 3)

        # selector group: selector file
        self.lbl_saved_as = QLabel(_("Selector"))
        self.lbl_selector_file = QLabel()
        self.lbl_selector_file.setTextInteractionFlags(Qt.TextSelectableByMouse)
        grid.addWidget(self.lbl_saved_as, 3, 1)
        grid.addWidget(self.lbl_selector_file, 3, 2, 1, 2)

        # selector group: bottom buttons
        self.btn_open_selector = QPushButton(_("Open..."))
        self.btn_open_selector.clicked.connect(self.on_btn_open_selector_clicked)
        self.btn_save_selector_as = QPushButton(_("Save as..."))
        self.btn_save_selector_as.clicked.connect(self.on_btn_save_selector_as_clicked)
        self.btn_play_selected = QPushButton(_("Play"))
        self.btn_play_selected.clicked.connect(self.on_btn_play_selected_clicked)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn_open_selector)
        hbox3.addWidget(self.btn_save_selector_as)
        hbox3.addWidget(self.btn_play_selected)
        grid.addLayout(hbox3, 4, 1, 1, 3)

        self.grp_selector.setLayout(grid)
        vbl_0.addWidget(self.grp_selector)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Select resources"))
        self.grp_simple.setTitle(_("Simpel selection: One file or directory"))
        self.lbl_simple.setText(_("Location"))
        self.btn_simple_brws.setText(_("Browse"))
        self.btn_simple_play.setText(_("Play"))
        self.grp_selector.setTitle(_("Advanced: Create a selector"))
        self.lbl_includes.setText(_("Includes"))
        self.btn_incl_brws.setText(_("Browse"))
        self.btn_incl_imp.setText(_("Import"))
        self.lbl_excludes.setText(_("Excludes"))
        self.btn_excl_brws.setText(_("Browse"))
        self.btn_excl_imp.setText(_("Import"))
        self.lbl_saved_as.setText(_("Selector"))
        self.btn_open_selector.setText(_("Open..."))
        self.btn_save_selector_as.setText(_("Save as..."))
        self.btn_play_selected.setText(_("Play"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.grp_simple.setChecked(self.paras.select_mode == SelectMode.simple)
        self.grp_selector.setChecked(self.paras.select_mode == SelectMode.selector)
        self.edt_simple.setText(self.paras.simple_select_file)

    def on_switch_selector(self):
        self.selector = self.ctrl.selector
        self.includes = self.selector.get_included_entries()
        self.excludes = self.selector.get_excluded_entries()
        self.txt_includes.setPlainText("\n".join(self.includes))
        self.txt_excludes.setPlainText("\n".join(self.excludes))
        if self.selector.location:
            self.lbl_selector_file.setText(self.selector.abs_location())
        else:
            self.lbl_selector_file.setText("")
        self.lbl_saved_as.setVisible(self.lbl_selector_file.text() != "")

    def is_selector_dirty(self):
        dirty = False
        includes = {x.strip() for x in self.txt_includes.toPlainText().splitlines() if x.strip() != ""}
        if includes != self.includes:
            dirty = True
            self.selector.clear_includes()
            self.selector.include(includes)
        excludes = {x.strip() for x in self.txt_excludes.toPlainText().splitlines() if x.strip() != ""}
        if excludes != self.excludes:
            dirty = True
            self.selector.clear_excludes()
            self.selector.exclude(excludes)
        return dirty

    def store_in_selector(self):
        if self.is_selector_dirty():
            self.ctrl.save_selector()

    def on_switch_tab(self, from_index, to_index):
        if from_index == self.index:
            self.store_in_selector()

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

    # ###################################################
    def on_btn_simple_brws_clicked(self):
        self.edt_simple.setFocus()
        dlg = QFileDialog(self)
        directory = self.edt_simple.text()
        if directory == "":
            directory = self.paras.resource_dir
        dlg.setDirectory(directory)
        result = dlg.exec()
        if result > 0:
            filename = dlg.selectedFiles()[0]
            self.edt_simple.setText(filename)

    def on_edt_simple_finished(self):
        self.paras.simple_select_file = self.edt_simple.text()
        self.paras.save_configuration()

    def on_btn_simple_play_clicked(self):
        if self.play_widget_simple is None:
            self.play_widget_simple = PlayWidget(self.__get_simple_selector, _("Simpel selection: List resources"))
        else:
            self.play_widget_simple.show()
            self.play_widget_simple.setWindowState(Qt.WindowActive)
            self.play_widget_simple.activateWindow()
            self.play_widget_simple.raise_()

    def __get_simple_selector(self):
        selector = Selector()
        selector.include(self.paras.simple_select_file)
        return selector

    # ########################################################
    def on_btn_incl_brws_clicked(self):
        self.txt_includes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.AnyFile)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_includes.appendPlainText(file)
            includes = set(self.txt_includes.toPlainText().splitlines())
            self.txt_includes.setPlainText("\n".join(sorted(includes)))

    def on_btn_excl_brws_clicked(self):
        self.txt_excludes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.AnyFile)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_excludes.appendPlainText(file)
            excludes = set(self.txt_excludes.toPlainText().splitlines())
            self.txt_excludes.setPlainText("\n".join(sorted(excludes)))

    def on_btn_incl_import_clicked(self):
        filenames = QFileDialog.getOpenFileName(self, _("Import included filename"), self.ctrl.last_directory)
        if filenames[0] != "":
            self.ctrl.load_selector_includes(filenames[0])

    def on_btn_excl_import_clicked(self):
        filenames = QFileDialog.getOpenFileName(self, _("Import excluded filenames"), self.ctrl.last_directory)
        if filenames[0] != "":
            self.ctrl.load_selector_excludes(filenames[0])

    def on_btn_save_selector_as_clicked(self):
        saved = False
        self.store_in_selector()
        if self.selector.location:
            directory = self.selector.abs_location()
        else:
            directory = os.path.join(os.path.expanduser("~"), "selector.csv")
        filenames = QFileDialog.getSaveFileName(self, _("Save selector"), directory)
        if filenames[0] != "":
            self.ctrl.save_selector_as(filenames[0])
            saved = True
        return saved

    def on_btn_open_selector_clicked(self):
        if self.on_about_to_change(_("Open a new selector")):
            if self.selector.location:
                directory = os.path.dirname(self.selector.abs_location())
            else:
                directory = os.path.expanduser("~")
            filenames = QFileDialog.getOpenFileName(self, _("Open selector"), directory)
            if filenames[0] != "":
                self.ctrl.open_selector(filenames[0])

    def on_about_to_change(self, window_title):
        ok_to_change = True
        self.store_in_selector()
        if self.selector.location is None and not self.selector.is_empty():
            msg_box = QMessageBox()
            msg_box.setText(window_title)
            i_text = _("Selector has unsaved changes.")
            i_text += "\n\n"
            i_text += _("Save selector?")
            msg_box.setInformativeText(i_text)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg_box.setDefaultButton(QMessageBox.Yes)
            exe = msg_box.exec()
            if exe == QMessageBox.Yes:
                ok_to_change = self.on_btn_save_selector_as_clicked()
        return ok_to_change

    def on_btn_play_selected_clicked(self):
        self.store_in_selector()
        if self.play_widget_selector is None:
            self.play_widget_selector = PlayWidget(self.__get_advanced_selector, _("Advanced: List resources"))
        else:
            self.play_widget_selector.show()
            self.play_widget_selector.setWindowState(Qt.WindowActive)
            self.play_widget_selector.activateWindow()
            self.play_widget_selector.raise_()

    def __get_advanced_selector(self):
        return self.selector


class PlayWidget(QWidget):

    def __init__(self, get_selector, title=None, max_lines=1000000):
        QWidget.__init__(self)
        self.get_selector = get_selector
        self.setWindowTitle(title)
        self.max_lines = max_lines

        self.player = None
        self.resource_count = 0

        self.__init_ui__()
        self.show()

    def __init_ui__(self):
        vbox = QVBoxLayout()

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(self.max_lines)
        self.output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.output.setCenterOnScroll(True)
        vbox.addWidget(self.output)

        btn_box = QHBoxLayout()
        lbl_recources_count = QLabel(_("Count resources:"))
        btn_box.addWidget(lbl_recources_count)
        self.lbl_resources_counter = QLabel("0")
        btn_box.addWidget(self.lbl_resources_counter)
        btn_box.addStretch(1)

        self.btn_play = QPushButton(_("Play"))
        self.btn_play.clicked.connect(self.on_btn_play_clicked)
        btn_box.addWidget(self.btn_play)

        self.btn_stop = QPushButton(_("Stop"))
        self.normal_style = self.btn_stop.styleSheet()
        self.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        self.btn_stop.setEnabled(False)
        btn_box.addWidget(self.btn_stop)

        self.btn_close = QPushButton(_("Close"))
        self.btn_close.clicked.connect(self.on_btn_close_clicked)
        btn_box.addWidget(self.btn_close)

        vbox.addLayout(btn_box)
        self.setLayout(vbox)
        #self.setFixedSize(800, 250)
        self.resize(800, 250)

    def on_btn_play_clicked(self):
        self.output.setPlainText("")
        selector = self.get_selector()
        self.player = PlayerThread(selector, self)
        self.player.yield_resource.connect(self.on_yield_resource)
        self.player.finished.connect(self.on_player_finished)
        self.resource_count = 0

        self.btn_close.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_stop.setStyleSheet(Style.alarm())
        self.player.start()

    def on_yield_resource(self, file):
        self.resource_count += 1
        self.lbl_resources_counter.setText(str(self.resource_count))
        self.output.appendPlainText(file)
        self.update()

    def on_btn_stop_clicked(self):
        self.btn_stop.setStyleSheet(self.normal_style)
        self.btn_stop.setEnabled(False)
        self.player.requestInterruption()

    def on_player_finished(self):
        self.btn_stop.setStyleSheet(self.normal_style)
        self.btn_stop.setEnabled(False)
        self.btn_play.setEnabled(True)
        self.btn_close.setEnabled(True)

    def on_btn_close_clicked(self):
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.close()

    def closeEvent(self, event):
        if self.player:
            self.player.requestInterruption()
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
            event.ignore()
        else:
            event.accept()


class PlayerThread(QThread):

    yield_resource = pyqtSignal(str)

    def __init__(self, selector, parent=None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.selector = selector

    def run(self):
        LOG.debug("Thread started %s" % self)
        for file in self.selector:
            self.yield_resource.emit(file)
            if self.isInterruptionRequested():
                LOG.debug("Thread interrupt was requested and granted %s" % self)
                break
        LOG.debug("Thread finished %s" % self)


