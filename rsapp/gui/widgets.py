#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

from rsapp.gui.style import Style
from rspub.core.rs_enum import Strategy


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

    @staticmethod
    def str_conv():
        return ParaWidget.str2tx, ParaWidget.tx2str

    @staticmethod
    def int_conv():
        return ParaWidget.int2tx, ParaWidget.tx2int


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
        if self.browse == "SaveFileName":
            filename = QFileDialog.getSaveFileName(self.parent(), _(self.name + "_label"),
                                                        getattr(self.paras, self.name))
            if filename[0] != "":
                self.edit.setText(filename[0])
        else:
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

