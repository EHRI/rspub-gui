#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config

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

        self.main_window = WMain()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
        self.logger.info("Closing application")
        self.main_window.close()
        self.logger.info("Closed application")
