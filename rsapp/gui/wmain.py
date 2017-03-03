#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtWidgets import QActionGroup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rsapp import version
from rsapp.gui.conf import GuiConf
from rsapp.gui.fconfigure import ConfigureFrame
from rsapp.gui.fexecute import ExecuteFrame
from rsapp.gui.fexport import ExportFrame
from rsapp.gui.fselect import SelectFrame
from rsapp.gui.style import Style
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
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.window_title = (_("Metadata Publishing Tool"))
        self.paras = self.ctrl.paras
        self.config = GuiConf()
        self.init_ui()
        self.on_switch_language()
        self.on_switch_configuration()

    def init_ui(self):
        self.create_menus()
        self.tabframe = TabbedFrame(self)
        self.setCentralWidget(self.tabframe)
        self.about_widget = None
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
        self.config_action_group.triggered.connect(self.on_action_switch_config_triggered)
        self.menu_open_config.aboutToShow.connect(self.on_menu_open_config_about_to_show)

        self.action_save_configuration_as = QAction(_("Save configuration as..."), self)
        self.menu_file.addAction(self.action_save_configuration_as)
        self.action_save_configuration_as.triggered.connect(self.on_action_save_configuration_as_triggered)

        self.action_configurations = QAction(_("Configurations..."), self)
        self.menu_file.addAction(self.action_configurations)
        self.action_configurations.triggered.connect(self.on_action_configurations_triggered)

        self.menu_file.addSeparator()
        self.action_exit = QAction(_("Exit"), self)
        self.action_exit.setShortcut("Ctrl+Q")
        self.action_exit.triggered.connect(self.on_action_exit_triggered)
        self.menu_file.addAction(self.action_exit)

        self.menu_settings = self.create_menu_settings()
        self.menubar.addMenu(self.menu_settings)

        self.menu_window = QMenu(_("Window"), self)
        self.menu_window.aboutToShow.connect(self.on_menu_window_about_to_show)
        self.menubar.addMenu(self.menu_window)
        self.window_action_group = QActionGroup(self)
        self.window_action_group.triggered.connect(self.on_action_switch_window_triggered)
        self.action_about = QAction(_("About..."), self)
        self.action_about.triggered.connect(self.on_action_about_triggered)

    ####### menus ######################################
    def create_menu_settings(self):
        menu_settings = QMenu(_("Preferences"), self)
        self.menu_language = self.create_menu_language()
        menu_settings.addMenu(self.menu_language)

        return menu_settings

    def create_menu_language(self):
        language_menu = QMenu(_("Language"), self)
        action_group = QActionGroup(self)
        action_group.triggered.connect(self.on_action_language_switch_triggered)
        iso_idx = self.ctrl.iso_lang()
        current_locale = self.ctrl.current_language()

        for locale in self.ctrl.locales():
            short_locale = locale.split("-")[0]
            if short_locale in iso_idx:
                iso = iso_idx[short_locale]
            else:
                iso = {'nativeName': '-', 'name': '-'}
            action = QAction("%s - %s  [%s]" % (iso["nativeName"], iso["name"], locale), self)
            action.setCheckable(True)
            action.setData(locale)
            language_menu.addAction(action)
            action_group.addAction(action)
            if locale == current_locale:
                action.setChecked(True)
        return language_menu

    def on_menu_window_about_to_show(self):
        self.menu_window.clear()
        for child in self.window_action_group.children():
            self.window_action_group.removeAction(child)
        for window in QApplication.instance().topLevelWindows():
            if window.type() == 1 and not window.title() == self.windowTitle():
                action = QAction(window.title(), self)
                action.setData(window.title())
                action.setCheckable(True)
                self.window_action_group.addAction(action)
                self.menu_window.addAction(action)

        self.menu_window.addSeparator()
        self.menu_window.addAction(self.action_about)

    ####### functions #######################################
    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.menu_file.setTitle(_("File"))
        self.action_exit.setText(_("Exit"))
        self.action_exit.setStatusTip(_("Exit application"))
        self.menu_open_config.setTitle(_("Load configuration"))
        self.action_save_configuration_as.setText(_("Save configuration as..."))
        self.action_configurations.setText(_("Configurations..."))
        self.action_about.setText(_("About..."))
        self.menu_settings.setTitle(_("Preferences"))
        self.menu_language.setTitle(_("Language"))
        self.window_title = (_("Metadata Publishing Tool"))
        self.setWindowTitle(self.window_title + " [" + self.paras.configuration_name() + "]")

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.setWindowTitle(self.window_title + " [" + self.paras.configuration_name() + "]")

    def on_menu_open_config_about_to_show(self):
        self.menu_open_config.clear()
        for child in self.config_action_group.children():
            self.config_action_group.removeAction(child)
        current_name = Configurations.current_configuration_name()
        for name in Configurations.list_configurations():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setData(name)
            self.config_action_group.addAction(action)
            self.menu_open_config.addAction(action)
            if name == current_name:
                action.setChecked(True)

    def on_action_switch_config_triggered(self):
        action_group = self.sender()
        name = action_group.checkedAction().data()
        if self.tabframe.about_to_change(_("Switch configuration...")):
            self.ctrl.load_configuration(name)

    def on_action_save_configuration_as_triggered(self):
        text =  _("Save configuration as...")
        if self.tabframe.about_to_change(text):
            dlg = QInputDialog(self)
            dlg.setInputMode(QInputDialog.TextInput)
            dlg.setWindowTitle(text)
            dlg.setLabelText(_("Configuration name:"))
            dlg.setTextValue(self.paras.configuration_name())
            dlg.resize(300, 100)
            if dlg.exec_():
                self.ctrl.save_configuration_as(dlg.textValue())

    def on_action_configurations_triggered(self):
        ConfigurationsDialog(self).exec_()

    def on_action_language_switch_triggered(self):
        action_group = self.sender()
        locale = action_group.checkedAction().data()
        self.ctrl.set_language(locale)

    def on_action_switch_window_triggered(self):
        action_group = self.sender()
        window_title = action_group.checkedAction().data()
        for window in QApplication.instance().topLevelWindows():
            if window_title == window.title():
                window.show()
                window.raise_()
                window.requestActivate()

    def on_action_about_triggered(self):
        if self.about_widget is None:
            LOG.debug("Creating About window")
            self.about_widget = AboutWidget(self)
        else:
            self.about_widget.show()
            self.about_widget.setWindowState(Qt.WindowActive)
            self.about_widget.activateWindow()
            self.about_widget.raise_()

    def on_action_exit_triggered(self):
        LOG.debug("action_exit_triggered")
        if self.tabframe.about_to_change(_("Closing application...")):
            qApp.quit()

    def closeEvent(self, event):
        LOG.debug("closeEvent was triggered")
        if self.tabframe.about_to_change(_("Closing application...")):
            LOG.debug("Accepting closeEvent")
            event.accept()
        else:
            LOG.debug("Ignoring closeEvent")
            event.ignore()

    def close(self):
        LOG.debug("window closing")
        self.ctrl.config.set_window_height(self.height())
        self.ctrl.config.set_window_width(self.width())
        self.ctrl.config.set_last_configuration_name(self.paras.configuration_name())
        self.ctrl.config.persist()
        self.tabframe.close()
        if self.about_widget:
            self.about_widget.close()


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
        self.frame_configure = ConfigureFrame(self, 0)
        self.frame_select = SelectFrame(self, 1)
        self.frame_execute = ExecuteFrame(self, 2)
        self.frame_export = ExportFrame(self, 3)

        self.addTab(self.frame_configure, _("Configure"))
        self.addTab(self.frame_select, _("Select"))
        self.addTab(self.frame_execute, _("Execute"))
        self.addTab(self.frame_export, _("Export"))

    @pyqtSlot(str)
    def retranslate_ui(self, code=None):
        self.setTabText(0, _("Configure"))
        self.setTabText(1, _("Select"))
        self.setTabText(2, _("Execute"))
        self.setTabText(3, _("Export"))

    @pyqtSlot(int)
    def __tabchanged(self, index):
        if self.previndex > -1:
            self.widget(self.previndex).hide()

        self.ctrl.report_tab_switch(self.previndex, index)
        self.widget(index).show()
        self.previndex = index

    def about_to_change(self, window_title):
        return self.frame_configure.on_about_to_change(window_title) and \
               self.frame_select.on_about_to_change(window_title)

    def close(self):
        LOG.debug("TabbedFrame closing")
        for i in range(0, self.count()):
            self.widget(i).close()


# ################################################################
class ConfigurationsDialog(QDialog):

    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.ctrl = QApplication.instance().ctrl
        self.__init_ui__()

    def __init_ui__(self):
        self.setWindowTitle(_("Manage configurations"))
        vbox = QVBoxLayout(self)

        list_view = QListView()
        list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        list_view.setAlternatingRowColors(True)
        self.list_model = QStandardItemModel(list_view)
        self.populate_model()
        list_view.setModel(self.list_model)
        self.selection_model = list_view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)
        hbox = QHBoxLayout()
        hbox.addWidget(list_view)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        btn_box = QHBoxLayout()
        self.btn_delete = QPushButton(_("Delete"))
        self.btn_delete.setEnabled(False)
        self.btn_delete.clicked.connect(self.on_btn_delete_clicked)
        btn_box.addWidget(self.btn_delete)

        btn_close = QPushButton(_("Close"))
        btn_close.setDefault(True)
        btn_close.clicked.connect(self.close)
        btn_box.addWidget(btn_close)

        btn_box.addStretch(1)
        vbox.addLayout(btn_box)

        self.setLayout(vbox)

    def populate_model(self):
        self.list_model.clear()
        for cfg in Configurations.list_configurations():
            item = QStandardItem(cfg)
            self.list_model.appendRow(item)

    def on_selection_changed(self, selected=None, deselected=None):
        self.btn_delete.setEnabled(self.selection_model.hasSelection())

    def on_btn_delete_clicked(self):
        items = [x.data() for x in self.selection_model.selectedIndexes()]
        msg_box = QMessageBox()
        msg_box.setText(_("Delete configurations"))
        if len(items) == 1:
            i_text = _("Delete configuration '%s'" % items[0])
        else:
            i_text = _("Delete %d configurations" % len(items))
        i_text += "\n\n"
        i_text += _("Ok to proceed?")
        msg_box.setInformativeText(i_text)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        exe = msg_box.exec()
        if exe == QMessageBox.Yes:
            for item in self.selection_model.selectedIndexes():
                Configurations.remove_configuration(item.data())
            self.populate_model()
            self.on_selection_changed()


class AboutWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)
        self.ctrl = QApplication.instance().ctrl
        self.parent = parent
        self.setWindowTitle("About")
        hbox = QHBoxLayout()
        pic = QLabel(self)
        pix = QPixmap(os.path.join(self.ctrl.application_home, 'conf/img/logo_h.png'))
        pic.setPixmap(pix)
        hbox.addWidget(pic)

        vbox = QVBoxLayout()

        lbl_title = QLabel("Metadata Publishing Tool", self)
        lbl_title.setMinimumWidth(400)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        lbl_title.setFont(font)
        lbl_title.setContentsMargins(2, 5, 5, 7)
        lbl_title.setStyleSheet(Style.h2())
        vbox.addWidget(lbl_title)
        vbox.addSpacing(20)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(2)
        grid.setHorizontalSpacing(2)

        grid.addWidget(QLabel("Version: "), 1, 1)
        grid.addWidget(QLabel(version.__version__), 1,2)

        grid.addWidget(QLabel("Release: "), 2, 1)
        grid.addWidget(QLabel(version.__release_date__), 2, 2)

        hbox_grid = QHBoxLayout()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch(1)
        vbox.addLayout(hbox_grid)

        vbox.addStretch(1)
        txt = QTextBrowser()
        txt.setOpenExternalLinks(True)
        txt.setOpenLinks(False)
        txt.anchorClicked.connect(self.on_anchor_clicked)
        txt.append(version.__about__)
        vbox.addWidget(txt)

        hbox_button = QHBoxLayout()
        hbox_button.addStretch(1)
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.btn_close_clicked)
        hbox_button.addWidget(btn_close)
        vbox.addLayout(hbox_button)

        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)
        self.move(200, 200)

        self.show()

    def on_anchor_clicked(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def btn_close_clicked(self):
        if self.windowState() & Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowMaximized)
        else:
            self.close()
            self.destroy()

    def close(self):
        self.parent.about_widget = None
        super(AboutWidget, self).close()

    def closeEvent(self, event):
        self.close()
        event.accept()