#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QActionEvent
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
from rsapp.gui.widgets import WorkWidget, Answer
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

        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        lbl_color = QLabel("   ", self)
        lbl_color.setStyleSheet(Style.execute_title())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_color)
        hbox1.addWidget(self.label_title, 1)
        hbox1.setContentsMargins(0, 0, 0, 5)
        vbl_0.addLayout(hbox1)
        #
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(2)
        grid.setHorizontalSpacing(2)

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
        hbox2 = QHBoxLayout()
        hbox2.addLayout(grid)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        self.btn_run = QPushButton(_("Run..."))
        self.btn_run.clicked.connect(self.on_btn_run_clicked)
        vbox.addWidget(self.btn_run)
        hbox2.addLayout(vbox)

        hbox2.addStretch(1)
        vbl_0.addLayout(hbox2)
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
                value = "<a href=\"" + value + "\">" + value + "</a>"
            if isinstance(value, list):
                value = str(len(value))

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

    def close(self):
        LOG.debug("ExecuteFrame closing")
        if self.execute_widget:
            self.execute_widget.save_dimensions()

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
class ExecuteWidget(WorkWidget):

    def __init__(self):
        WorkWidget.__init__(self, work="Execute", title_style=Style.execute_title())
        _("Execute")

    def on_switch_configuration(self, name=None):
        super(ExecuteWidget, self).on_switch_configuration(name)
        self.chk_trial_run.setChecked(not self.paras.is_saving_sitemaps)

    def on_btn_run_clicked(self):
        super(ExecuteWidget, self).on_btn_run_clicked()
        if self.paras.select_mode == SelectMode.simple:
            selector = Selector()
            if self.paras.simple_select_file:
                selector.include(self.paras.simple_select_file)
        else:
            selector = self.ctrl.selector
        self.paras.is_saving_sitemaps = not self.chk_trial_run.isChecked()

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
