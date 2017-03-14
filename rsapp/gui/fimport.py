#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QThread
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
from PyQt5.QtWidgets import QVBoxLayout

from rsapp.gui.style import Style
from rsapp.gui.widgets import ParaLine, ParaWidget, WorkWidget, Answer
from rspub.core.importer import Importer
from rspub.core.rs_paras import RsParameters
from rspub.util.observe import EventObserver

LOG = logging.getLogger(__name__)


class ImportFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl

        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.ctrl.switch_tab.connect(self.on_switch_tab)
        self.import_widget = None

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
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.label_title, 1)
        hbox1.setContentsMargins(0, 0, 0, 5)
        vbl_0.addLayout(hbox1)
        vbl_0.insertSpacing(2, 25)

        # # scp group
        grid1 = QGridLayout()
        grid1.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid1.setVerticalSpacing(5)
        grid1.setHorizontalSpacing(10)

        self.grp_scp = QGroupBox(_("Import files with Secure Copy Protocol (scp)"))
        vbox1 = QVBoxLayout()

        self.para_scp_widgets = {
            "imp_scp_server": ParaLine(self, "imp_scp_server", ParaWidget.str_conv(), grid1, 3, False),
            "imp_scp_port": ParaLine(self, "imp_scp_port", ParaWidget.int_conv(), grid1, 5, False, width=100),
            "imp_scp_user": ParaLine(self, "imp_scp_user", ParaWidget.str_conv(), grid1, 7, False),
            "imp_scp_remote_path": ParaLine(self, "imp_scp_remote_path", ParaWidget.str_conv(), grid1, 9, False),
            "imp_scp_local_path": ParaLine(self, "imp_scp_local_path", ParaWidget.str_conv(), grid1, 11, True),
        }

        self.grp_scp.setLayout(vbox1)
        vbox1.addLayout(grid1)

        hbox_scp = QHBoxLayout()
        hbox_scp.addStretch(1)
        self.scp_button_start = QPushButton(_("Start"))
        self.scp_button_start.clicked.connect(self.on_scp_button_start_clicked)
        hbox_scp.addWidget(self.scp_button_start)
        vbox1.addLayout(hbox_scp)

        vbl_0.addWidget(self.grp_scp)

        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Import resources"))
        #
        self.grp_scp.setTitle(_("Import files with Secure Copy Protocol (scp)"))
        self.scp_button_start.setText(_("Start"))

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)

    def on_switch_tab(self, from_index, to_index):
        pass

    def on_scp_button_start_clicked(self):
        self.activate_worker()

    def activate_worker(self):
        if self.import_widget:
            self.import_widget.close()
            self.import_widget.destroy()

        self.import_widget = ImportWidget()
        self.import_widget.work_started.connect(self.on_work_started)
        self.import_widget.work_ended.connect(self.on_work_ended)

    def on_work_started(self):
        self.scp_button_start.setEnabled(False)

    def on_work_ended(self):
        self.scp_button_start.setEnabled(True)

    def close(self):
        LOG.debug("ImportFrame closing")
        if self.import_widget:
            self.import_widget.save_dimensions()

    def translatables(self):
        # parameter labels
        _("imp_scp_server_label")
        _("imp_scp_port_label")
        _("imp_scp_user_label")
        _("imp_scp_remote_path_label")
        _("imp_scp_local_path_label")


class ImportWidget(WorkWidget):

    def __init__(self):
        WorkWidget.__init__(self, work="Import", title_style=Style.import_title())
        self.chk_trial_run.setVisible(False)
        _("Import")

    def on_btn_run_clicked(self):
        password = "secret"
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setWindowTitle(_("Connecting to %s") % self.paras.imp_scp_server)
        dlg.setLabelText(_("Password for %s@%s:") % (self.paras.imp_scp_user, self.paras.imp_scp_server))
        dlg.setTextEchoMode(QLineEdit.Password)
        if dlg.exec_():
            password = dlg.textValue()
        else:
            return

        super(ImportWidget, self).on_btn_run_clicked()
        self.executor_thread = ImportThread(self.paras, password, self)
        self.executor_thread.signal_exception.connect(self.on_signal_exception)
        self.executor_thread.ask_confirmation.connect(self.on_ask_confirmation)
        self.executor_thread.signal_main_event.connect(self.on_signal_main_event)
        self.executor_thread.signal_minor_event.connect(self.on_signal_minor_event)
        self.executor_thread.signal_next_file.connect(self.on_signal_next_file)
        self.executor_thread.signal_end_processing.connect(self.on_signal_end_processing)
        self.executor_thread.finished.connect(self.on_executor_thread_finished)
        self.executor_thread.start()
        self.update()


class ImportThread(QThread, EventObserver):

    signal_exception = pyqtSignal(str)
    signal_main_event = pyqtSignal(str)
    signal_minor_event = pyqtSignal(str)
    signal_next_file = pyqtSignal(str)
    ask_confirmation = pyqtSignal(str, str, Answer)
    signal_end_processing = pyqtSignal(RsParameters)

    def __init__(self, paras, password="secret", parent=None):
        QThread.__init__(self, parent)
        EventObserver.__init__(self)
        self.paras = paras
        self.password = password
        self.scp_count = 0

    def run(self):
        LOG.debug("Importer thread started %s" % self)
        self.scp_count = 0
        importer = None
        try:
            importer = Importer(self.paras, self.password)
            importer.register(self)
            LOG.debug("Starting import")
            importer.scp_get()
            self.signal_end_processing.emit(self.paras)
        except Exception as err:
            LOG.exception("Exception in import thread:")
            self.signal_exception.emit(_("Exception in importer thread: {0}").format(err))
        finally:
            if importer:
                importer.unregister(self)

    def pass_inform(self, *args, **kwargs):
        print(">>>>> inform >>>>>>", args, kwargs)

    def pass_confirm(self, *args, **kwargs):
        print(">>>>> confirm >>>>>", args, kwargs)
        return True

    def inform_import_start(self, *args, **kwargs):
        txt = _("Start import.")
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

    def inform_scp_progress(self, *args, **kwargs):
        filename = kwargs["filename"]
        size = kwargs["size"]
        sent = kwargs["sent"]
        perc = sent / size
        percstr = "{:.0%}".format(perc).rjust(5)
        txt = " | " + percstr + " | " + filename
        self.signal_next_file.emit(txt)

    def inform_scp_transfer_complete(self, *args, **kwargs):
        filename = kwargs["filename"]
        count_imports = kwargs["count_imports"]
        txt = "<code>imported:&nbsp;"
        txt += str(count_imports) + "&nbsp;&nbsp;"
        txt += filename
        txt += "</code>"
        self.signal_minor_event.emit(txt)

    def inform_import_end(self, *args, **kwargs):
        count_imports = kwargs["count_imports"]
        count_errors = kwargs["count_errors"]
        txt = "<hr>"
        txt += _("End import.")
        txt += "<table>"
        txt += "<tr><td>"
        txt += _("imports") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_imports)
        txt += "</td></tr><tr><td>"
        txt += _("errors") + "&nbsp;"
        txt += "</td><td>"
        txt += str(count_errors)
        txt += "</td></tr></table><br/><br/>"
        self.signal_main_event.emit(txt)

    def confirm_transfer_file(self, *args, **kwargs):
        if self.isInterruptionRequested():
            self.signal_exception.emit(_("Process interrupted by user"))
        return not self.isInterruptionRequested()