#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style
from rsapp.gui.widgets import ParaLine, ParaWidget, WorkWidget, Answer
from rspub.core.rs_paras import RsParameters
from rspub.core.transport import Transport
from rspub.util.observe import EventObserver

LOG = logging.getLogger(__name__)


class ExportFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl

        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.export_widget = None
        self.export_mode = None
        self.all_resources = False
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
        lbl_color.setStyleSheet(Style.transport_title())
        hbox1 = QHBoxLayout()
        hbox1.addWidget(lbl_color)
        hbox1.addWidget(self.label_title, 1)
        hbox1.setContentsMargins(0, 0, 0, 5)
        vbl_0.addLayout(hbox1)

        grid1 = QGridLayout()
        grid1.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid1.setVerticalSpacing(2)
        grid1.setHorizontalSpacing(2)

        self.lbl_metadata_key = QLabel(self)
        self.lbl_metadata_value = QLabel(self)
        self.lbl_metadata_key.setContentsMargins(5, 1, 5, 1)
        self.lbl_metadata_value.setContentsMargins(5, 1, 5, 1)
        self.lbl_metadata_key.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_metadata_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_metadata_key.setStyleSheet(Style.derived())
        self.lbl_metadata_value.setStyleSheet(Style.derived())
        grid1.addWidget(self.lbl_metadata_key, 2, 1)
        grid1.addWidget(self.lbl_metadata_value, 2, 2)

        self.lbl_last_execution_key = QLabel(self)
        self.lbl_last_execution_value = QLabel(self)
        self.lbl_last_execution_key.setContentsMargins(5, 1, 5, 1)
        self.lbl_last_execution_value.setContentsMargins(5, 1, 5, 1)
        self.lbl_last_execution_key.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_last_execution_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_last_execution_key.setStyleSheet(Style.derived())
        self.lbl_last_execution_value.setStyleSheet(Style.derived())
        grid1.addWidget(self.lbl_last_execution_key, 3, 1)
        grid1.addWidget(self.lbl_last_execution_value, 3, 2)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(grid1)
        hbox2.addStretch(1)
        vbl_0.addLayout(hbox2)
        vbl_0.insertSpacing(2, 25)

        # # scp group
        grid2 = QGridLayout()
        grid2.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid2.setVerticalSpacing(5)
        grid2.setHorizontalSpacing(10)

        self.grp_scp = QGroupBox(_("Transfer files with Secure Copy Protocol (scp)"))
        vbox3 = QVBoxLayout()

        self.para_scp_widgets = {
            "exp_scp_server": ParaLine(self, "exp_scp_server", ParaWidget.str_conv(), grid2, 3, False),
            "exp_scp_port": ParaLine(self, "exp_scp_port", ParaWidget.int_conv(), grid2, 5, False, width=100),
            "exp_scp_user": ParaLine(self, "exp_scp_user", ParaWidget.str_conv(), grid2, 7, False),
            "exp_scp_document_root": ParaLine(self, "exp_scp_document_root", ParaWidget.str_conv(), grid2, 9, False),
        }
        self.lbl_server_path = QLabel(_("server_path_label"))
        self.edt_server_path = QLabel(self.ctrl.paras.server_path())
        self.edt_server_path.setStyleSheet(Style.derived())
        self.edt_server_path.setTextInteractionFlags(Qt.TextSelectableByMouse)
        grid2.addWidget(self.lbl_server_path, 11, 1)
        grid2.addWidget(self.edt_server_path, 11, 2)

        self.grp_scp.setLayout(vbox3)
        vbox3.addLayout(grid2)

        hbox_scp = QHBoxLayout()
        hbox_scp.addStretch(1)
        self.scp_radio_all = QRadioButton(_("Export all resources"))
        self.scp_radio_all.setChecked(False)
        self.scp_radio_latest = QRadioButton(_("Export latest changes"))
        self.scp_radio_latest.setChecked(True)
        hbox_scp.addWidget(self.scp_radio_all)
        hbox_scp.addWidget(self.scp_radio_latest)
        self.scp_button_start = QPushButton(_("Start transfer"))
        self.scp_button_start.clicked.connect(self.on_scp_button_start_clicked)
        hbox_scp.addWidget(self.scp_button_start)
        vbox3.addLayout(hbox_scp)

        vbl_0.addWidget(self.grp_scp)
        vbl_0.insertSpacing(4, 15)

        # # zip group
        grid3 = QGridLayout()
        grid3.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid3.setVerticalSpacing(5)
        grid3.setHorizontalSpacing(10)

        self.grp_zip = QGroupBox(_("Create a .zip file"))
        vbox4 = QVBoxLayout()

        self.para_zip_widgets = {
            "zip_filename": ParaLine(self, "zip_filename", ParaWidget.str_conv(), grid3, 3, browse="SaveFileName")
        }

        self.grp_zip.setLayout(vbox4)
        vbox4.addLayout(grid3)

        hbox_zip = QHBoxLayout()
        hbox_zip.addStretch(1)
        self.zip_radio_all = QRadioButton(_("Zip all resources"))
        self.zip_radio_all.setChecked(False)
        self.zip_radio_latest = QRadioButton(_("Zip latest changes"))
        self.zip_radio_latest.setChecked(True)
        hbox_zip.addWidget(self.zip_radio_all)
        hbox_zip.addWidget(self.zip_radio_latest)
        self.zip_button_start = QPushButton(_("Start creation"))
        self.zip_button_start.clicked.connect(self.on_zip_button_start_clicked)
        hbox_zip.addWidget(self.zip_button_start)
        vbox4.addLayout(hbox_zip)

        vbl_0.addWidget(self.grp_zip)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Export: '%s'") % self.ctrl.paras.configuration_name())
        self.lbl_metadata_key.setText(_("Export based on"))
        self.lbl_last_execution_key.setText(_("last_execution_label"))
        #
        self.grp_scp.setTitle(_("Transfer files with Secure Copy Protocol (scp)"))
        self.lbl_server_path.setText(_("server_path_label"))
        self.scp_radio_all.setText(_("Export all resources"))
        self.scp_radio_latest.setText(_("Export latest changes"))
        self.scp_button_start.setText(_("Start"))
        #
        self.grp_zip.setTitle(_("Create a .zip file"))
        self.zip_radio_all.setText(_("Zip all resources"))
        self.zip_radio_latest.setText(_("Zip latest changes"))
        self.zip_button_start.setText(_("Start"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.label_title.setText(_("Export: '%s'") % self.ctrl.paras.configuration_name())
        self.lbl_metadata_value.setText(self.ctrl.paras.abs_metadata_dir())
        value = self.ctrl.paras.last_execution
        if value is None:
            value = "None"
        self.lbl_last_execution_value.setText(_(value))
        self.edt_server_path.setText(self.ctrl.paras.server_path())
        self.scp_button_start.setEnabled(self.ctrl.paras.last_execution is not None)
        self.zip_button_start.setEnabled(self.ctrl.paras.last_execution is not None)

    def on_switch_tab(self, from_index, to_index):
        if to_index == self.index:
            self.on_switch_configuration()

    def on_scp_button_start_clicked(self):
        self.activate_worker("scp", self.scp_radio_all.isChecked())

    def on_zip_button_start_clicked(self):
        self.activate_worker("zip", self.zip_radio_all.isChecked())

    def activate_worker(self, export_mode, all_resources):
        if self.export_widget:
            self.export_widget.close()
            self.export_widget.destroy()

        self.export_widget = TransportWidget(export_mode, all_resources)
        self.export_widget.work_started.connect(self.on_work_started)
        self.export_widget.work_ended.connect(self.on_work_ended)

    def on_work_started(self):
        self.scp_button_start.setEnabled(False)
        self.zip_button_start.setEnabled(False)

    def on_work_ended(self):
        self.scp_button_start.setEnabled(True)
        self.zip_button_start.setEnabled(True)

    def close(self):
        LOG.debug("ExportFrame closing")
        if self.export_widget:
            self.export_widget.save_dimensions()

    def translatables(self):
        # parameter labels
        _("exp_scp_server_label")
        _("exp_scp_port_label")
        _("exp_scp_user_label")
        _("exp_scp_document_root_label")
        _("server_path_label")
        _("zip_filename_label")


class TransportWidget(WorkWidget):

    def __init__(self, export_mode, all_resources = False):
        WorkWidget.__init__(self, work=export_mode + " " + "Transport", title_style=Style.transport_title())
        self.chk_trial_run.setVisible(False)
        self.export_mode = export_mode
        self.all_resources = all_resources
        _("Transport")

    def on_btn_run_clicked(self):
        password = "secret"
        if self.export_mode == "scp":
            dlg = QInputDialog(self)
            dlg.setInputMode(QInputDialog.TextInput)
            dlg.setWindowTitle(_("Connecting to %s") % self.paras.exp_scp_server)
            dlg.setLabelText(_("Password for %s@%s:") % (self.paras.exp_scp_user, self.paras.exp_scp_server))
            dlg.setTextEchoMode(QLineEdit.Password)
            #dlg.resize(300, 100)
            if dlg.exec_():
                password = dlg.textValue()
            else:
                return

        super(TransportWidget, self).on_btn_run_clicked()
        self.executor_thread = TransportThread(self.paras,
                                               self.export_mode,
                                               self.all_resources,
                                               password,
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


class TransportThread(QThread, EventObserver):

    signal_exception = pyqtSignal(str)
    signal_main_event = pyqtSignal(str)
    signal_minor_event = pyqtSignal(str)
    signal_next_file = pyqtSignal(str)
    ask_confirmation = pyqtSignal(str, str, Answer)
    signal_end_processing = pyqtSignal(RsParameters)

    def __init__(self, paras, mode, all_resources=False, password="secret", parent=None):
        QThread.__init__(self, parent)
        EventObserver.__init__(self)
        self.paras = paras
        self.mode = mode
        self.all_resources = all_resources
        self.password = password
        self.scp_percentage = 0.0
        self.scp_count = 0

    def run(self):
        LOG.debug("Transporter thread started %s" % self)
        self.scp_percentage = 0.0
        self.scp_count = 0
        trans = None
        try:
            trans = Transport(self.paras)
            trans.register(self)
            if self.mode == "scp":
                LOG.debug("Starting transportation in mode scp")
                trans.scp_resources(all_resources=self.all_resources, password=self.password)
            elif self.mode == "zip":
                LOG.debug("Starting transportation in mode zip")
                trans.zip_resources(all_resources=self.all_resources)
            self.signal_end_processing.emit(self.paras)
        except Exception as err:
            LOG.exception("Exception in transport thread:")
            self.signal_exception.emit(_("Exception in transporter thread: {0}").format(err))
        finally:
            if trans:
                trans.unregister(self)

    def pass_inform(self, *args, **kwargs):
        print(">>>>> inform >>>>>>", args, kwargs)

    def pass_confirm(self, *args, **kwargs):
        print(">>>>> confirm >>>>>", args, kwargs)
        return True

    def inform_transport_start(self, *args, **kwargs):
        mode = kwargs["mode"]
        all = kwargs["all_resources"]
        txt = _("Start export. Mode=%s, all resources=%s") % (mode, all)
        self.signal_main_event.emit(txt)

    def inform_start_copy_to_temp(self, *args, **kwargs):
        self.signal_main_event.emit(_("Copy resources and sitemaps to temporary directory..."))

    def inform_copy_resource(self, *args, **kwargs):
        file = kwargs["file"]
        count = kwargs["count_resources"]
        txt = "<code>resource:&nbsp;"
        txt += str(count) + "&nbsp;&nbsp;"
        txt += "<a href=\"file://" + file + "\">" + file + "</a></code>"
        self.signal_minor_event.emit(txt)

    def inform_copy_sitemap(self, *args, **kwargs):
        file = kwargs["file"]
        count = kwargs["count_sitemaps"]
        txt = "<code>sitemap:&nbsp;"
        txt += str(count) + "&nbsp;&nbsp;"
        txt += "<a href=\"file://" + file + "\">" + file + "</a></code>"
        self.signal_minor_event.emit(txt)

    def inform_resource_not_found(self, *args, **kwargs):
        resource = kwargs["file"]
        txt = _("Resource not found: ")
        txt += resource
        self.signal_exception.emit(txt)

    def inform_site_map_not_found(self, *args, **kwargs):
        sitemap = kwargs["file"]
        txt = _("Sitemap not found: ")
        txt += sitemap
        self.signal_exception.emit(txt)

    def inform_zip_resources(self, *args, **kwargs):
        self.signal_next_file.emit("")
        zip_file = kwargs["zip_file"]
        zip_dir = os.path.dirname(zip_file)
        zip = os.path.basename(zip_file)
        txt = _("Creating zip file: ")
        txt += "<a href=\"file://" + zip_dir + "\">" + zip_dir + "</a>"
        txt += os.path.sep + zip
        txt += "<br/>"
        txt += _("This may take a while ....")
        self.signal_main_event.emit(txt)

    def inform_scp_exception(self, *args, **kwargs):
        exception = kwargs["exception"]
        txt = "SCP exception: "
        txt += exception
        self.signal_exception.emit(txt)

    def inform_ssh_client_creation(self, *args, **kwargs):
        # server, port, user
        txt = _("Creating ssh client. ")
        txt += "  server: " + kwargs["server"]
        txt += "  port: " + str(kwargs["port"])
        txt += "  user: " + kwargs["user"]
        self.signal_main_event.emit(txt)

    def inform_scp_resources(self, *arga, **kwargs):
        command = kwargs["command"]
        txt = _("Transfering files: ")
        txt += command
        self.signal_main_event.emit(txt)

    def inform_scp_progress(self, *args, **kwargs):
        filename = kwargs["filename"]
        size = kwargs["size"]
        sent = kwargs["sent"]
        perc = sent / size
        percstr = "{:.0%}".format(perc).rjust(5)
        total_perc = "{:.0%}".format(self.scp_percentage).rjust(5)
        txt = " | " + total_perc + " | " + percstr + " | " + filename
        self.signal_next_file.emit(txt)

    def inform_scp_transfer_complete(self, *args, **kwargs):
        filename = kwargs["filename"]
        count_resources = kwargs["count_resources"]
        count_sitemaps = kwargs["count_sitemaps"]
        tot_files = count_resources + count_sitemaps
        self.scp_count = kwargs["count_transfers"]
        self.scp_percentage = kwargs["percentage"]
        txt = "<code>transferred:&nbsp;"
        txt += str(self.scp_count) + "/" + str(tot_files) + "&nbsp;&nbsp;"
        txt += filename
        txt += "</code>"
        self.signal_minor_event.emit(txt)

    def inform_transport_end(self, *args, **kwargs):
        count_resources = kwargs["count_resources"]
        count_sitemaps = kwargs["count_sitemaps"]
        count_transfers = kwargs["count_transfers"]
        count_errors = kwargs["count_errors"]
        mode = kwargs["mode"]
        txt = "<hr>"
        txt += _("End export. Mode=%s") % mode
        txt += "<table>"
        txt += "<tr><td>"
        txt += _("resources") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_resources)
        txt += "</td></tr><tr><td>"
        txt += _("sitemaps") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_sitemaps)
        txt += "</td></tr><tr><td>"
        txt += _("transfers") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_transfers)
        txt += "</td></tr><tr><td>"
        txt += _("errors") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_errors)
        txt += "</td></tr></table><br/><br/>"
        self.signal_main_event.emit(txt)

    def confirm_copy_file(self, *args, **kwargs):
        self.signal_next_file.emit(kwargs["filename"])
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()

    def confirm_transfer_file(self, *args, **kwargs):
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()