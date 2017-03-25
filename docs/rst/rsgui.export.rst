Export resources and sitemaps
=============================

.. contents:: Transfer resources and sitemaps to a web server
    :depth: 1
    :local:
    :backlinks: top

.. figure:: ../img/export/export.png

    *Screenshot of the export page*

.. IMPORTANT::
    The local :term:`synchronization` will not publish your :term:`resource`\ s and :term:`sitemap`\ s. For that,
    :term:`resource`\ s and :term:`sitemap`\ s must be made available on a web server.
    The export page offers two methods to export :term:`resource`\ s and :term:`sitemap`\ s from your local or networked
    drive to your web server:

    - **Transfer files with SCP** - Uses the Secure Copy Protocol (:term:`scp`) to transfer files directly to your webserver.
    - **Create a zip file** - This method creates a zip file of your :term:`resource`\ s and :term:`sitemap`\ s. This you should than hand over to your system administrator who should take care of publishing the contents on the web server.

    There are other ways to publish in conformance with :term:`ResourceSync`. See for this [link to appendix].

The export page shows the current :term:`configuration`, on what metadata the export will be based
and at what date and time the last execution of the :term:`synchronization` took place.

.. figure:: ../img/export/export_02.png

    *Detail of the export page*

.. ATTENTION::
    The outcome of an export may be undecided if you
    switch :term:`configuration`\ s or change parameters on the :doc:`Configuration page <rsgui.configure>`
    in between execution of a :term:`synchronization` and an export. Always export
    :term:`resource`\ s and :term:`sitemap`\ s right after a fresh :term:`synchronization` run.


Transfer files with SCP
+++++++++++++++++++++++

.. figure:: ../img/export/export_03.png

    *Detail of the export page with the SCP parameters*

The parameters for export with :term:`scp` can best be set with the help of a technically skilled person.
These parameters are automatically saved with the current :term:`configuration`.

Server
    The name or IP address of the web server.

Port
    The :term:`scp` port on the web server. Default :term:`scp` port is 22.

User
    The username on the web server.

Document root
    The document root is the folder where the website files for a domain name are stored. With the Apache
    HTTP Server for instance this defaults to ``/var/www/html``.

The `Document path`, relative to the `Document root`, is derived from the :term:`URL prefix` you set on the
:doc:`Configuration page <rsgui.configure>`.


Create a zip file
+++++++++++++++++
