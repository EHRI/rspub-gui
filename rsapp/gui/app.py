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


def system_language():
    # # Better to use DEFAULT_LOCALE as fallback because of strange settings in some MacOs versions
    loc = None
    try:
        loc = locale.getdefaultlocale()
    except:
        pass
    return DEFAULT_LOCALE if loc is None else loc[0]


def current_language():
    from rsapp.gui.conf import GuiConf
    return GuiConf().language(fallback=DEFAULT_LOCALE)


def get_logging_directory():
    import platform
    c_path = os.path.expanduser("~")
    opsys = platform.system()
    if opsys == "Windows":
        win_path = os.path.join(c_path, "AppData", "Local")
        if os.path.exists(win_path): c_path = win_path
    elif opsys == "Darwin":
        dar_path = os.path.join(c_path, ".config")
        if not os.path.exists(dar_path): os.makedirs(dar_path)
        if os.path.exists(dar_path): c_path = dar_path
    elif opsys == "Linux":
        lin_path = os.path.join(c_path, ".config")
        if not os.path.exists(lin_path): os.makedirs(lin_path)
        if os.path.exists(lin_path): c_path = lin_path

    c_path = os.path.join(c_path, "rspub", "logs")
    if not os.path.exists(c_path):
        os.makedirs(c_path)
    return c_path


if __name__ == '__main__':

    if getattr(sys, 'frozen', False):
        # running in a bundle
        application_home = sys._MEIPASS
    else:
        application_home = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    # Start this module from anywhere on the system: append root directory of project.
    sys.path.append(application_home)
    print("application_home:", application_home)

    # encoding=utf8

    # create log directory
    log_dir = get_logging_directory()
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, LOG_FILE)
    # For Windows single backslash path names:
    log_file = log_file.replace("\\", "\\\\")
    # configure logging
    log_conf = os.path.join(application_home, CONFIGURATION_DIR, LOGGING_CFG_FILE)
    logging.config.fileConfig(log_conf, defaults={"log_file": log_file})
    # create a logger
    logger = logging.getLogger(__name__)
    logger.debug("Initialized logging: %s", log_file)

    # set an initial language
    locale_dir = os.path.join(application_home, "i18n")
    logger.debug("Locale directory: %s", locale_dir)
    language = current_language()
    logger.debug("Current language: %s", language)
    trls = gettext.translation(LOCALE_DOMAIN, localedir=locale_dir, languages=[language], fallback=True)
    trls.install("gettext")

    from rsapp.gui.wapp import RsApplication
    application = RsApplication(sys.argv, application_home=application_home, locale_dir=locale_dir)

    from rsapp.gui.conf import GuiConf
    if GuiConf().show_splash():
        # Create and display the splash screen
        splash_pix = QPixmap(os.path.join(application_home, 'conf/img/splash.png'))
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        splash.finish(application.main_window)
        #

    # start the application
    application.main_window.show()
    sys.exit(application.exec_())


