#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import QEvent
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
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rsapp.gui.conf import GuiConf
from rsapp.gui.style import Style
from rspub.core.rs_enum import SelectMode
from rspub.core.selector import Selector
from rspub.util.observe import EventObserver

LOG = logging.getLogger(__name__)


class SelectFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_selector.connect(self.on_switch_selector)
        self.paras = self.ctrl.paras
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

        self.grp_simple = QGroupBox(_("Simpel selection: One directory"))
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
        self.btn_simple_play = QPushButton(_("Play..."))
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

        # selector group: selector file
        self.lbl_saved_as = QLabel(_("Selector"))
        self.lbl_selector_file = QLabel()
        self.lbl_selector_file.setTextInteractionFlags(Qt.TextSelectableByMouse)
        grid.addWidget(self.lbl_saved_as, 1, 1)
        grid.addWidget(self.lbl_selector_file, 1, 2, 1, 2)

        # selector group: includes
        self.lbl_includes = QLabel(_("Includes"))
        self.lbl_includes.setAlignment(Qt.AlignTop)
        self.txt_includes = QPlainTextEdit()
        self.txt_includes.installEventFilter(self)
        self.btn_incl_directory = QPushButton(_("Add directory"))
        self.btn_incl_directory.clicked.connect(self.on_btn_incl_directory_clicked)
        self.btn_incl_files = QPushButton(_("Add files"))
        self.btn_incl_files.clicked.connect(self.on_btn_incl_files_clicked)
        self.btn_incl_import = QPushButton(_("Import entries"))
        self.btn_incl_import.clicked.connect(self.on_btn_incl_import_clicked)
        grid.addWidget(self.lbl_includes, 2, 1)
        grid.addWidget(self.txt_includes, 2, 2)
        vbox_inc = QVBoxLayout()
        vbox_inc.setSpacing(0)
        vbox_inc.addWidget(self.btn_incl_directory)
        vbox_inc.addWidget(self.btn_incl_files)
        vbox_inc.addWidget(self.btn_incl_import)
        vbox_inc.addStretch(1)
        grid.addLayout(vbox_inc, 2, 3)

        # selector group: excludes
        self.lbl_excludes = QLabel(_("Excludes"))
        self.lbl_excludes.setAlignment(Qt.AlignTop)
        self.txt_excludes = QPlainTextEdit()
        self.txt_excludes.installEventFilter(self)
        self.btn_excl_directory = QPushButton(_("Add directory"))
        self.btn_excl_directory.clicked.connect(self.on_btn_excl_directory_clicked)
        self.btn_excl_files = QPushButton(_("Add files"))
        self.btn_excl_files.clicked.connect(self.on_btn_excl_files_clicked)
        self.btn_excl_import = QPushButton(_("Import entries"))
        self.btn_excl_import.clicked.connect(self.on_btn_excl_import_clicked)
        grid.addWidget(self.lbl_excludes, 3, 1)
        grid.addWidget(self.txt_excludes, 3, 2)
        vbox_exc = QVBoxLayout()
        vbox_exc.setSpacing(0)
        vbox_exc.addWidget(self.btn_excl_directory)
        vbox_exc.addWidget(self.btn_excl_files)
        vbox_exc.addWidget(self.btn_excl_import)
        vbox_exc.addStretch(1)
        grid.addLayout(vbox_exc, 3, 3)

        # selector group: bottom buttons
        self.btn_open_selector = QPushButton(_("Open..."))
        self.btn_open_selector.clicked.connect(self.on_btn_open_selector_clicked)
        self.btn_save_selector_as = QPushButton(_("Save as..."))
        self.btn_save_selector_as.clicked.connect(self.on_btn_save_selector_as_clicked)
        self.btn_play_selected = QPushButton(_("Play..."))
        self.btn_play_selected.clicked.connect(self.on_btn_play_selected_clicked)
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn_open_selector)
        hbox3.addWidget(self.btn_save_selector_as)
        grid.addLayout(hbox3, 4, 1, 1, 2)
        grid.addWidget(self.btn_play_selected, 4, 3)

        self.grp_selector.setLayout(grid)
        vbl_0.addWidget(self.grp_selector)

        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Select resources"))
        self.grp_simple.setTitle(_("Simple selection: One directory"))
        self.lbl_simple.setText(_("Location"))
        self.btn_simple_brws.setText(_("Browse"))
        self.btn_simple_play.setText(_("Play..."))
        self.grp_selector.setTitle(_("Advanced: Create a selector"))
        self.lbl_includes.setText(_("Includes"))
        self.btn_incl_directory.setText(_("Add directory"))
        self.btn_incl_files.setText(_("Add files"))
        self.btn_incl_import.setText(_("Import entries"))
        self.lbl_excludes.setText(_("Excludes"))
        self.btn_excl_directory.setText(_("Add directory"))
        self.btn_excl_files.setText(_("Add files"))
        self.btn_excl_import.setText(_("Import entries"))
        self.lbl_saved_as.setText(_("Selector"))
        self.btn_open_selector.setText(_("Open..."))
        self.btn_save_selector_as.setText(_("Save as..."))
        self.btn_play_selected.setText(_("Play..."))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.grp_simple.setChecked(self.paras.select_mode == SelectMode.simple)
        self.grp_selector.setChecked(self.paras.select_mode == SelectMode.selector)
        self.edt_simple.setText(self.paras.simple_select_file)

    def on_switch_selector(self):
        self.txt_includes.setPlainText("\n".join(self.ctrl.selector.get_included_entries()))
        self.txt_excludes.setPlainText("\n".join(self.ctrl.selector.get_excluded_entries()))
        if self.ctrl.selector.location:
            self.lbl_selector_file.setText(self.ctrl.selector.abs_location())
        else:
            self.lbl_selector_file.setText("")
        self.lbl_saved_as.setVisible(self.lbl_selector_file.text() != "")

    def refresh_includes(self):
        includes = set(self.txt_includes.toPlainText().splitlines())
        includes = sorted([x for x in includes if len(x.strip()) > 0])
        self.txt_includes.setPlainText("\n".join(includes))
        return includes

    def refresh_excludes(self):
        excludes = set(self.txt_excludes.toPlainText().splitlines())
        excludes = sorted([x for x in excludes if len(x.strip()) > 0])
        self.txt_excludes.setPlainText("\n".join(excludes))
        return excludes

    def synchronize_selector(self):
        includes = self.refresh_includes()
        self.ctrl.selector.clear_includes()
        self.ctrl.selector.include(includes)
        excludes = self.refresh_excludes()
        self.ctrl.selector.clear_excludes()
        self.ctrl.selector.exclude(excludes)
        self.ctrl.save_selector()

    def eventFilter(self, source, event):
        if event.type() == QEvent.FocusOut and (source is self.txt_includes or source is self.txt_excludes):
            self.synchronize_selector()
        return super(SelectFrame, self).eventFilter(source, event)

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
        dlg.setFileMode(QFileDialog.AnyFile)
        filename = dlg.getExistingDirectory()
        if filename:
            self.edt_simple.setText(filename)

    def on_edt_simple_finished(self):
        self.paras.simple_select_file = self.edt_simple.text()
        self.paras.save_configuration()

    def on_btn_simple_play_clicked(self):
        if self.play_widget_simple is None:
            self.play_widget_simple = PlayWidget(self.__get_simple_selector, "Simpel selection: List resources")
        else:
            self.play_widget_simple.show()
            self.play_widget_simple.setWindowState(Qt.WindowActive)
            self.play_widget_simple.activateWindow()
            self.play_widget_simple.raise_()

    def __get_simple_selector(self):
        selector = Selector()
        if self.paras.simple_select_file:
            selector.include(self.paras.simple_select_file)
        return selector

    # ########################################################
    def on_btn_incl_directory_clicked(self):
        self.txt_includes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.Directory)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_includes.appendPlainText(file)
            # refresh content of widget
            self.refresh_includes()

    def on_btn_incl_files_clicked(self):
        self.txt_includes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_includes.appendPlainText(file)
            # refresh content of widget
            self.refresh_includes()

    def on_btn_incl_import_clicked(self):
        self.synchronize_selector()
        filenames = QFileDialog.getOpenFileName(self, _("Import included filenames"), self.ctrl.last_directory)
        if filenames[0] != "":
            self.ctrl.load_selector_includes(filenames[0])

    def on_btn_excl_directory_clicked(self):
        self.txt_excludes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.Directory)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_excludes.appendPlainText(file)
            # refresh content of widget
            self.refresh_excludes()

    def on_btn_excl_files_clicked(self):
        self.txt_excludes.setFocus()
        dlg = QFileDialog(self)
        dlg.setDirectory(self.paras.resource_dir)
        dlg.setFileMode(QFileDialog.ExistingFiles)
        result = dlg.exec()
        if result > 0:
            for file in dlg.selectedFiles():
                self.txt_excludes.appendPlainText(file)
            # refresh content of widget
            self.refresh_excludes()

    def on_btn_excl_import_clicked(self):
        self.synchronize_selector()
        filenames = QFileDialog.getOpenFileName(self, _("Import excluded filenames"), self.ctrl.last_directory)
        if filenames[0] != "":
            self.ctrl.load_selector_excludes(filenames[0])

    # #######################################
    def on_btn_save_selector_as_clicked(self):
        saved = False
        self.synchronize_selector()
        if self.ctrl.selector.location:
            directory = self.ctrl.selector.abs_location()
        else:
            directory = os.path.join(os.path.expanduser("~"), "selector.csv")
        filenames = QFileDialog.getSaveFileName(self, _("Save selector"), directory)
        if filenames[0] != "":
            self.ctrl.save_selector_as(filenames[0])
            saved = True
        return saved

    def on_btn_open_selector_clicked(self):
        if self.on_about_to_change(_("Open a new selector")):
            if self.ctrl.selector.location:
                directory = os.path.dirname(self.ctrl.selector.abs_location())
            else:
                directory = os.path.expanduser("~")
            filenames = QFileDialog.getOpenFileName(self, _("Open selector"), directory)
            if filenames[0] != "":
                self.ctrl.open_selector(filenames[0])

    def on_about_to_change(self, window_title):
        ok_to_change = True
        self.synchronize_selector()
        if self.ctrl.selector.location is None and not self.ctrl.selector.is_empty():
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
        self.synchronize_selector()
        if self.play_widget_selector is None:
            self.play_widget_selector = PlayWidget(self.__get_advanced_selector, "Advanced: List resources")
        else:
            self.play_widget_selector.show()
            self.play_widget_selector.setWindowState(Qt.WindowActive)
            self.play_widget_selector.activateWindow()
            self.play_widget_selector.raise_()

    def __get_advanced_selector(self):
        return self.ctrl.selector

    def translatables(self):
        _("Advanced: List resources")
        _("Simpel selection: List resources")


# #################################################################
class PlayWidget(QWidget):

    def __init__(self, get_selector, title=None, max_lines=1000000):
        QWidget.__init__(self)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.get_selector = get_selector
        self.window_title = title
        self.setWindowTitle(_(self.window_title))
        self.max_lines = max_lines
        self.conf = GuiConf()

        self.player = None
        self.resource_count = 0
        self.excluded_resource_count = 0
        self.exception_count = 0

        self.__init_ui__()
        self.show()

    def __init_ui__(self):
        vbox = QVBoxLayout()

        self.lbl_explanation = QLabel(_("Selected resources"))
        vbox.addWidget(self.lbl_explanation)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)

        self.pte_output = QPlainTextEdit()
        self.pte_output.setReadOnly(True)
        self.pte_output.setMaximumBlockCount(self.max_lines)
        self.pte_output.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pte_output.setCenterOnScroll(True)
        splitter.addWidget(self.pte_output)

        self.pte_exceptions = QPlainTextEdit()
        self.pte_exceptions.setReadOnly(True)
        self.pte_exceptions.setMaximumBlockCount(5000)
        self.pte_exceptions.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pte_exceptions.setCenterOnScroll(True)
        self.pte_exceptions.setStyleSheet(Style.blue_text())
        splitter.addWidget(self.pte_exceptions)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        vbox.addWidget(splitter)

        btn_box = QHBoxLayout()

        count_grid = QGridLayout()
        count_grid.setSpacing(3)
        self.lbl_recources_count = QLabel(_("Selected resources:"))
        count_grid.addWidget(self.lbl_recources_count, 1, 1)
        self.lbl_resources_counter = QLabel("0")
        self.lbl_resources_counter.setTextInteractionFlags(Qt.TextSelectableByMouse)
        count_grid.addWidget(self.lbl_resources_counter, 1, 2)

        self.lbl_excluded_recources_count = QLabel(_("Excluded resources:"))
        count_grid.addWidget(self.lbl_excluded_recources_count, 2, 1)
        self.lbl_excluded_resources_counter = QLabel("0")
        self.lbl_excluded_resources_counter.setTextInteractionFlags(Qt.TextSelectableByMouse)
        count_grid.addWidget(self.lbl_excluded_resources_counter, 2, 2)

        btn_box.addLayout(count_grid)
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
        self.resize(self.conf.play_widget_width(), self.conf.play_widget_height())

    def on_switch_language(self):
        self.setWindowTitle(_(self.window_title))
        self.lbl_explanation.setText(_("Selected resources"))
        self.lbl_recources_count.setText(_("Selected resources:"))
        self.lbl_excluded_recources_count.setText(_("Excluded resources:"))
        self.btn_play.setText(_("Play"))
        self.btn_stop.setText(_("Stop"))
        self.btn_close.setText(_("Close"))

    def on_btn_play_clicked(self):
        self.pte_output.setPlainText("")
        self.pte_exceptions.setPlainText("")
        selector = self.get_selector()
        self.player = PlayerThread(selector, self)
        self.player.yield_resource.connect(self.on_yield_resource)
        self.player.signal_exception.connect(self.on_signal_exception)
        self.player.signal_excluded_resource.connect(self.on_signal_excluded_resource)
        self.player.finished.connect(self.on_player_finished)
        # counters
        self.resource_count = 0
        self.excluded_resource_count = 0
        self.exception_count = 0
        self.lbl_resources_counter.setText(str(self.resource_count))
        self.lbl_excluded_resources_counter.setText(str(self.excluded_resource_count))
        # buttons
        self.btn_close.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_stop.setStyleSheet(Style.alarm())
        self.player.start()
        self.update()

    def on_yield_resource(self, file):
        self.resource_count += 1
        self.lbl_resources_counter.setText(str(self.resource_count))
        self.pte_output.appendPlainText(file)
        self.update()

    def on_signal_exception(self, msg):
        self.exception_count += 1
        self.pte_exceptions.appendHtml("<span style=color:red;>" + msg + "</span>")

    def on_signal_excluded_resource(self, msg):
        self.excluded_resource_count += 1
        self.lbl_excluded_resources_counter.setText(str(self.excluded_resource_count))
        self.pte_exceptions.appendPlainText(msg)
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
            self.conf.set_play_widget_width(self.width())
            self.conf.set_play_widget_height(self.height())
            self.conf.persist()
            event.accept()


# ##############################################################################
class PlayerThread(QThread, EventObserver):

    yield_resource = pyqtSignal(str)
    signal_exception = pyqtSignal(str)
    signal_excluded_resource = pyqtSignal(str)

    def __init__(self, selector, parent=None):
        QThread.__init__(self, parent)
        EventObserver.__init__(self)
        self.selector = selector
        self.selector.register(self)

    def run(self):
        LOG.debug("Player thread started %s" % self)
        try:
            for file in self.selector:
                self.yield_resource.emit(file)
                if self.isInterruptionRequested():
                    LOG.debug("Player thread interrupted %s" % self)
                    break
            LOG.debug("Player thread finished %s" % self)
        except:
            LOG.exception("Unregular end of PlayerTread execution.")
        finally:
            self.selector.unregister(self)

    def inform_file_does_not_exist(self, *args, **kwargs):
        self.signal_exception.emit(_("File does not exist: %s") % kwargs["filename"])

    def inform_not_a_regular_file(self, *args, **kwargs):
        self.signal_exception.emit(_("Not a regular file: %s") % kwargs["filename"])

    def confirm_file_excluded(self, *args, **kwargs):
        self.signal_excluded_resource.emit(_("File excluded: %s") % kwargs["filename"])
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()

    def confirm_next_file(self, *args, **kwargs):
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()


