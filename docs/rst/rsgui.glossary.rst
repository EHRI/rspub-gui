Glossary
========

.. rubric:: Glossary of terms used in context with :term:`Metadata Publishing Tool`

.. glossary::

    capabilitylist
        A capabilitylist is an xml-document of type :term:`sitemap` that enlists :term:`resourcelist`\ s
        and :term:`changelist`\ s that have links to a particular set of resources.

        .. seealso::

            `Capability List <http://www.openarchives.org/rs/1.1/resourcesync#CapabilityList>`_
                ResourceSync Framework Specification

    changelist
        A changelist is an xml-document of type :term:`sitemap` that enlists resources that have changed since a previous
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

    DANS
        Data Archiving and Networked Services. DANS gives permanent access to digital research resources.
        DANS is an institute of the Dutch Academy KNAW and funding organisation NWO.

        .. seealso::

            `Data Archiving and Networked Services (DANS) <https://dans.knaw.nl/en>`_

    description directory
        The description directory is an existing directory on the (local or networked) filesystem.
        In this directory (a copy of) the document that describes the entire site,
        also known as ``.well-known/resourcesync`` or :term:`source description`
        is expected or will be created. If no description directory is given, the document is expected or will be
        created in the :term:`metadata directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

            `Describing the Source <http://www.openarchives.org/rs/1.1/resourcesync#SourceDesc>`_
                ResourceSync Framework Specification

    destination
        A system that synchronizes itself with a :term:`source`\ 's resources.

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
        Will increment an existing :term:`changelist` with the newly found changes.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    metadata directory
        The name of the directory where generated sitemaps are stored. The value of metadata directory may
        consist of multiple path elements. The metadata directory is always relative to the
        :term:`resource directory`.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    MPT
    Metadata Publishing Tool
        Metadata Publishing Tool (MPT) is an application for publishing resources in conformance with the
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
        Will create a new :term:`changelist` at each synchronization run.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    new resourcelist strategy
        At each synchronization run a completely new :term:`resourcelist` will be generated.

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

    scp
        Secure Copy Protocol. SCP copies files over a secure, encrypted network connection.

        .. seealso::

            `Linux and Unix scp command <http://www.computerhope.com/unix/scp.htm>`_

    set of resources
        "A collection of resources that is made available for :term:`synchronization` by a :term:`source`\.
        A source may expose one or more such collections and support distinct ResourceSync capabilities for each.
        Individual resources may be included in more than one set of resources"

        -- ResourceSync Framework Specification

        .. seealso::

            `Definitions <http://www.openarchives.org/rs/1.1/resourcesync#Definitions>`_
                ResourceSync Framework Specification

    sitemap
    sitemap protocol
        An XML schema for xml-documents that describe the resources of a site.

        .. seealso::

            `Sitemap protocol <https://www.sitemaps.org/protocol.html>`_
                Official site

    source
        A server that hosts resources subject to synchronization.

        .. seealso::

            `Definitions <http://www.openarchives.org/rs/1.1/resourcesync#Definitions>`_
                ResourceSync Framework Specification

    source description
        In the context of :term:`ResourceSync Framework Specification` the document at::

            {server root}/.well-known/resourcesync

        This document describes the site by listing all :term:`capabilitylist`\ s that are available from the site.
        This practice is an extension on the :term:`well-known URI` scheme, also known as RFC5785.

        .. seealso::

            `ResourceSync Well-Known URI <http://www.openarchives.org/rs/1.1/resourcesync#wellknown>`_
                ResourceSync Framework Specification

    strategy
        The strategy defines what kind of sitemap documents will be generated when a synchronization is executed.

        .. seealso::

            :doc:`rsgui.configure`
                Configure page

    synchronization
    synchronize
        Keeping a set of resources
        at a :term:`destination` the same as the set of resources at a :term:`source`.

        As seen from the destination
        this includes copying the original set of resources from the source and then keeping up to date with
        additions to, changes of and deletions from the set of resources at the source.

        As seen from a source this involves providing the resources and the metadata that describe the changes
        to this set of resources.

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
