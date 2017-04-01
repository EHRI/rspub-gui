#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QThread
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style
from rsapp.gui.widgets import SelectableLabel, WorkWidget, Answer
from rspub.core.audit import Audit
from rspub.core.rs_paras import RsParameters
from rspub.util.observe import EventObserver

LOG = logging.getLogger(__name__)


class AuditFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl

        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.audit_widget = None

        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())
        self.on_switch_configuration()

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
        lbl_color.setStyleSheet(Style.audit_title())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_color)
        hbox1.addWidget(self.label_title, 1)
        self.btn_help = QPushButton(_("Help..."), self)
        self.btn_help.clicked.connect(self.on_button_help_clicked)
        hbox1.addWidget(self.btn_help)
        hbox1.setContentsMargins(0, 0, 0, 5)
        vbl_0.addLayout(hbox1)

        grid1 = QGridLayout()
        grid1.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid1.setVerticalSpacing(2)
        grid1.setHorizontalSpacing(2)

        self.lbl_metadata_key = SelectableLabel(self)
        self.lbl_metadata_value = SelectableLabel(self)
        grid1.addWidget(self.lbl_metadata_key, 2, 1)
        grid1.addWidget(self.lbl_metadata_value, 2, 2)

        self.lbl_last_execution_key = SelectableLabel(self)
        self.lbl_last_execution_value = SelectableLabel(self)
        grid1.addWidget(self.lbl_last_execution_key, 3, 1)
        grid1.addWidget(self.lbl_last_execution_value, 3, 2)

        self.lbl_web_server_key = SelectableLabel(self)
        self.lbl_web_server_value = SelectableLabel(self)
        grid1.addWidget(self.lbl_web_server_key, 4, 1)
        grid1.addWidget(self.lbl_web_server_value, 4, 2)

        self.lbl_server_path_key = SelectableLabel(self)
        self.lbl_server_path_value = SelectableLabel(self)
        grid1.addWidget(self.lbl_server_path_key, 5, 1)
        grid1.addWidget(self.lbl_server_path_value, 5, 2)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(grid1)
        hbox2.addStretch(1)
        vbl_0.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        self.radio_all = QRadioButton(_("Audit all resources"))
        self.radio_all.setChecked(False)
        self.radio_latest = QRadioButton(_("Audit latest changes"))
        self.radio_latest.setChecked(True)
        hbox3.addWidget(self.radio_all)
        hbox3.addWidget(self.radio_latest)
        self.btn_start = QPushButton(_("Start"))
        self.btn_start.clicked.connect(self.on_btn_start_clicked)
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn_start)
        vbl_0.addLayout(hbox3)

        vbl_0.insertSpacing(2, 25)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_button_help_clicked(self):
        link = "http://rspub-gui.readthedocs.io/en/latest/rst/rsgui.audit.html"
        QDesktopServices.openUrl(QUrl(link))

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Audit: '%s'") % self.ctrl.paras.configuration_name())
        self.btn_help.setText(_("Help..."))
        self.lbl_metadata_key.setText(_("Audit based on"))
        self.lbl_last_execution_key.setText(_("last_execution_label"))
        self.lbl_web_server_key.setText(_("web_server_label"))
        self.lbl_server_path_key.setText(_("server_path_label"))
        #
        self.radio_all.setText(_("Audit all resources"))
        self.radio_latest.setText(_("Audit latest changes"))
        self.btn_start.setText(_("Start"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.label_title.setText(_("Audit: '%s'") % self.ctrl.paras.configuration_name())
        #
        self.lbl_metadata_value.setText(self.ctrl.paras.abs_metadata_dir())
        value = self.ctrl.paras.last_execution
        if value is None:
            value = "None"
        self.lbl_last_execution_value.setText(_(value))
        self.lbl_web_server_value.setText(self.ctrl.paras.server_root())
        self.lbl_server_path_value.setText(self.ctrl.paras.server_path())
        #

    def on_switch_tab(self, from_index, to_index):
        if to_index == self.index:
            self.on_switch_configuration()

    def on_btn_start_clicked(self):
        self.activate_worker(self.radio_all.isChecked())

    def activate_worker(self, all_resources=False):
        if self.audit_widget:
            self.audit_widget.close()
            self.audit_widget.destroy()

        self.audit_widget = AuditWidget(all_resources)
        self.audit_widget.work_started.connect(self.on_work_started)
        self.audit_widget.work_ended.connect(self.on_work_ended)

    def on_work_started(self):
        self.btn_start.setEnabled(False)

    def on_work_ended(self):
        self.btn_start.setEnabled(True)

    def close(self):
        LOG.debug("AuditFrame closing")
        if self.audit_widget:
            self.audit_widget.save_dimensions()


class AuditWidget(WorkWidget):

    def __init__(self, all_resources=False):
        WorkWidget.__init__(self, work="Audit", title_style=Style.audit_title())
        self.chk_trial_run.setVisible(False)
        self.all_resources = all_resources

    def on_btn_run_clicked(self):
        super(AuditWidget, self).on_btn_run_clicked()
        self.executor_thread = AuditThread(self.paras,
                                           self.all_resources,
                                           self)
        self.executor_thread.signal_exception.connect(self.on_signal_exception)
        self.executor_thread.ask_confirmation.connect(self.on_ask_confirmation)
        self.executor_thread.signal_main_event.connect(self.on_signal_main_event)
        self.executor_thread.signal_minor_event.connect(self.on_signal_minor_event)
        self.executor_thread.signal_next_file.connect(self.on_signal_next_file)
        self.executor_thread.signal_end_processing.connect(self.on_signal_end_processing)
        self.executor_thread.finished.connect(self.on_executor_thread_finished)
        self.executor_thread.start()
        self.update()


class AuditThread(QThread, EventObserver):

    signal_exception = pyqtSignal(str)
    signal_main_event = pyqtSignal(str)
    signal_minor_event = pyqtSignal(str)
    signal_next_file = pyqtSignal(str)
    ask_confirmation = pyqtSignal(str, str, Answer)
    signal_end_processing = pyqtSignal(RsParameters)

    def __init__(self, paras, all_resources=False, parent=None):
        QThread.__init__(self, parent)
        EventObserver.__init__(self)
        self.paras = paras
        self.all_resources = all_resources

    def run(self):
        LOG.debug("Audit thread started %s" % self)
        audit = None
        try:
            audit = Audit(self.paras)
            audit.register(self)
            audit.run_audit(self.all_resources)
            self.signal_end_processing.emit(self.paras)
        except Exception as err:
            LOG.exception("Exception in audit thread:")
            self.signal_exception.emit(_("Exception in audit thread: {0}").format(err))
        finally:
            if audit:
                audit.unregister(self)

    def pass_inform(self, *args, **kwargs):
        print(">>>>> inform >>>>>>", args, kwargs)

    def pass_confirm(self, *args, **kwargs):
        print(">>>>> confirm >>>>>", args, kwargs)
        return True

    def inform_audit_start(self, *args, **kwargs):
        all = kwargs["all_resources"]
        txt = _("Start audit. all resources=%s") % all
        self.signal_main_event.emit(txt)

    def confirm_test_resource_uri(self, *args, **kwargs):
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()

    def confirm_test_sitemap_uri(self, *args, **kwargs):
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()

    def inform_resource_uri_ok(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_ok = kwargs["count_ok"]
        txt = "<code>ok:&nbsp;"
        txt += str(count_ok) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_minor_event.emit(txt)

    def inform_sitemap_uri_ok(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_ok = kwargs["count_ok"]
        txt = "<code>ok:&nbsp;"
        txt += str(count_ok) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_minor_event.emit(txt)

    def inform_resource_uri_404(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_404 = kwargs["count_404"]
        txt = "<code>Not Found:&nbsp;"
        txt += str(count_404) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_exception.emit(txt)

    def inform_sitemap_uri_404(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_404 = kwargs["count_404"]
        txt = "<code>Not Found:&nbsp;"
        txt += str(count_404) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_exception.emit(txt)

    def inform_resource_checksum_error(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_checksum_error = kwargs["count_checksum_error"]
        txt = "<code>Checksum not equal:&nbsp;"
        txt += str(count_checksum_error) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_exception.emit(txt)

    def inform_sitemap_checksum_error(self, *args, **kwargs):
        uri = kwargs["uri"]
        count_checksum_error = kwargs["count_checksum_error"]
        txt = "<code>Checksum not equal:&nbsp;"
        txt += str(count_checksum_error) + "&nbsp;&nbsp;"
        txt += "<a href=\"" + uri + "\">" + uri + "</a></code>"
        self.signal_exception.emit(txt)

    def inform_audit_global_error(self, *args, **kwargs):
        exception = kwargs["exception"]
        txt = "Other exception: "
        txt += exception
        self.signal_exception.emit(txt)

    def inform_audit_end(self, *args, **kwargs):
        count_resources = kwargs["count_resources"]
        count_resources_uri_ok = kwargs["count_resources_uri_ok"]
        count_resources_uri_404 = kwargs["count_resources_uri_404"]
        count_resources_checksum_error = kwargs["count_resources_checksum_error"]
        #
        count_sitemaps = kwargs["count_sitemaps"]
        count_sitemaps_uri_ok = kwargs["count_sitemaps_uri_ok"]
        count_sitemaps_uri_404 = kwargs["count_sitemaps_uri_404"]
        count_sitemaps_checksum_error = kwargs["count_sitemaps_checksum_error"]
        #
        count_global_errors = kwargs["count_global_errors"]
        total_errors = count_resources_uri_404 + count_resources_checksum_error\
                       + count_sitemaps_uri_404 + count_sitemaps_checksum_error + count_global_errors
        txt = _("End Audit.")
        txt += "<hr>"
        txt += "<table>"
        txt += "<tr><td>"
        txt += _("total resources") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_resources)
        txt += "</td></tr><tr><td>"
        txt += _("resources free of error") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_resources_uri_ok)
        txt += "</td></tr><tr><td>"
        txt += _("resources not found") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_resources_uri_404)
        txt += "</td></tr><tr><td>"
        txt += _("resources not in sync") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_resources_checksum_error)
        txt += "</td></tr><tr><td></td><td></td></tr><tr><td>"
        #
        txt += _("total sitemaps") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_sitemaps)
        txt += "</td></tr><tr><td>"
        txt += _("sitemaps free of error") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_sitemaps_uri_ok)
        txt += "</td></tr><tr><td>"
        txt += _("sitemaps not found") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_sitemaps_uri_404)
        txt += "</td></tr><tr><td>"
        txt += _("sitemaps not in sync") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_sitemaps_checksum_error)
        txt += "</td></tr><tr><td></td><td></td></tr><tr><td>"
        #
        txt += _("other errors") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_global_errors)
        txt += "</td></tr><tr><td>"
        txt += "<b>" + _("Total errors") + "&nbsp;" + "</b>"
        txt += "</td><td>"
        txt += "<b>" + str(total_errors) + "</b>"
        txt += "</td></tr></table><br/><br/>"
        self.signal_main_event.emit(txt)