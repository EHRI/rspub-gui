#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from rsapp.gui.style import Style
from rspub.core.rs_enum import Strategy

LOG = logging.getLogger(__name__)


class ParaWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.accepted = True

    def on_switch_language(self):
        raise NotImplementedError

    def on_switch_configuration(self):
        raise NotImplementedError

    def is_accepted(self):
        return self.accepted


class ParaLine(ParaWidget):

    def __init__(self, parent, name, conv, grid, ordinal, browse=False, width=None):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.v2tx = conv[0]
        self.tx2v = conv[1]
        self.grid = grid
        self.ordinal = ordinal
        self.browse = browse

        self.label = QLabel(self)
        self.edit = QLineEdit()
        if width:
            self.edit.setFixedWidth(width)
        self.button = QPushButton()
        self.err_label = QLabel(self)
        self.err_label.setStyleSheet(Style.error())
        self.err_label.setVisible(False)

        self.edit.textChanged.connect(self.parameter_changed)
        self.edit.editingFinished.connect(self.parameter_finished)
        self.button.clicked.connect(self.button_clicked)

        grid.addWidget(self.label, ordinal, 1)
        grid.addWidget(self.edit, ordinal, 2)
        if self.browse:
            grid.addWidget(self.button, ordinal, 3)
        grid.addWidget(self.err_label, ordinal + 1, 1, 1, 3)

        self.on_switch_language()
        self.on_switch_configuration()

    def parameter_changed(self, text):
        try:
            value = self.tx2v(text)
            setattr(self.paras, self.name, value)
            self.accepted = True
            self.err_label.setText("")
            self.err_label.setVisible(False)
            self.edit.setStyleSheet(Style.default())
            self.label.setStyleSheet(Style.default())
            self.edit.setToolTip(None)
        except ValueError as err:
            self.accepted = False
            self.err_label.setText(str(err))
            self.err_label.setVisible(True)
            self.edit.setStyleSheet(Style.error())
            self.label.setStyleSheet(Style.error())

    def parameter_finished(self):
        try:
            value = self.tx2v(self.edit.text())
            setattr(self.paras, self.name, value)
            self.paras.save_configuration()
            self.accepted = True
            self.err_label.setText("")
            self.err_label.setVisible(False)
            value = self.v2tx(getattr(self.paras, self.name))
            self.edit.setText(value)
            self.edit.setStyleSheet(Style.default())
            self.label.setStyleSheet(Style.default())
        except ValueError as err:
            self.accepted = False
            self.err_label.setText(str(err))
            self.err_label.setVisible(True)
            self.edit.setStyleSheet(Style.error())
            self.label.setStyleSheet(Style.error())

    def button_clicked(self):
        self.edit.setFocus()
        filename = QFileDialog.getExistingDirectory(self.parent(), _(self.name + "_label"),
                                                    getattr(self.paras, self.name))
        if filename != "":
            self.edit.setText(filename)

    def on_switch_language(self):
        self.label.setText(_(self.name + "_label"))
        self.button.setText(_("Browse"))

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        value = self.v2tx(getattr(self.paras, self.name))
        self.edit.setText(value)


class ParaCheck(ParaWidget):

    def __init__(self, parent, name, grid, ordinal):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.check = QCheckBox("", self)
        self.check.setFixedHeight(25)
        self.check.toggled.connect(self.on_toggled)
        grid.addWidget(self.check, ordinal, 2)

        self.on_switch_language()
        self.on_switch_configuration()

    def on_toggled(self, checked):
        if checked != getattr(self.paras, self.name):
            setattr(self.paras, self.name, checked)
            # link paras.is_saving_sitemaps to 'trial run' on ExecuteWidget Frame:
            self.ctrl.update_configuration(self.paras)

    def on_switch_language(self):
        self.check.setText(_(self.name + "_label"))

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        self.check.setChecked(getattr(self.paras, self.name))


class ParaStrategyDrop(ParaWidget):

    def __init__(self, parent, name, grid, ordinal):
        ParaWidget.__init__(self, parent)
        self.name = name
        self.label = QLabel(self)
        self.combo = QComboBox(self)
        self.combo.activated.connect(self.on_activated)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.combo)
        hbox.addStretch(1)

        grid.addWidget(self.label, ordinal, 1)
        grid.addLayout(hbox, ordinal, 2)

        self.on_switch_language()
        self.on_switch_configuration()

    def on_activated(self):
        setattr(self.paras, self.name, self.combo.currentData())
        self.paras.save_configuration()

    def on_switch_language(self):
        self.label.setText(_(self.name + "_label"))
        self.combo.clear()
        for i in range(len(Strategy.names())):
            strategy = Strategy.strategy_for(i)
            self.combo.addItem(_(str(strategy)), strategy.name)

    def on_switch_configuration(self):
        self.paras = self.ctrl.paras
        strategy = getattr(self.paras, self.name)
        self.combo.setCurrentIndex(strategy.value)


class ConfigureFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.switch_language.connect(self.on_switch_language)
        self.ctrl.switch_configuration.connect(self.on_switch_configuration)
        self.paras = self.ctrl.paras
        self.init_ui()
        self.on_switch_language(self.ctrl.current_language())

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)

        self.label_title = QLabel(self)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setContentsMargins(2, 5, 5, 7)
        self.label_title.setStyleSheet(Style.h2())
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_title, 1)
        hbox.setContentsMargins(0, 0, 0, 5)
        grid.addLayout(hbox, 1, 1, 1, 3)

        str_conv = (self.str2tx, self.tx2str)
        int_conv = (self.int2tx, self.tx2int)

        self.para_widgets = {
            "resource_dir": ParaLine(self, "resource_dir", str_conv, grid, 3, True),
            "metadata_dir": ParaLine(self, "metadata_dir", str_conv, grid, 5, False),
            "description_dir": ParaLine(self, "description_dir", str_conv, grid, 7, True),
            "plugin_dir": ParaLine(self, "plugin_dir", str_conv, grid, 9, True),
            "url_prefix": ParaLine(self, "url_prefix", str_conv, grid, 11, False),
            "strategy": ParaStrategyDrop(self, "strategy", grid, 13),
            "max_items_in_list": ParaLine(self, "max_items_in_list", int_conv, grid, 15, False, 100),
            "zero_fill_filename": ParaLine(self, "zero_fill_filename", int_conv, grid, 17, False, 100),
            "is_saving_pretty_xml": ParaCheck(self, "is_saving_pretty_xml", grid, 19),
            "is_saving_sitemaps": ParaCheck(self, "is_saving_sitemaps", grid, 20),
            "has_wellknown_at_root": ParaCheck(self, "has_wellknown_at_root", grid, 21)
        }

        self.button_reset = QPushButton(_("Reset"), self)
        self.button_reset.clicked.connect(self.on_button_reset_clicked)
        grid.addWidget(self.button_reset, 22, 3)

        vbl_0.addLayout(grid)
        vbl_0.addStretch(1)
        self.setLayout(vbl_0)

    def on_switch_language(self, code=None):
        LOG.debug("Switch language: %s" % code)
        self.label_title.setText(_("Configure parameters: '%s'") % self.paras.configuration_name())

    def on_switch_configuration(self, name=None):
        LOG.debug("Switch configuration: %s" % name)
        self.paras = self.ctrl.paras
        self.label_title.setText(_("Configure parameters: '%s'") % self.paras.configuration_name())

    def on_button_reset_clicked(self):
        msg_box = QMessageBox()
        msg_box.setText(_("Reset current parameters"))
        msg_box.setInformativeText(_("Reset '%s' parameters to default values?") % self.paras.configuration_name())
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.No| QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        exe = msg_box.exec()
        if exe == QMessageBox.Yes:
            self.ctrl.reset_configuration()

    def count_errors(self):
        return len([p for p in self.para_widgets.values() if not p.is_accepted()])

    def on_about_to_change(self, window_title):
        ok_to_change = True
        error_count = self.count_errors()
        if error_count > 0:
            msg_box = QMessageBox()
            msg_box.setText(window_title)
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

    @staticmethod
    def str2tx(x):
        return x

    @staticmethod
    def tx2str(x):
        return x

    @staticmethod
    def int2tx(x):
        return str(x)

    @staticmethod
    def tx2int(x):
        return int(x)

    def translatables(self):
        # parameter labels
        _("resource_dir_label")
        _("metadata_dir_label")
        _("description_dir_label")
        _("plugin_dir_label")
        _("url_prefix_label")
        _("strategy_label")
        _("max_items_in_list_label")
        _("zero_fill_filename_label")
        _("is_saving_pretty_xml_label")
        _("is_saving_sitemaps_label")
        _("has_wellknown_at_root_label")






