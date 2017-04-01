#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config
import os
import platform

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from rsapp.gui.ctrl import Ctrl
from rsapp.gui.wmain import WMain


class RsApplication(QApplication):

    def __init__(self, *args, application_home=None, locale_dir=None):
        QApplication.__init__(self, *args)
        self.logger = logging.getLogger(__name__)
        self.ctrl = Ctrl(application_home, locale_dir)

        self.logger.info("Starting application")
        self.logger.info("application_home=%s" % self.ctrl.application_home)
        self.logger.info("locale_dir=%s" % self.ctrl.locale_dir)
        self.logger.info(_("Language was set to locale en-US"))

        opsys = platform.system()
        if opsys == "Windows":
            self.logger.info("Setting Windows-specific values")
            self.setWindowIcon(QIcon(os.path.join(application_home, "conf", "img", "mpt256.ico")))
            import ctypes
            mpt_app_id = "nl.knaw.dans.ehri2.mpt"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(mpt_app_id)

        self.main_window = WMain()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
        self.logger.info("Closing application")
        self.main_window.close()
        self.logger.info("Closed application")
