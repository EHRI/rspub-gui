Glossary
========

:samp:`Glossary of terms used in context with {Metadata Publishing Tool}`

.. glossary::

    capabilitylist
        A capabilitylist is an xml-document of type :term:`sitemap` that enlists :term:`resourcelist`\ s
        and :term:`changelist`\ s that have links to a particular set of resources.

        .. seealso::

            `Capability List <http://www.openarchives.org/rs/1.1/resourcesync#CapabilityList>`_
                ResourceSync Framework Specification

    changelist
        A changelis is an xml-document of type :term:`sitemap` that enlists resources that have changed since a previous
        synchronization.

        .. seealso::

            `Change List <http://www.openarchives.org/rs/1.1/resourcesync#ChangeList>`_
                ResourceSync Framework Specification

    configuration
        A named set of parameters that constitute all variables needed to synchronize a set of resources.
        The first configuration will be saved under the name 'DEFAULT'.
        Configurations can be loaded, saved, listed and deleted under
        the :ref:`File<application-menus-file-label>` menu. The parameters that are set under a configuration
        are automatically saved.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    description directory
        The description directory is an existing directory on the (local or networked) filesystem.
        In this directory the document that describes the entire site, also known as ``.well-known/resourcesync``
        is expected or will be created. If no description directory is given, the document is expected or will be
        created in the :term:`metadata directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

            `Decribing the Source <http://www.openarchives.org/rs/1.1/resourcesync#SourceDesc>`_
                ResourceSync Framework Specification

    metadata directory
        The name of the directory where generated sitemaps are stored. The value of metadata directory may
        consist of multiple path elements. The metadata directory is always relative to the
        :term:`resource directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    MPT
    Metadata Publishing Tool
        Metadata Publishing Tool is an application for publishing resources in conformance with the
        :term:`ResourceSync Framework Specification`.
        Metadata Publishing Tool was developed by
        Data Archiving and Networked Services (DANS-KNAW) under auspices of the
        European Holocaust Research Infrastructure (EHRI).

        .. seealso::

            `rspub-core at gitHub <https://github.com/EHRI/rspub-core>`_
                The base library under MPT

            `rspub-gui at gitHub <https://github.com/EHRI/rspub-gui>`_
                The source code of the graphical user interface under MPT

            `Data Archiving and Networked Services (DANS) <https://dans.knaw.nl/en>`_

            `European Holocaust Research Infrastructure (EHRI) <https://www.ehri-project.eu/>`_


    plugin directory
        In this directory or its subdirectories a search for plugins will be conducted.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

            `ResourceGateBuilder <http://rspub-core.readthedocs.io/en/latest/rst/rspub.pluggable.gate.html#resource-gate-builder>`_
                Documentation on rspub-core

    resource directory
        The base directory on the (local or networked) filesystem where resources are stored. The resource directory
        should be chosen careful, because it influences the composition of the URL to the resource.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    resourcelist
        A resourcelist is an xml-document of type :term:`sitemap` that enlists available resources on a particular site.

        .. seealso::

            `Resource List <http://www.openarchives.org/rs/1.1/resourcesync#ResourceList>`_
                ResourceSync Framework Specification

    ResourceSync Framework Specification
        The ResourceSync specification describes a synchronization framework for the web consisting of various
        capabilities that allow third-party systems to remain synchronized with a server's evolving resources.

        .. seealso::

            `ResourceSync Framework Specification <http://www.openarchives.org/rs/resourcesync>`_
                Open Archives Initiative ResourceSync Framework Specification

    sitemap
    sitemap protocol
        An XML schema for xml-documents that describe the resources of a site.

        .. seealso::

            `Sitemap protocol <https://www.sitemaps.org/protocol.html>`_
                Official site

    strategy
        The strategy defines what kind of sitemap documents will be generated when a synchronization is executed.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    URL prefix
        The URL prefix is the basename of the site, optionally followed by a path segment.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page


