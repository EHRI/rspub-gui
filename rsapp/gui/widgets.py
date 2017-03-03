#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rsapp.gui.conf import GuiConf
from rsapp.gui.style import Style
from rspub.core.rs_enum import Strategy

LOG = logging.getLogger(__name__)


class ParaWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.accepted = True

    def on_switch_language(self):
        raise NotImplementedError

    def on_switch_configuration(self):
        raise NotImplementedError

    def is_accepted(self):
        return self.accepted

    @staticmethod
    def str2tx(x):
        return x

    @staticmethod
    def tx2str(x):
        return x

    @staticmethod
    def int2tx(x):
        return str(x)

    @staticmethod
    def tx2int(x):
        return int(x)

    @staticmethod
    def str_conv():
        return ParaWidget.str2tx, ParaWidget.tx2str

    @staticmethod
    def int_conv():
        return ParaWidget.int2tx, ParaWidget.tx2int


class ParaLine(ParaWidget):

    def __init__(self, parent, name, conv, grid, ordinal, browse=False, width=None):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.v2tx = conv[0]
        self.tx2v = conv[1]
        self.grid = grid
        self.ordinal = ordinal
        self.browse = browse

        self.label = QLabel(self)
        self.edit = QLineEdit()
        if width:
            self.edit.setFixedWidth(width)
        self.button = QPushButton()
        self.err_label = QLabel(self)
        self.err_label.setStyleSheet(Style.error())
        self.err_label.setVisible(False)

        self.edit.textChanged.connect(self.parameter_changed)
        self.edit.editingFinished.connect(self.parameter_finished)
        self.button.clicked.connect(self.button_clicked)

        grid.addWidget(self.label, ordinal, 1)
        grid.addWidget(self.edit, ordinal, 2)
        if self.browse:
            grid.addWidget(self.button, ordinal, 3)
        grid.addWidget(self.err_label, ordinal + 1, 1, 1, 3)

        self.on_switch_language()
        self.on_switch_configuration()

    def parameter_changed(self, text):
        try:
            value = self.tx2v(text)
            setattr(self.paras, self.name, value)
            self.accepted = True
            self.err_label.setText("")
            self.err_label.setVisible(False)
            self.edit.setStyleSheet(Style.default())
            self.label.setStyleSheet(Style.default())
            self.edit.setToolTip(None)
        except ValueError as err:
            self.accepted = False
            self.err_label.setText(str(err))
            self.err_label.setVisible(True)
            self.edit.setStyleSheet(Style.error())
            self.label.setStyleSheet(Style.error())

    def parameter_finished(self):
        try:
            value = self.tx2v(self.edit.text())
            setattr(self.paras, self.name, value)
            self.paras.save_configuration()
            self.accepted = True
            self.err_label.setText("")
            self.err_label.setVisible(False)
            value = self.v2tx(getattr(self.paras, self.name))
            self.edit.setText(value)
            self.edit.setStyleSheet(Style.default())
            self.label.setStyleSheet(Style.default())
        except ValueError as err:
            self.accepted = False
            self.err_label.setText(str(err))
            self.err_label.setVisible(True)
            self.edit.setStyleSheet(Style.error())
            self.label.setStyleSheet(Style.error())

    def button_clicked(self):
        self.edit.setFocus()
        if self.browse == "SaveFileName":
            filename = QFileDialog.getSaveFileName(self.parent(), _(self.name + "_label"),
                                                        getattr(self.paras, self.name))
            if filename[0] != "":
                self.edit.setText(filename[0])
        else:
            filename = QFileDialog.getExistingDirectory(self.parent(), _(self.name + "_label"),
                                                    getattr(self.paras, self.name))
            if filename != "":
                self.edit.setText(filename)


    def on_switch_language(self):
        self.label.setText(_(self.name + "_label"))
        self.button.setText(_("Browse"))

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        value = self.v2tx(getattr(self.paras, self.name))
        self.edit.setText(value)


class ParaCheck(ParaWidget):

    def __init__(self, parent, name, grid, ordinal):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.check = QCheckBox("", self)
        self.check.setFixedHeight(25)
        self.check.toggled.connect(self.on_toggled)
        grid.addWidget(self.check, ordinal, 2)

        self.on_switch_language()
        self.on_switch_configuration()

    def on_toggled(self, checked):
        if checked != getattr(self.paras, self.name):
            setattr(self.paras, self.name, checked)
            # link paras.is_saving_sitemaps to 'trial run' on ExecuteWidget Frame:
            self.ctrl.update_configuration(self.paras)

    def on_switch_language(self):
        self.check.setText(_(self.name + "_label"))

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        self.check.setChecked(getattr(self.paras, self.name))


class ParaStrategyDrop(ParaWidget):

    def __init__(self, parent, name, grid, ordinal):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.label = QLabel(self)
        self.combo = QComboBox(self)
        self.combo.activated.connect(self.on_activated)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.combo)
        hbox.addStretch(1)

        grid.addWidget(self.label, ordinal, 1)
        grid.addLayout(hbox, ordinal, 2)

        self.on_switch_language()
        self.on_switch_configuration()

    def on_activated(self):
        setattr(self.paras, self.name, self.combo.currentData())
        self.paras.save_configuration()

    def on_switch_language(self):
        self.label.setText(_(self.name + "_label"))
        self.combo.clear()
        for i in range(len(Strategy.names())):
            strategy = Strategy.strategy_for(i)
            self.combo.addItem(_(str(strategy)), strategy.name)

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        strategy = getattr(self.paras, self.name)
        self.combo.setCurrentIndex(strategy.value)


class WorkWidget(QWidget):

    work_started = pyqtSignal()
    work_ended = pyqtSignal()

    def __init__(self, work="", title_style=Style.h2()):
        QWidget.__init__(self)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.conf = GuiConf()
        # work should be a verb: Execute, Transport ...
        self.work = work
        self.title_style = title_style
        self.setWindowTitle(_(self.work))
        self.executor_thread = None
        self.splitter_event_moved = False
        self.splitter_title_moved = False
        self.init_ui()
        self.show()

    def init_ui(self):
        vbox = QVBoxLayout()

        self.label_title = QLabel("%s %s" % (_(self.work), self.paras.configuration_name()))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(10, 5, 5, 7)
        self.label_title.setStyleSheet(self.title_style)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label_title, 1)
        vbox.addLayout(hbox1)

        self.splitter_title = QSplitter(Qt.Vertical)
        self.splitter_event = QSplitter(Qt.Vertical)
        self.splitter_title.splitterMoved.connect(self.on_splitter_title_moved)
        self.splitter_event.splitterMoved.connect(self.on_splitter_event_moved)

        self.lbl_events_title1 = QLabel(_("Main events"))
        self.splitter_title.addWidget(self.lbl_events_title1)

        self.lbl_events_title2 = QLabel(_("Resources"))
        self.splitter_title.addWidget(self.lbl_events_title2)

        self.lbl_events_title3 = QLabel(_("Errors"))
        self.splitter_title.addWidget(self.lbl_events_title3)

        self.pte_events1 = QTextBrowser()
        self.pte_events1.setOpenExternalLinks(True)
        self.pte_events1.setOpenLinks(False)
        self.pte_events1.anchorClicked.connect(self.on_anchor_clicked)
        self.pte_events1.setLineWrapMode(QTextEdit.NoWrap)
        self.splitter_event.addWidget(self.pte_events1)

        self.pte_events2 = QTextBrowser()
        self.pte_events2.setOpenExternalLinks(True)
        self.pte_events2.setOpenLinks(False)
        self.pte_events2.anchorClicked.connect(self.on_anchor_clicked)
        self.pte_events2.setLineWrapMode(QTextEdit.NoWrap)
        self.splitter_event.addWidget(self.pte_events2)

        self.pte_events3 = QPlainTextEdit()
        self.pte_events3.setReadOnly(True)
        self.pte_events3.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pte_events3.setStyleSheet(Style.red_text())
        self.pte_events3.setCenterOnScroll(True)
        self.splitter_event.addWidget(self.pte_events3)

        self.splitter_title.setStretchFactor(0, 5)
        self.splitter_title.setStretchFactor(1, 3)
        self.splitter_title.setStretchFactor(2, 1)
        self.splitter_event.setStretchFactor(0, 5)
        self.splitter_event.setStretchFactor(1, 3)
        self.splitter_event.setStretchFactor(2, 1)
        hbox_splitters = QHBoxLayout()
        hbox_splitters.addWidget(self.splitter_title, 0)
        hbox_splitters.addWidget(self.splitter_event, 5)
        vbox.addLayout(hbox_splitters)

        lbl_box = QHBoxLayout()
        self.lbl_processing = QLabel(_("Processing:"))
        self.lbl_processing_file = QLabel("")
        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.lbl_processing_file.setFont(font)
        self.lbl_processing.setFont(font)
        self.lbl_processing.setVisible(False)
        self.lbl_processing_file.setVisible(False)
        lbl_box.addWidget(self.lbl_processing)
        lbl_box.addWidget(self.lbl_processing_file)
        lbl_box.addStretch(1)
        vbox.addLayout(lbl_box)

        btn_box = QHBoxLayout()
        btn_box.addStretch(1)
        self.chk_trial_run = QCheckBox(_("Trial run"))
        self.chk_trial_run.setChecked(not self.paras.is_saving_sitemaps)
        btn_box.addWidget(self.chk_trial_run)
        self.btn_run = QPushButton(_("Run"))
        self.btn_run.clicked.connect(self.on_btn_run_clicked)
        btn_box.addWidget(self.btn_run)
        self.btn_stop = QPushButton(_("Stop"))
        self.btn_stop.clicked.connect(self.on_btn_stop_clicked)
        self.normal_style = self.btn_stop.styleSheet()
        self.btn_stop.setEnabled(False)
        btn_box.addWidget(self.btn_stop)
        self.btn_close = QPushButton(_("Close"))
        self.btn_close.clicked.connect(self.on_btn_close_clicked)
        btn_box.addWidget(self.btn_close)
        vbox.addLayout(btn_box)

        self.setLayout(vbox)
        self.resize(self.conf.work_widget_width(self.work), self.conf.work_widget_height(self.work))

    def on_splitter_title_moved(self, pos, index):
        self.splitter_title_moved = True
        if not self.splitter_event_moved:
            self.splitter_event.moveSplitter(pos, index)
        self.splitter_title_moved = False

    def on_splitter_event_moved(self, pos, index):
        self.splitter_event_moved = True
        if not self.splitter_title_moved:
            self.splitter_title.moveSplitter(pos, index)
        self.splitter_event_moved = False

    def on_switch_language(self):
        self.setWindowTitle(_(self.work))
        self.label_title.setText("%s %s" % (_(self.work), self.paras.configuration_name()))
        self.lbl_events_title1.setText(_("Main events"))
        self.lbl_events_title2.setText(_("Resources"))
        self.lbl_events_title3.setText(_("Errors"))
        self.lbl_processing.setText(_("Processing:"))
        self.chk_trial_run.setText(_("Trial run"))
        self.btn_run.setText(_("Run"))
        self.btn_stop.setText(_("Stop"))
        self.btn_close.setText(_("Close"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.label_title.setText("%s %s" % (_(self.work), self.paras.configuration_name()))

    def on_anchor_clicked(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def on_btn_run_clicked(self):
        self.work_started.emit()
        self.pte_events1.setPlainText("")
        self.pte_events2.setPlainText("")
        self.pte_events3.setPlainText("")
        self.lbl_processing.setVisible(True)
        self.lbl_processing_file.setVisible(True)

        self.btn_close.setEnabled(False)
        self.btn_run.setEnabled(False)
        self.chk_trial_run.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_stop.setStyleSheet(Style.alarm())

    def on_btn_stop_clicked(self):
        self.btn_stop.setStyleSheet(self.normal_style)
        self.btn_stop.setEnabled(False)
        if self.executor_thread:
            self.executor_thread.requestInterruption()

    def on_signal_exception(self, msg):
        self.pte_events3.appendHtml(msg)
        self.update()

    def on_ask_confirmation(self, text, i_text, answer):
        msg_box = QMessageBox()
        msg_box.setText(text)
        i_text += "\n\n"
        i_text += _("Ok to proceed?")
        msg_box.setInformativeText(i_text)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        exe = msg_box.exec()
        if exe == QMessageBox.No:
            answer.answer = False
        else:
            answer.answer = True
        answer.answered = True

    def on_signal_main_event(self, msg):
        self.pte_events1.append(msg)
        self.update()

    def on_signal_minor_event(self, msg):
        self.pte_events2.append(msg)
        self.update()

    def on_signal_next_file(self, filename):
        lfn = len(filename)
        ww = (self.width() - 150)/7
        www = int(ww/2)
        if lfn > ww:
            filename = filename[:www] + "..." + filename[lfn - www:]
        self.lbl_processing_file.setText(filename)
        self.update()

    def on_signal_end_processing(self, paras):
        self.ctrl.update_configuration(paras)

    def on_executor_thread_finished(self):
        self.btn_stop.setStyleSheet(self.normal_style)
        self.btn_stop.setEnabled(False)
        self.btn_close.setEnabled(True)
        self.btn_run.setEnabled(True)
        self.chk_trial_run.setEnabled(True)
        self.lbl_processing.setVisible(False)
        self.lbl_processing_file.setVisible(False)
        self.update()
        self.work_ended.emit()

    def on_btn_close_clicked(self):
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.close()
            self.destroy()

    def closeEvent(self, event):
        LOG.debug("Closing event on work window %s" % self.work)
        if self.executor_thread:
            self.executor_thread.requestInterruption()
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
            event.ignore()
        else:
            self.save_dimensions()
            event.accept()

    def save_dimensions(self):
        LOG.debug("Saving dimensions for work-window %s" % self.work)
        self.conf.set_work_widget_width(self.work, self.width())
        self.conf.set_work_widget_height(self.work, self.height())
        self.conf.persist()


class Answer(object):

    answered = False
    answer = False