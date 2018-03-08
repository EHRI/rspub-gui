Introduction
============

.. contents:: Introduction to :term:`Metadata Publishing Tool`
    :depth: 1
    :local:
    :backlinks: top

.. img:: ../img/ehri_logo.png
    :scale: 50 %
    :align: centre
    :alt: the EHRI logo

.. note:: **Introducing the EHRI use case**

    "The mission of the European Holocaust Research Infrastructure (:term:`EHRI`) is to support the Holocaust research
    community by building a digital infrastructure and facilitating human networks. :term:`EHRI` provides online access
    to information about dispersed sources relating to the Holocaust through its Online Portal, and tools and
    methods that enable researchers and archivists to collaboratively work with such sources."

    -- `The EHRI web site <https://www.ehri-project.eu/about-ehri>`_

    In order to collect information on dispersed archives across Europe -and the rest of the world- that hold
    Holocaust-related collections the Encoded Archival Description (:term:`EAD`) is used as the format for
    information dissemination; the :term:`ResourceSync` Framework may be used as the transportation
    and :term:`synchronization` mechanism.

    :term:`Metadata Publishing Tool` is the subject of this documentation. Examples in this introduction
    and the rest of the documentation will sometimes use the :term:`EHRI` use case to describe the working of the tool.

ResourceSync
++++++++++++
The :term:`ResourceSync Framework Specification` describes
a :term:`synchronization` framework for the web consisting of various capabilities that allow third-party systems to
remain :term:`synchronize`\ d with a server's evolving :term:`resource`\ s.
More precisely the :term:`ResourceSync` Framework describes the communication between :term:`Source`
and :term:`Destination` aimed at
synchronizing one or more :term:`resource`\ s. Communication utilizes `http` and an extension on
the :term:`sitemap protocol`, an xml-based format for expressing metadata, relevant for :term:`synchronization`.

.. figure:: ../../img/resourcesync.png

    *Fig. 1. External logistics. The ResourceSync Framework Specification at work. Collection Holding Institutions expose content and
    ResourceSync metadata on their web servers. The central hub (in this case the EHRI Portal) is actively collecting
    resources and keeping them in sync with the aid of published sitemaps.*

We can say that the :term:`ResourceSync` Specification is a perfect fit for solving the **external logistics**
when it comes to synchronizing :term:`resource`\ s between a central :term:`Destination` and various
:term:`Source`\ s. *Figure 1.* depicts the external logistics.

When the :term:`resource`\ s we are trying to :term:`synchronize` are not web-resources by them selves but instead stem from
information systems, databases or other places within an organization, we are faced with other problems, which we can
qualify as related to **internal logistics**.

Metadata Publishing Tool
++++++++++++++++++++++++
:term:`Metadata Publishing Tool` is an application that solves various problems related to the **internal logistics**:

*   How do we collect and import :term:`resource`\ s from various places within the organization;
*   How do we select relevant :term:`resource`\ s;
*   How do we create :term:`ResourceSync` :term:`sitemap` metadata on relevant :term:`resource`\ s;
*   How do we export :term:`resource`\ s and :term:`sitemap`\ s to the web server;
*   How do we verify that the exposed URL's are correct and our :term:`ResourceSync` site ready to be harvested by a :term:`Destination`.

.. figure:: ../../img/internal.png

    *Fig. 2. Internal logistics. Metadata Publishing Tool at work.*

*Figure 2.* depicts **internal logistics** and the role of :term:`Metadata Publishing Tool`. The situation
described may be exemplary for Collection Holding Institutions (CHI's) within the EHRI infrastructure, although
different situations may equally be applicable. :term:`Metadata Publishing Tool` is an application that is deployed on
your laptop or local work station. From there you collect and select :term:`resource`\ s, create the :term:`ResourceSync`
:term:`sitemap`\ s, export :term:`resource`\ s and :term:`sitemap`\ s to your web server and verify the exposed URL's.

Configuration of :term:`Metadata Publishing Tool` may need the hand and insight of a technically skilled person.
Once configured it can be managed by archivists and other content-savvy users that do not necessarily have technical skills.

This documentation
++++++++++++++++++
This documentation starts with describing how to install :term:`Metadata Publishing Tool` on various operating Systems in the
:doc:`rsgui.install` pages. Each tab or wizard page of the application is the subject of the other chapters. There
are `Help` buttons on each tab or wizard page that link to the relevant chapters in this documentation. Finally
there is a :doc:`rsgui.glossary` on terms used throughout this documentation.
.. and an appendix that handles various
use cases that may be applicable to your situation on your institution.













