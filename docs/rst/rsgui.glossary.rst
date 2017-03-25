Glossary
========

.. rubric:: Glossary of terms used in context with :term:`Metadata Publishing Tool`

.. glossary::

    Capability List
        A Capability List is an xml-document of type :term:`sitemap` that enlists :term:`Resource List`\ s
        and :term:`Change List`\ s that contain links to a particular :term:`set of resources`\ .

        .. seealso::

            `Capability List <http://www.openarchives.org/rs/1.1/resourcesync#CapabilityList>`_
                ResourceSync Framework Specification

    Change List
        A Change List is an xml-document of type :term:`sitemap` that enlists :term:`resource`\ s that have changed since a
        previous :term:`synchronization`\ .

        .. seealso::

            `Change List <http://www.openarchives.org/rs/1.1/resourcesync#ChangeList>`_
                ResourceSync Framework Specification

    configuration
        A named set of parameters that constitute all variables needed to :term:`synchronize` a
        :term:`set of resources`\ .
        The first configuration will be saved under the name 'DEFAULT'.
        Configurations can be loaded, saved, listed and deleted under
        the :ref:`File<application-menus-file-label>` menu. The parameters that are set under a configuration
        are automatically saved.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    DANS
        Data Archiving and Networked Services. DANS gives permanent access to digital research :term:`resource`\ s.
        DANS is an institute of the Dutch Academy KNAW and funding organisation NWO.

        .. seealso::

            `Data Archiving and Networked Services (DANS) <https://dans.knaw.nl/en>`_

    description directory
        The description directory is an existing directory on the (local or networked) filesystem.
        In this directory (a copy of) the document that describes the entire site,
        also known as ``.well-known/resourcesync`` or :term:`Source Description`
        is expected or will be created. If no description directory is given, the document is expected or will be
        created in the :term:`metadata directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

            `Describing the Source <http://www.openarchives.org/rs/1.1/resourcesync#SourceDesc>`_
                ResourceSync Framework Specification

    Destination
        A system that :term:`synchronize`\ s itself with a :term:`Source`\ 's :term:`resource`\ s.

        .. seealso::

            `Definitions <http://www.openarchives.org/rs/1.1/resourcesync#Definitions>`_
                ResourceSync Framework Specification

    EAD
        "Encoded Archival Description (..) is a non-proprietary de facto standard for the encoding of finding aids
        for use in a networked (online) environment. Finding aids are inventories, indexes, or guides that are
        created by archival and manuscript repositories to provide information about specific collections.
        While the finding aids may vary somewhat in style, their common purpose is to provide detailed
        description of the content and intellectual organization of collections of archival materials.
        EAD allows the standardization of collection information in finding aids within and across repositories."

        -- The Library of Congress, Official Site

        .. seealso::

            `Encoded Archival Description <https://www.loc.gov/ead/index.html>`_

    EHRI
        European Holocaust Research Infrastructure.

        "The mission of the European Holocaust Research Infrastructure (EHRI) is to support the Holocaust
        research community by building a digital infrastructure and facilitating human networks."

        -- About EHRI

        .. seealso::

            `European Holocaust Research Infrastructure <https://www.ehri-project.eu/>`_

    incremental changelist strategy
        Will increment an existing :term:`Change List` with the newly found changes.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    metadata directory
        The name of the directory where generated :term:`sitemap`\ s are stored. The value of metadata directory may
        consist of multiple path elements. The metadata directory is always relative to the
        :term:`resource directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    MPT
    Metadata Publishing Tool
        Metadata Publishing Tool (MPT) is an application for publishing :term:`resource`\ s in conformance with the
        :term:`ResourceSync Framework Specification`.
        Metadata Publishing Tool was developed by
        Data Archiving and Networked Services (:term:`DANS`\ -KNAW) under auspices of the
        European Holocaust Research Infrastructure (:term:`EHRI`).

        .. seealso::

            `rspub-core at gitHub <https://github.com/EHRI/rspub-core>`_
                The base library under MPT

            `rspub-gui at gitHub <https://github.com/EHRI/rspub-gui>`_
                The source code of the graphical user interface under MPT

    new changelist strategy
        Will create a new :term:`Change List` at each :term:`synchronization` run.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    new resourcelist strategy
        At each :term:`synchronization` run a completely new :term:`Resource List` will be generated.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    plugin directory
        In this directory or its subdirectories a search for plugins will be conducted.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

            `ResourceGateBuilder <http://rspub-core.readthedocs.io/en/latest/rst/rspub.pluggable.gate.html#resource-gate-builder>`_
                Documentation on rspub-core

    resource
        In web technology, a data resource is anything that can be accessed with a link. It can for instance
        be a file, (part of) a database or the output of a program.

    resource directory
        The base directory on the (local or networked) filesystem where :term:`resource`\ s that should
        be :term:`synchronize`\ d are stored. The resource directory
        should be chosen careful, because it influences the composition of the URL to the :term:`resource`\ .

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    Resource List
        A Resource List is an xml-document of type :term:`sitemap` that enlists available :term:`resource`\ s on a particular site.

        .. seealso::

            `Resource List <http://www.openarchives.org/rs/1.1/resourcesync#ResourceList>`_
                ResourceSync Framework Specification

    ResourceSync
    ResourceSync Framework Specification
        The ResourceSync specification describes a :term:`synchronization` framework for the web consisting of various
        capabilities that allow third-party systems to remain :term:`synchronize`\ d with a server's evolving :term:`resource`\ s.

        .. seealso::

            `ResourceSync Framework Specification <http://www.openarchives.org/rs/resourcesync>`_
                Open Archives Initiative ResourceSync Framework Specification

    scp
        Secure Copy Protocol. SCP copies files over a secure, encrypted network connection.

        .. seealso::

            `Linux and Unix scp command <http://www.computerhope.com/unix/scp.htm>`_

    set of resources
        "A collection of :term:`resource`\ s that is made available for :term:`synchronization` by a :term:`Source`\.
        A :term:`Source` may expose one or more such collections and support distinct ResourceSync capabilities for each.
        Individual :term:`resource`\ s may be included in more than one set of :term:`resource`\ s"

        -- ResourceSync Framework Specification

        .. seealso::

            `Definitions <http://www.openarchives.org/rs/1.1/resourcesync#Definitions>`_
                ResourceSync Framework Specification

    sitemap
    sitemap protocol
        An XML schema for xml-documents that describe the :term:`resource`\ s of a site. The
        :term:`ResourceSync Framework Specification` makes use of this protocol to express the location of :term:`resource`\ s
        and to express changes that affected this :term:`set of resources`\ . ResourceSync specifies these
        sitemaps:

        - `Source Description <http://www.openarchives.org/rs/1.1/resourcesync#SourceDesc>`_ enumerates the :term:`Capability List`\ s offered by a :term:`Source`
        - `Capability List <http://www.openarchives.org/rs/1.1/resourcesync#CapabilityList>`_ enumerates all capabilities supported by a :term:`Source` for a specific :term:`set of resources`
        - `Resource List <http://www.openarchives.org/rs/1.1/resourcesync#ResourceList>`_ lists and describes the :term:`resource`\ s that a :term:`Source` makes available for :term:`synchronization`
        - `Resource List Index <http://www.openarchives.org/rs/1.1/resourcesync#ResourceListIndex>`_ for grouping multiple :term:`Resource List`\ s
        - `Resource Dump <http://www.openarchives.org/rs/1.1/resourcesync#ResourceDump>`_ used to transfer :term:`resource`\ s from the :term:`Source` in bulk
        - `Resource Dump Manifest <http://www.openarchives.org/rs/1.1/resourcesync#ResourceDumpManifest>`_ describes the bulk package's constituents
        - `Change List <http://www.openarchives.org/rs/1.1/resourcesync#ChangeList>`_ contains a description of changes to a :term:`Source`\ 's :term:`resource`\ s
        - `Change List Index <http://www.openarchives.org/rs/1.1/resourcesync#ChangeListIndex>`_ for grouping multiple :term:`Change List`\ s
        - `Change Dump <http://www.openarchives.org/rs/1.1/resourcesync#ChangeDump>`_ used to transfer changed :term:`resource`\ s from the :term:`Source` in bulk
        - `Change Dump Manifest <http://www.openarchives.org/rs/1.1/resourcesync#ChangeDumpManifest>`_ describes the bulk package's constituents

        .. seealso::

            `Sitemap protocol <https://www.sitemaps.org/protocol.html>`_
                Official site

    Source
        A server that hosts :term:`resource`\ s subject to :term:`synchronization`\ .

        .. seealso::

            `Definitions <http://www.openarchives.org/rs/1.1/resourcesync#Definitions>`_
                ResourceSync Framework Specification

    Source Description
        In the context of :term:`ResourceSync Framework Specification` the document at::

            {server root}/.well-known/resourcesync

        This document describes the site by listing all :term:`Capability List`\ s that are available from the site.
        This practice is an extension on the :term:`well-known URI` scheme, also known as RFC5785.

        .. seealso::

            `ResourceSync Well-Known URI <http://www.openarchives.org/rs/1.1/resourcesync#wellknown>`_
                ResourceSync Framework Specification

    strategy
        The strategy defines what kind of :term:`sitemap` documents will be generated when
        a :term:`synchronization` is executed.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    synchronization
    synchronize
        Keeping a :term:`set of resources`
        at a :term:`Destination` the same as the :term:`set of resources` at a :term:`Source`\ .

        As seen from the :term:`Destination`
        this includes copying the original :term:`set of resources` from the :term:`Source` and then keeping up to date with
        additions to, changes of and deletions from the :term:`set of resources` at the :term:`Source`\ .

        As seen from a :term:`Source` this involves providing the :term:`resource`\ s and the metadata that describe the changes
        to this :term:`set of resources`\ .

        .. seealso::

            `Source perspective <http://www.openarchives.org/rs/1.1/resourcesync#SourcePers>`_
                ResourceSync Framework Specification
            `Destination perspective <http://www.openarchives.org/rs/1.1/resourcesync#DestPers>`_
                ResourceSync Framework Specification

    trial run
        The execution of a :term:`synchronization` run that will not write :term:`sitemap`\ s to disk.

        .. seealso::

            :ref:`config-save-sitemap-to-disk-label`

            :ref:`execute-synchronise-resources-label`

    URL prefix
        The URL prefix is the basename of the site, optionally followed by a path segment.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    well-known URI
        RFC5785. An internet standard that defines a path prefix for "well-known locations"

        .. seealso::

            `RFC5785 specification <https://www.ietf.org/rfc/rfc5785.txt>`_
