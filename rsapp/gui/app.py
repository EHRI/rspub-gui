#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import locale
import logging.config
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen

LOG_DIR = "logs"
LOG_FILE = "rspub.log"
CONFIGURATION_DIR = "conf"
LOGGING_CFG_FILE = "logging.conf"
LOCALE_DOMAIN = "rspub"
DEFAULT_LOCALE = "en-US"

#: :samp:`The absolute path to the directory that is the application home or root directory.`
#:
#: During run time. So the value shown in documentation is not a constant!
APPLICATION_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#                   rspub-gui         rspub           gui               wapp.py
#: :samp:`The absolute path to the i18n directory.`
LOCALE_DIR = os.path.join(APPLICATION_HOME, "i18n")


def system_language():
    loc = locale.getdefaultlocale()
    return DEFAULT_LOCALE if loc is None else loc[0]


def current_language():
    from rsapp.gui.conf import GuiConf
    return GuiConf().language(fallback=system_language())


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
    language = current_language()
    trls = gettext.translation(LOCALE_DOMAIN, localedir=LOCALE_DIR, languages=[language], fallback=True)
    trls.install("gettext")

    from rsapp.gui.wapp import RsApplication
    application = RsApplication(sys.argv, application_home=APPLICATION_HOME, locale_dir=LOCALE_DIR)

    from rsapp.gui.conf import GuiConf
    if GuiConf().show_splash():
        # Create and display the splash screen
        splash_pix = QPixmap(os.path.join(APPLICATION_HOME, 'rsapp/img/splash.png'))
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        splash.finish(application.main_window)
        #

    # start the application
    application.main_window.show()
    sys.exit(application.exec_())


