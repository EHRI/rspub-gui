#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
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
from rspub.core.rs import ResourceSync
from rspub.core.rs_enum import SelectMode
from rspub.core.rs_paras import RsParameters
from rspub.core.selector import Selector
from rspub.util.observe import EventObserver

LOG = logging.getLogger(__name__)


class ExecuteFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.paras = self.ctrl.paras
        self.execute_widget = None
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

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        self.btn_run = QPushButton(_("Run..."))
        self.btn_run.clicked.connect(self.on_btn_run_clicked)
        vbox.addWidget(self.btn_run)
        hbox.addLayout(vbox)

        hbox.addStretch(1)
        vbl_0.addLayout(hbox)
        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Execute configuration: '%s'") % self.paras.configuration_name())
        self.btn_run.setText(_("Run..."))
        self.render()

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.label_title.setText(_("Execute configuration: '%s'") % self.paras.configuration_name())
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

    def on_btn_run_clicked(self):
        if self.execute_widget is None:
            self.execute_widget = ExecuteWidget()
        else:
            self.execute_widget.show()
            self.execute_widget.setWindowState(Qt.WindowActive)
            self.execute_widget.activateWindow()
            self.execute_widget.raise_()

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


# #################################################################
class ExecuteWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.trial_run = not self.paras.is_saving_sitemaps
        self.conf = GuiConf()
        self.setWindowTitle(_("Execute %s") % self.paras.configuration_name())
        self.executor_thread = None
        self.splitter_event_moved = False
        self.splitter_title_moved = False
        self.init_ui()
        self.show()

    def init_ui(self):
        vbox = QVBoxLayout()

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
        self.lbl_processing.setVisible(False)
        self.lbl_processing_file.setVisible(False)
        lbl_box.addWidget(self.lbl_processing)
        lbl_box.addWidget(self.lbl_processing_file)
        lbl_box.addStretch(1)
        vbox.addLayout(lbl_box)

        btn_box = QHBoxLayout()
        btn_box.addStretch(1)
        self.chk_trial_run = QCheckBox(_("Trial run"))
        self.chk_trial_run.setChecked(self.trial_run)
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
        self.resize(self.conf.execute_widget_width(), self.conf.execute_widget_height())

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
        self.setWindowTitle(_("Execute %s") % self.paras.configuration_name())
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
        self.setWindowTitle(_("Execute %s") % self.paras.configuration_name())
        self.trial_run = not self.paras.is_saving_sitemaps
        self.chk_trial_run.setChecked(self.trial_run)

    def on_btn_run_clicked(self):
        self.ctrl.update_selector()
        if self.paras.select_mode == SelectMode.simple:
            selector = Selector()
            if self.paras.simple_select_file:
                selector.include(self.paras.simple_select_file)
        else:
            selector = self.ctrl.selector
        self.paras.is_saving_sitemaps = not self.chk_trial_run.isChecked()
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

        self.executor_thread = ExecutorThread(self.paras, selector, self)
        self.executor_thread.signal_exception.connect(self.on_signal_exception)
        self.executor_thread.ask_confirmation.connect(self.on_ask_confirmation)
        self.executor_thread.signal_main_event.connect(self.on_signal_main_event)
        self.executor_thread.signal_minor_event.connect(self.on_signal_minor_event)
        self.executor_thread.signal_next_file.connect(self.on_signal_next_file)
        self.executor_thread.signal_end_processing.connect(self.on_signal_end_processing)
        self.executor_thread.finished.connect(self.on_executor_thread_finished)
        self.executor_thread.start()
        self.update()

    def on_btn_stop_clicked(self):
        self.btn_stop.setStyleSheet(self.normal_style)
        self.btn_stop.setEnabled(False)
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

    def on_anchor_clicked(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def on_btn_close_clicked(self):
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.close()

    def closeEvent(self, event):
        if self.executor_thread:
            self.executor_thread.requestInterruption()
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
            event.ignore()
        else:
            self.conf.set_execute_widget_width(self.width())
            self.conf.set_execute_widget_height(self.height())
            self.conf.persist()
            event.accept()


class Answer(object):

    answered = False
    answer = False


# #################################################################
class ExecutorThread(QThread, EventObserver):

    signal_exception = pyqtSignal(str)
    signal_main_event = pyqtSignal(str)
    signal_minor_event = pyqtSignal(str)
    signal_next_file = pyqtSignal(str)
    ask_confirmation = pyqtSignal(str, str, Answer)
    signal_end_processing = pyqtSignal(RsParameters)

    def __init__(self, paras, selector, parent=None):
        QThread.__init__(self, parent)
        EventObserver.__init__(self)
        self.paras = paras
        self.selector = selector
        self.file_count = 0
        self.excluded_file_count = 0
        self.rejected_by_gate_count = 0

    def run(self):
        LOG.debug("Executor thread started %s" % self)
        self.file_count = 0
        self.excluded_file_count = 0
        self.rejected_by_gate_count = 0
        rs = None
        try:
            rs = ResourceSync(**self.paras.__dict__)
            rs.register(self)
            self.selector.register(self)
            rs.execute(self.selector)
            paras = RsParameters(**rs.__dict__)
            self.signal_end_processing.emit(paras)
        except Exception as err:
            LOG.exception("Exception in executor thread:")
            self.signal_exception.emit(_("Exception in executor thread: {0}").format(err))
            self.inform_execution_end(date_end_processing=None)
        finally:
            self.selector.unregister(self)
            if rs:
                rs.unregister(self)

    def inform_execution_start(self, *args, **kwargs):
        self.signal_main_event.emit(_("Start execution: %s") % kwargs["date_start_processing"])

    def confirm_clear_metadata_directory(self, *args, **kwargs):
        metadata_dir = kwargs["metadata_dir"]
        text = _("Clear metadata directory")
        i_text = _("Clearing xml-files from \n%s") % metadata_dir
        answer = Answer()
        self.ask_confirmation.emit(text, i_text, answer)
        while not answer.answered:
            pass
        return answer.answer

    def inform_created_resource(self, *args, **kwargs):
        resource = kwargs["resource"]
        count = kwargs["count"]
        file = kwargs["file"]
        txt = "<code>"
        txt += str(count) + "&nbsp;&nbsp;"
        txt += str(resource.lastmod) + "</code>&nbsp;&nbsp;"
        txt += "<a href=\"file://" + file + "\">" + file + "</a>&nbsp;&nbsp;&#9679;&nbsp;&nbsp;"
        txt += "<a href=\"" + resource.uri + "\">" + resource.uri + "</a>&nbsp;&nbsp;"
        txt += "<code>" + str(resource.length) + "</code>"
        self.signal_minor_event.emit(txt)

    def inform_found_changes(self, *args, **kwargs):
        # created, updated, deleted, unchanged
        txt = "<h3>"
        txt += _("Summary of changes")
        txt += "</h3>"
        txt += "<table>"
        txt += "<tr><td>"
        txt += _("created") + "&nbsp;"
        txt += "</td><td>"
        txt += str(kwargs["created"])
        txt += "</td></tr><tr><td>"
        txt += _("updated") + "&nbsp;"
        txt += "</td><td>"
        txt += str(kwargs["updated"])
        txt += "</td></tr><tr><td>"
        txt += _("deleted") + "&nbsp;"
        txt += "</td><td>"
        txt += str(kwargs["deleted"])
        txt += "</td></tr><tr><td>"
        txt += _("unchanged") + "&nbsp;"
        txt += "</td><td>"
        txt += str(kwargs["unchanged"])
        txt += "</td></tr></table><br/><br/>"
        self.signal_main_event.emit(txt)

    def inform_completed_document(self, *args, **kwargs):
        sitemap_data = kwargs["sitemap_data"]
        self.signal_main_event.emit(self.pretty_print_sitemap_data(sitemap_data))

    def inform_execution_end(self, *args, **kwargs):
        trs = self.file_count - self.excluded_file_count - self.rejected_by_gate_count
        self.signal_main_event.emit(_("Total file count: %d") % self.file_count)
        self.signal_main_event.emit(_("Excluded by selector: %d") % self.excluded_file_count)
        self.signal_main_event.emit(_("Rejected by resource gate: %d") % self.rejected_by_gate_count)
        self.signal_main_event.emit(_("Total resources synchronized: %d") % trs)
        self.signal_main_event.emit(_("End execution: %s") % kwargs["date_end_processing"])

    @staticmethod
    def pretty_print_sitemap_data(sitemap_data):
        txt = ""
        txt += "<h3>"
        txt += sitemap_data.capability_name
        txt += "</h3>"
        txt += "<table>"
        txt += "<tr><td>"
        txt += _("path") + "&nbsp;"
        txt += "</td><td>"
        txt += "<a href=\"file://" + sitemap_data.path + "\">" + sitemap_data.path + "</a>"
        txt += "</td></tr><tr><td>"
        txt += _("uri") + "&nbsp;"
        txt += "</td><td>"
        txt += "<a href=\"" + sitemap_data.uri + "\">" + sitemap_data.uri + "</a>"
        txt += "</td></tr><tr><td>"
        txt += _("count resources") + "&nbsp;"
        txt += "</td><td>"
        txt += str(sitemap_data.resource_count)
        txt += "</td></tr><tr><td>"
        txt += _("document saved") + "&nbsp;"
        txt += "</td><td>"
        txt += _(str(sitemap_data.document_saved))
        txt += "</td></tr></table><br/><br/>"
        return txt

    # resource gate
    def inform_rejected_file(self, *args, **kwargs):
        self.rejected_by_gate_count += 1

    # selector events
    def inform_file_does_not_exist(self, *args, **kwargs):
        self.signal_exception.emit(_("File does not exist: %s") % kwargs["filename"])

    def inform_not_a_regular_file(self, *args, **kwargs):
        self.signal_exception.emit(_("Not a regular file: %s") % kwargs["filename"])

    def confirm_file_excluded(self, *args, **kwargs):
        self.excluded_file_count += 1
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()

    def confirm_next_file(self, *args, **kwargs):
        self.signal_next_file.emit(kwargs["filename"])
        self.file_count += 1
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()
