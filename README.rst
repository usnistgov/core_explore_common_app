=======================
Core Explore Common App
=======================

Base exploration function for the curator core project.

Quick start
===========

1. Add "core_explore_common_app" to your INSTALLED_APPS setting
---------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_explore_common_app',
    ]

2. Include the core_explore_common_app URLconf in your project urls.py
----------------------------------------------------------------------

.. code:: python

    url(r'^explore/common/', include('core_explore_common_app.urls')),
