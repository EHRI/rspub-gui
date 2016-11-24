#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import gettext
import glob
import locale
import logging

import os

from rsapp.gui import wapp
from rsapp.gui.conf import GuiConf

LOG = logging.getLogger(__name__)
DEFAULT_LOCALE = "en-US"


def application_home():
    return wapp.APPLICATION_HOME


def locales():
    return [os.path.basename(x) for x in glob.glob(os.path.join(wapp.LOCALE_DIR, "*-*")) if os.path.isdir(x)]


def set_language(language):
    gettext.translation(wapp.LOCALE_DOMAIN, localedir=wapp.LOCALE_DIR, languages=[language], fallback=True).install()
    config = GuiConf()
    config.set_language(language)
    config.persist()


def system_language():
    loc = locale.getdefaultlocale()

    return DEFAULT_LOCALE if loc is None else loc[0]


def current_language():
    return GuiConf().language(fallback=system_language())


def language_index():
    lan_idx = {}
    languages_file = os.path.join(application_home(), "i18n", "languages.txt")
    try:
        with open(languages_file, "r") as lang_file:
            lines = lang_file.read().splitlines()
            for line in lines:
                (key, val) = line.split(",")
                lan_idx[key] = val
    except Exception as err:
        LOG.warn("Could not reed language index: {0}".format(err))

    return lan_idx








