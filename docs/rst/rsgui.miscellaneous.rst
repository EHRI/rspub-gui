Miscellaneous
=============

.. contents:: Various other items concerning :term:`Metadata Publishing Tool`
    :depth: 1
    :local:
    :backlinks: top

Reporting issues
++++++++++++++++
Issues, bugs, crashes, unwanted or unexpected behavior of the :term:`MPT` application can be reported at
gitHub' `rspub-gui issues <https://github.com/EHRI/rspub-gui/issues/new>`_. If relevant, please include the
latest log file.

Log file location
+++++++++++++++++
The :term:`MPT` application is creating log files. The log file location for various operating systems can be found
in the table below.

===================== ==================================================
Operating System      Log file location
===================== ==================================================
**Windows**           ``{user home}\AppData\Local\rspub\logs\rspub.log``
**Mac OS and Linux**  ``{user home}/.config/rspub/logs/rspub.log``
**Other**             ``{user home}/rspub/logs/rspub.log``
===================== ==================================================

Contributing a language
+++++++++++++++++++++++
The :term:`MPT`-team appreciates if you can and will contribute a translation of the text on buttons, menus and
descriptions in the :term:`MPT` application. Here is how to.

1.  Download and install the free Poedit application from `https://poedit.net/download <https://poedit.net/download>`_.
2.  The ``rspub.pot`` template file contains the original entries in English. Download the ``rspub.pot`` template file.
    *   Go to https://raw.githubusercontent.com/EHRI/rspub-gui/master/i18n/rspub.pot
    *   Right-click on the page and choose ``Save as`` from the popup menu.
3.  Start Poedit and on the Welcome page click ``Create New Translation``.
4.  Choose the ``rspub.pot`` template file you downloaded in step 2.
5.  Choose language (and region) for the translation you want to contribute.

Start translating. Choose an entry in the top panel. Enter tour translation in the text area below. The Poedit
application may give suggestions on the right-most side panel.

Save your translation as a `*.po` file and `contact <https://github.com/EHRI/rspub-gui/issues/new>`_ the
EHRI-team on how to send in your translation.

Alternatively you may clone the GitHub repository and issue a pull request for your translation.







