#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget

from rsapp.gui import utils
from rsapp.gui.conf import GuiConf
from rsapp.gui.fpref import PreferencesFrame

LOG = logging.getLogger(__name__)


class WMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.config = GuiConf()
        self.init_ui()
        self.retranslate_ui()
        self.show()

    def init_ui(self):
        self.create_actions()
        self.create_menus()



        self.tabframe = TabbedFrame(self)
        self.setCentralWidget(self.tabframe)
        self.resize(self.config.window_width(), self.config.window_height())

    def create_actions(self):
        self.action_exit = QAction(self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.triggered.connect(qApp.quit)

        self.action_open_configuration = QAction(self)
        self.action_open_configuration.setShortcut("Ctrl+O")
        self.action_open_configuration.triggered.connect(self.open_configuration)

    def create_menus(self):
        self.menu_file = self.create_menu_file()
        self.menu_language = self.create_menu_language()

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(True)
        self.menubar.addMenu(self.menu_file)
        self.menubar.addMenu(self.menu_language)

    def create_menu_file(self):
        menu_file = QMenu(self)
        menu_file.addAction(self.action_exit)
        menu_file.addAction(self.action_open_configuration)
        return menu_file

    def create_menu_language(self):
        language_menu = QMenu(self)
        languageActionGroup = QActionGroup(self)
        languageActionGroup.triggered.connect(self.switch_language)
        lang_idx = utils.language_index()
        current_locale = utils.current_language()
        for locale in utils.locales():
            if locale in lang_idx:
                language = lang_idx[locale]
            else:
                language = "-"
            action = QAction(language + " (" + locale + ")", self)
            action.setCheckable(True)
            action.setData(locale)
            language_menu.addAction(action)
            languageActionGroup.addAction(action)
            if locale == current_locale:
                action.setChecked(True)
        return language_menu


    def retranslate_ui(self):
        self.menu_file.setTitle(_("&File"))

        self.action_exit.setText(_("&Exit"))
        self.action_exit.setStatusTip(_("Exit application"))

        self.action_open_configuration.setText(_("&Open configuration"))
        self.action_open_configuration.setStatusTip(_("Open a saved configuration"))

        self.menu_language.setTitle(_("&Language"))

        self.tabframe.retranslate_ui()

    def open_configuration(self):
        LOG.debug("open congig")

    def create_menu(self):

        exit_action = QAction(_("&Exit"), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip(_("Exit application"))
        exit_action.triggered.connect(qApp.quit)

        show_configure_action = QAction(_("&Configure"), self)
        show_configure_action.setShortcut("Ctrl+C")
        show_configure_action.setStatusTip("Configure rsync")
        show_configure_action.triggered.connect(lambda: self.on_tab_choice(0))

        show_export_action = QAction(_("&Export"), self)
        show_export_action.setShortcut("Ctrl+E")
        show_export_action.setStatusTip(_("Export files"))
        show_export_action.triggered.connect(lambda: self.on_tab_choice(1))

        show_statistics_action = QAction(_("&Statistics"), self)
        show_statistics_action.setShortcut("Ctrl+S")
        show_statistics_action.setStatusTip(_("Statistics"))
        show_statistics_action.triggered.connect(lambda: self.on_tab_choice(2))

        show_man_sets_action = QAction(_("&Manual Sets"), self)
        show_man_sets_action.setShortcut("Ctrl+M")
        show_man_sets_action.setStatusTip(_("Manual Sets"))
        show_man_sets_action.triggered.connect(lambda: self.on_tab_choice(3))

        show_rule_based_sets_action = QAction(_("&Rule-based Sets"), self)
        show_rule_based_sets_action.setShortcut("Ctrl+R")
        show_rule_based_sets_action.setStatusTip(_("Rule-based Sets"))
        show_rule_based_sets_action.triggered.connect(lambda: self.on_tab_choice(4))


        self.menubar.setNativeMenuBar(True)

        self.fileMenu = self.menubar.addMenu(_("&File"))
        self.fileMenu.addAction(exit_action)             # on mac under [application] > Quit [application]

        self.viewMenu = self.menubar.addMenu(_("&View"))
        self.viewMenu.addAction(show_configure_action)   # on mac under [application] > Preverences
        self.viewMenu.addAction(show_export_action)
        self.viewMenu.addAction(show_statistics_action)
        self.viewMenu.addAction(show_man_sets_action)
        self.viewMenu.addAction(show_rule_based_sets_action)

        self.tab_actions = list()
        self.tab_actions.append(show_configure_action)      # 0
        self.tab_actions.append(show_export_action)         # 1
        self.tab_actions.append(show_statistics_action)     # 2
        self.tab_actions.append(show_man_sets_action)       # 3
        self.tab_actions.append(show_rule_based_sets_action) # 4

        self.menu_language = self.create_menu_language()
        self.menubar.addMenu(self.menu_language)


    def switch_language(self):
        action_group = self.sender()
        locale = action_group.checkedAction().data()
        utils.set_language(locale)
        self.retranslate_ui()

    # def on_tab_choice(self, tabnr):
    #     self.tabframe.setCurrentIndex(tabnr)
    #     self.set_tab_menu_enabled(tabnr)
    #
    # def set_tab_menu_enabled(self, tabnr):
    #     for action in self.tab_actions:
    #         action.setEnabled(True)
    #     self.tab_actions[tabnr].setEnabled(False)

    def close(self):
        LOG.debug("window closing")
        self.config.set_window_height(self.height())
        self.config.set_window_width(self.width())
        self.config.persist()
        self.tabframe.close()


class TabbedFrame(QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.currentChanged.connect(self.__tabchanged)
        self.previndex = -1
        self.preferencesFrame = PreferencesFrame(self)
        # self.exportframe = ExportFrame(self)
        self.init_ui()

    def __tabchanged(self, index):
        if self.previndex > -1:
            self.widget(self.previndex).hide()

        self.widget(index).show()
        self.previndex = index
        #self.parent.set_tab_menu_enabled(index)

    def init_ui(self):
        LOG.debug("Initializing TabbedFrame")
        # self.addTab(self.configframe, _("&Configuration"))
        # self.addTab(self.exportframe, _("&Export"))

        self.addTab(self.preferencesFrame, _("&Preferences"))


        self.addTab(QWidget(), _("Statistics"))
        self.addTab(QWidget(), _("Manual Sets"))
        self.addTab(QWidget(), _("Rule-based Sets"))

    def retranslate_ui(self):
        self.setTabText(0, _("&Preferences"))
        self.preferencesFrame.retranslate_ui()


    def close(self):
        LOG.debug("TabbedFrame closing")
        self.currentWidget().close()


