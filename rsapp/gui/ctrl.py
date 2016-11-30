#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import glob
import json
import locale
import logging
import os

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from rsapp.gui.conf import GuiConf
from rspub.core.config import Configurations
from rspub.core.rs_paras import RsParameters
from rspub.core.selector import Selector

LOG = logging.getLogger(__name__)
LOCALE_DOMAIN = "rspub"
DEFAULT_LOCALE = "en-US"


class Ctrl(QObject):

    switch_language = pyqtSignal(str)
    switch_configuration = pyqtSignal(str)
    switch_tab = pyqtSignal(int)

    def __init__(self, application_home, locale_dir):
        QObject.__init__(self)
        self.application_home = application_home
        self.locale_dir = locale_dir
        self.config = GuiConf()
        self.paras = RsParameters()

    def report_tab_switch(self, index):
        self.switch_tab.emit(index)

    def locales(self):
        return [os.path.basename(x) for x in glob.glob(os.path.join(self.locale_dir, "*-*")) if os.path.isdir(x)]

    def system_language(self):
        loc = locale.getdefaultlocale()
        return DEFAULT_LOCALE if loc is None else loc[0]

    def current_language(self):
        return GuiConf().language(fallback=self.system_language())

    def set_language(self, code):
        gettext.translation(LOCALE_DOMAIN, localedir=self.locale_dir, languages=[code],
                            fallback=True).install()
        self.config.set_language(code)
        self.config.persist()
        self.switch_language.emit(code)

    def iso_lang(self):
        data = {}
        iso_path = os.path.join(self.application_home, "i18n", "iso-lang.json")
        try:
            with open(iso_path, "r") as iso_file:
                data = json.load(iso_file)
        except Exception as err:
            self.warn(_("Could not read iso-lang.json"), err)
        return data

    def load_configuration(self, name):
        try:
            self.paras = RsParameters(config_name=name)
            self.switch_configuration.emit(name)
        except ValueError as err:
            self.error("Unable to load configuration %s" % name, err)

    def save_configuration_as(self, name):
        try:
            self.paras.save_configuration_as(name)
            self.switch_configuration.emit(name)
        except ValueError as err:
            self.error("Unable to save configuration %s" % name, err)

    def reset_configuration(self):
        try:
            self.paras.reset()
            self.switch_configuration.emit(self.paras.configuration_name())
        except Exception as err:
            self.error("Unable to reset parameters.", err)

    def get_selector(self):
        if self.paras.selector_file:
            try:
                selector = Selector(location=self.paras.selector_file)
            except Exception as err:
                self.error("Unable to read selector file '%s." % self.paras.selector_file, err)
                selector = Selector()
        else:
            selector = Selector()
        return selector

    @staticmethod
    def error(msg, cause=None):
        LOG.exception(msg)
        Ctrl.__msg(QMessageBox.Critical, msg, cause)

    @staticmethod
    def warn(msg, cause=None):
        LOG.warning(msg, exc_info=True)
        Ctrl.__msg(QMessageBox.Warning, msg, cause)

    @staticmethod
    def __msg(icon, text, cause=None):
        msg_box = QMessageBox()
        if cause:
            msg_box.setText(_("%s\nCaused by:\n\n%s") % (text, cause))
        else:
            msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.exec()


