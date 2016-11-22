#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import logging.config
import os
import sys
from PyQt5.QtWidgets import QApplication

#: :samp:`The absolute path to the directory that is the application home or root directory.`
#:
#: During run time. So the value shown in documentation is not a constant!
APPLICATION_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
#                   rspub-gui         rspub           gui               app.py
# Start this module from anywhere on the system: append root directory of project.
sys.path.append(APPLICATION_HOME)
#: :samp:`The absolute path to the locale directory.`
LOCALE_DIR = os.path.join(APPLICATION_HOME, "locale")

#_ = gettext.gettext
#_ = lambda s: s


class RsApplication(QApplication):

    def __init__(self, *args):
        super().__init__(*args)
        self.log = logging.getLogger(__name__)
        self.log.info(_("Starting application"))
        self.log.info(_("Started i18n"))


if __name__ == '__main__':
    # start logging
    log_dir = os.path.join(APPLICATION_HOME, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "rspub.log")
    log_conf = os.path.join(APPLICATION_HOME, "conf", "logging.conf")
    logging.config.fileConfig(log_conf, defaults={"log_file": log_file})

    # set an initial language
    from rspub.gui.conf import GuiConf
    language = GuiConf().language(fallback="fr-FR")
    gettext.translation('rspub', localedir=LOCALE_DIR, languages=[language]).install()

    # start the application
    app = RsApplication(sys.argv)
