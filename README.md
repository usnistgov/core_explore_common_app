# core_explore_common_app

core_explore_common_app is a Django app.

# Quick start

1. Add "core_explore_common_app" to your INSTALLED_APPS setting like this:

  ```python
  INSTALLED_APPS = [
      ...
      'core_explore_common_app',
  ]
  ```

  2. Include the core_explore_common_app URLconf in your project urls.py like this::

  ```python
  url(r'^explore/common/', include('core_explore_common_app.urls')),
  ```
