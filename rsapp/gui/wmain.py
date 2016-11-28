#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTabWidget

from rsapp.gui.conf import GuiConf
from rsapp.gui.fconfigure import ConfigureFrame
from rsapp.gui.fexecute import ExecuteFrame
from rsapp.gui.finspect import InspectFrame
from rsapp.gui.fselect import SelectFrame
from rspub.core.config import Configurations

LOG = logging.getLogger(__name__)

# Menus disappear when the menu text -or its translation- is 'special'
# under MacOs and -
#       self.menubar.setNativeMenuBar(True)
# - .


class WMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.retranslate_ui)
        self.ctrl.switch_configuration.connect(self.reset_paras)
        self.paras = self.ctrl.paras
        self.config = GuiConf()

        self.init_ui()
        self.retranslate_ui()
        self.reset_paras()
        self.show()

    def init_ui(self):
        self.create_menus()

        self.tabframe = TabbedFrame(self)
        self.setCentralWidget(self.tabframe)
        self.resize(self.ctrl.config.window_width(), self.ctrl.config.window_height())


    ####### menu bar ######################################
    def create_menus(self):
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.menu_file = QMenu(_("File"), self)
        self.menubar.addMenu(self.menu_file)

        self.menu_open_config = QMenu(_("Load configuration"), self)
        self.menu_file.addMenu(self.menu_open_config)
        self.config_action_group = QActionGroup(self)
        self.config_action_group.triggered.connect(self.switch_config)
        self.menu_open_config.aboutToShow.connect(self.set_open_config_menu_items)

        self.action_save_configuration_as = QAction(_("Save configuration as..."), self)
        self.menu_file.addAction(self.action_save_configuration_as)
        self.action_save_configuration_as.triggered.connect(self.save_configuration_as)

        self.menu_file.addSeparator()
        self.action_exit = QAction(_("Exit"), self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.triggered.connect(qApp.quit)
        self.menu_file.addAction(self.action_exit)

        self.menu_settings = self.create_menu_settings()
        self.menubar.addMenu(self.menu_settings)

    ####### menus ######################################
    def create_menu_settings(self):
        menu_settings = QMenu(_("Preferences"), self)
        self.menu_language = self.create_menu_language()
        menu_settings.addMenu(self.menu_language)

        return menu_settings

    def create_menu_language(self):
        language_menu = QMenu(_("Language"), self)
        action_group = QActionGroup(self)
        action_group.triggered.connect(self.switch_language)
        iso_idx = self.ctrl.iso_lang()
        current_locale = self.ctrl.current_language()

        for locale in self.ctrl.locales():
            short_locale = locale.split("-")[0]
            if short_locale in iso_idx:
                iso = iso_idx[short_locale]
            else:
                iso = {'nativeName': '-', 'name': '-'}
            action = QAction("%s - %s | %s" % (iso["nativeName"], iso["name"], locale), self)
            action.setCheckable(True)
            action.setData(locale)
            language_menu.addAction(action)
            action_group.addAction(action)
            if locale == current_locale:
                action.setChecked(True)
        return language_menu

    ####### functions #######################################
    def retranslate_ui(self, code=None):
        self.menu_file.setTitle(_("File"))
        self.action_exit.setText(_("Exit"))
        self.action_exit.setStatusTip(_("Exit application"))
        self.menu_open_config.setTitle(_("Load configuration"))
        self.action_save_configuration_as.setText(_("Save configuration as..."))
        self.menu_settings.setTitle(_("Preferences"))
        self.menu_language.setTitle(_("Language"))

    def reset_paras(self, name=None):
        self.paras = self.ctrl.paras
        self.setWindowTitle(self.paras.configuration_name())

    def set_open_config_menu_items(self):
        self.menu_open_config.clear()
        for child in self.config_action_group.children():
            self.config_action_group.removeAction(child)
        current_name = Configurations.current_configuration_name()
        for name in Configurations.list_configurations():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setData(name)
            self. config_action_group.addAction(action)
            self.menu_open_config.addAction(action)
            if name == current_name:
                action.setChecked(True)

    def switch_config(self):
        action_group = self.sender()
        name = action_group.checkedAction().data()
        if self.tabframe.ok_to_change_parameters(_("Switch configuration...")):
            self.ctrl.load_configuration(name)

    def switch_language(self):
        action_group = self.sender()
        locale = action_group.checkedAction().data()
        self.ctrl.set_language(locale)

    def save_configuration_as(self):
        text =  _("Save configuration as...")
        if self.tabframe.ok_to_change_parameters(text):
            name, ok = QInputDialog.getText(self, text, _("Configuration name:"))
            if ok:
                self.ctrl.save_configuration_as(name)

    def close(self):
        LOG.debug("window closing")
        self.ctrl.config.set_window_height(self.height())
        self.ctrl.config.set_window_width(self.width())
        self.ctrl.config.persist()
        self.tabframe.close()


# ################################################################
class TabbedFrame(QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.retranslate_ui)
        self.currentChanged.connect(self.__tabchanged)
        self.previndex = -1
        self.init_ui()

    def init_ui(self):
        self.frame_configure = ConfigureFrame(self)
        self.frame_inspect = InspectFrame(self)
        self.frame_select = SelectFrame(self)
        self.frame_execute = ExecuteFrame(self)

        self.addTab(self.frame_configure, _("Configure"))
        self.addTab(self.frame_inspect, _("Inspect"))
        self.addTab(self.frame_select, _("Select"))
        self.addTab(self.frame_execute, _("Execute"))

    @pyqtSlot(str)
    def retranslate_ui(self, code=None):
        self.setTabText(0, _("Configure"))
        self.setTabText(1, _("Inspect"))
        self.setTabText(2, _("Select"))
        self.setTabText(3, _("Execute"))

    @pyqtSlot(int)
    def __tabchanged(self, index):
        if self.previndex > -1:
            self.widget(self.previndex).hide()

        self.widget(index).show()
        self.previndex = index

    def ok_to_change_parameters(self, text):
        ok_to_change = True
        error_count = self.frame_configure.count_errors()
        if error_count > 0:
            msg_box = QMessageBox()
            msg_box.setText(text)
            i_text = _("Parameters '%s' has %d error(s).") % (self.paras.configuration_name(), error_count)
            i_text += "\n\n"
            i_text += _("Ok to proceed?")
            msg_box.setInformativeText(i_text)
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msg_box.setDefaultButton(QMessageBox.Yes)
            exe = msg_box.exec()
            if exe == QMessageBox.No:
                ok_to_change = False
        return ok_to_change

    def close(self):
        LOG.debug("TabbedFrame closing")
        self.currentWidget().close()


