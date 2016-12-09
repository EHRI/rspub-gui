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
from rspub.core.rs_paras import RsParameters
from rspub.core.selector import Selector

LOG = logging.getLogger(__name__)
LOCALE_DOMAIN = "rspub"
DEFAULT_LOCALE = "en-US"


class Ctrl(QObject):

    switch_language = pyqtSignal(str)
    switch_configuration = pyqtSignal(str)
    switch_selector = pyqtSignal(str)
    switch_tab = pyqtSignal(int, int)
    request_update_selector = pyqtSignal()

    def __init__(self, application_home, locale_dir):
        QObject.__init__(self)
        self.application_home = application_home
        self.locale_dir = locale_dir
        self.config = GuiConf()
        self.last_directory = os.path.expanduser("~")
        try:
            self.paras = RsParameters(config_name=self.config.last_configuration_name())
        except:
            self.paras = RsParameters()
        self.selector = self.__get_selector()

    def report_tab_switch(self, from_index, to_index):
        self.switch_tab.emit(from_index, to_index)

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
            with open(iso_path, "r", encoding="utf-8") as iso_file:
                data = json.load(iso_file)
        except Exception as err:
            self.warn(_("Could not read iso-lang.json"), err)
        return data

    def load_configuration(self, name):
        try:
            self.paras = RsParameters(config_name=name)
            self.selector = self.__get_selector()
            self.switch_configuration.emit(name)
            LOG.debug("Loaded configuration: '%s'" % name)
            self.switch_selector.emit(self.selector.abs_location())
        except ValueError as err:
            self.error("Unable to load configuration %s" % name, err)

    def save_configuration_as(self, name):
        try:
            if self.paras.selector_file:
                selector_dir = os.path.dirname(self.paras.selector_file)
                new_name = os.path.join(selector_dir, name + "-selector.csv")
                self.selector.write(new_name)
                LOG.debug("Saved selector '%s' as '%s'" % (self.paras.selector_file, new_name))
                self.paras.selector_file = new_name
            self.paras.save_configuration_as(name)
            LOG.debug("Saved configuration as '%s'" % name)
            self.switch_configuration.emit(name)
            self.switch_selector.emit(self.selector.abs_location())
        except ValueError as err:
            self.error("Unable to save configuration '%s'" % name, err)

    def reset_configuration(self):
        try:
            self.paras.reset()
            self.selector = self.__get_selector()
            LOG.debug("Configuration was reset")
            self.switch_configuration.emit(self.paras.configuration_name())
            self.switch_selector.emit(self.selector.abs_location())
        except Exception as err:
            self.error("Unable to reset parameters.", err)

    def update_configuration(self, paras):
        self.paras = paras
        self.paras.save_configuration()
        self.selector = self.__get_selector()
        LOG.debug("Configuration updated")
        self.switch_configuration.emit(self.paras.configuration_name())
        self.switch_selector.emit(self.selector.abs_location())

    def __get_selector(self):
        if self.paras.selector_file:
            try:
                selector = Selector(location=self.paras.selector_file)
                self.last_directory = os.path.dirname(self.paras.selector_file)
                LOG.debug("Loaded selector from %s" % self.paras.selector_file)
            except Exception as err:
                self.warn("Unable to read selector file '%s'" % self.paras.selector_file, err)
                selector = Selector()
        else:
            selector = Selector()
        return selector

    def save_selector(self):
        if self.selector.location:
            try:
                self.selector.write()
                LOG.debug("Saved selector as %s" % self.selector.abs_location())
                self.switch_selector.emit(self.selector.abs_location())
            except Exception as err:
                self.warn("Unable to save selector file '%s'" % self.selector.abs_location(), err)

    def save_selector_as(self, filename):
        try:
            self.selector.write(filename)
            LOG.debug("Saved selector as %s" % self.selector.abs_location())
            self.last_directory = os.path.dirname(self.selector.abs_location())
            self.paras.selector_file = filename
            self.paras.save_configuration()
            self.switch_configuration.emit(self.paras.configuration_name())
            self.switch_selector.emit(self.selector.abs_location())
        except Exception as err:
            self.warn("Unable to save selector file as '%s'" % self.selector.abs_location(), err)

    def open_selector(self, filename):
        try:
            self.selector = Selector(filename)
            LOG.debug("Opened selector %s" % self.selector.abs_location())
            self.last_directory = os.path.dirname(self.selector.abs_location())
            self.paras.selector_file = filename
            self.paras.save_configuration()
            self.switch_configuration.emit(self.paras.configuration_name())
            self.switch_selector.emit(self.selector.abs_location())
        except Exception as err:
            self.warn("Unable to open selector file '%s'" % self.selector.abs_location(), err)

    def update_selector(self):
        self.request_update_selector.emit()
        self.selector = self.__get_selector()
        self.switch_selector.emit(self.selector.abs_location())

    def load_selector_includes(self, filename):
        try:
            self.selector.read_includes(filename)
            LOG.debug("Loaded includes %s" % filename)
            self.last_directory = os.path.dirname(filename)
            self.switch_selector.emit(self.selector.abs_location())
        except Exception as err:
            self.warn("Unable to load includes from %s." % filename, err)

    def load_selector_excludes(self, filename):
        try:
            self.selector.read_excludes(filename)
            LOG.debug("Loaded excludes %s" % filename)
            self.last_directory = os.path.dirname(filename)
            self.switch_selector.emit(self.selector.abs_location())
        except Exception as err:
            self.warn("Unable to load excludes from %s." % filename, err)

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


