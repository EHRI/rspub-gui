#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import logging.config
import os
import sys

from PyQt5.QtWidgets import QApplication

LOG_DIR = "logs"
LOG_FILE = "rspub.log"
CONFIGURATION_DIR = "conf"
LOGGING_CFG_FILE = "logging.conf"

LOCALE_DOMAIN = "rspub"

#: :samp:`The absolute path to the directory that is the application home or root directory.`
#:
#: During run time. So the value shown in documentation is not a constant!
APPLICATION_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#                   rspub-gui         rspub           gui               wapp.py
#: :samp:`The absolute path to the i18n directory.`
LOCALE_DIR = os.path.join(APPLICATION_HOME, "i18n")


class RsApplication(QApplication):

    def __init__(self, *args):
        super().__init__(*args)
        self.logger = logging.getLogger(__name__)
        self.logger.info(_("Starting application"))
        self.logger.info("APPLICATION_HOME=%s" % APPLICATION_HOME)
        self.logger.info("LOCALE_DIR=%s" % LOCALE_DIR)
        self.logger.info(_("Language was set to i18n en-US"))

        from rsapp.gui.wmain import WMain
        self.main_window = WMain()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
        self.logger.info(_("Closing application"))
        self.main_window.close()


if __name__ == '__main__':
    # Start this module from anywhere on the system: append root directory of project.
    sys.path.append(APPLICATION_HOME)

    # create log directory
    log_dir = os.path.join(APPLICATION_HOME, LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, LOG_FILE)
    # configure logging
    log_conf = os.path.join(APPLICATION_HOME, CONFIGURATION_DIR, LOGGING_CFG_FILE)
    logging.config.fileConfig(log_conf, defaults={"log_file": log_file})

    # set an initial language
    from rsapp.gui import utils
    language = utils.current_language()
    gettext.translation(LOCALE_DOMAIN, localedir=LOCALE_DIR, languages=[language], fallback=True).install()

    # instantiate the application
    app = RsApplication(sys.argv)
    # start the application
    sys.exit(app.exec_())
