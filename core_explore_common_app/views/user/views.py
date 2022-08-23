""" Explore Common Views
"""
from abc import ABCMeta, abstractmethod

from django.contrib import messages
from django.views.generic import RedirectView
from django.views.generic import View

from core_main_app.access_control.exceptions import AccessControlError

from core_explore_common_app import settings
from core_explore_common_app.components.query import api as query_api
from core_explore_common_app.components.query.models import Query
from core_explore_common_app.settings import (
    EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY,
)
from core_explore_common_app.utils.query.query import add_local_data_source


class ResultsView(View):
    """Results View"""

    def __init__(self, **kwargs):
        self.assets = self._load_assets()
        self.modals = self._load_modals()

        super().__init__(**kwargs)

    @staticmethod
    def build_sorting_context_array(query):
        """Get the query data-sources dans build the context sorting array for the JS

        Returns:

        """
        context_array = []
        for data_source in query.data_sources:
            context_array.append(data_source["order_by_field"])

        return ";".join(context_array)

    def _load_assets(self):
        assets = {
            "js": [
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {
                    "path": "core_main_app/common/js/modals/error_page_modal.js",
                    "is_raw": True,
                },
                {"path": "core_main_app/common/js/debounce.js", "is_raw": False},
                {"path": "core_explore_common_app/user/js/results.js", "is_raw": False},
                {
                    "path": "core_explore_common_app/user/js/results.raw.js",
                    "is_raw": True,
                },
                {"path": "core_main_app/user/js/sharing_modal.js", "is_raw": False},
                {
                    "path": "core_explore_common_app/user/js/persistent_query_config.js",
                    "is_raw": False,
                },
                {
                    "path": f"core_explore_common_app/user/js/sorting_{settings.SORTING_DISPLAY_TYPE}_criteria.js",
                    "is_raw": False,
                },
            ],
            "css": [
                "core_main_app/common/css/XMLTree.css",
                "core_explore_common_app/user/css/query_result.css",
                "core_explore_common_app/user/css/results.css",
                "core_explore_common_app/user/css/toggle.css",
            ],
        }

        # Add assets needed for the exporters
        if "core_exporters_app" in settings.INSTALLED_APPS:
            # add all assets needed
            assets["js"].extend(
                [
                    {
                        "path": "core_exporters_app/user/js/exporters/list/modals/list_exporters_selector.js",
                        "is_raw": False,
                    }
                ]
            )

        # Add assets needed for the file preview
        if "core_file_preview_app" in settings.INSTALLED_APPS:
            assets["js"].extend(
                [
                    {
                        "path": "core_file_preview_app/user/js/file_preview.js",
                        "is_raw": False,
                    }
                ]
            )
            assets["css"].append("core_file_preview_app/user/css/file_preview.css")

        # Add assets needed for the PID sharing
        if "core_linked_records_app" in settings.INSTALLED_APPS:
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            if pid_settings_api.get().auto_set_pid:
                assets["js"].extend(
                    [
                        {
                            "path": "core_linked_records_app/user/js/sharing/explore.js",
                            "is_raw": False,
                        }
                    ]
                )
                assets["css"].append("core_linked_records_app/user/css/sharing.css")

        return assets

    def _load_modals(self):
        modals = [
            "core_main_app/common/modals/error_page_modal.html",
            "core_explore_common_app/user/persistent_query/modal.html",
        ]

        # Add the exporters modal
        if "core_exporters_app" in settings.INSTALLED_APPS:
            modals.extend(
                [
                    "core_exporters_app/user/exporters/list/modals/list_exporters_selector.html"
                ]
            )

        # Add the file preview modal
        if "core_file_preview_app" in settings.INSTALLED_APPS:
            modals.append("core_file_preview_app/user/file_preview_modal.html")

        # Add PID modal
        if "core_linked_records_app" in settings.INSTALLED_APPS:
            from core_linked_records_app.components.pid_settings import (
                api as pid_settings_api,
            )

            if pid_settings_api.get().auto_set_pid:
                modals.append("core_linked_records_app/user/sharing/explore/modal.html")

        return modals


class ResultQueryRedirectView(RedirectView, metaclass=ABCMeta):
    """Results Query Redirect View"""

    model_name = None
    object_name = None
    redirect_url = None

    def get_redirect_url(self, *args, **kwargs):
        try:
            # here we receive a PersistentQuery  name or id
            persistent_query_id = self.request.GET.get("id", None)
            persistent_query_name = self.request.GET.get("name", None)

            if persistent_query_id is not None:
                persistent_query = self._get_persistent_query_by_id(
                    persistent_query_id, self.request.user
                )
            elif persistent_query_name is not None:
                persistent_query = self._get_persistent_query_by_name(
                    persistent_query_name, self.request.user
                )
            else:
                messages.add_message(
                    self.request, messages.ERROR, "Expecting id or name."
                )
                return self._get_reversed_url_if_failed()

            # from it we have to duplicate it to a Query with the new user_id
            # we should probably add the query_id into the persistent query?
            # to avoid to recreate this query each time we visit the persistent URL
            query = Query(
                user_id=str(self.request.user.id),
                content=persistent_query.content,
                data_sources=persistent_query.data_sources,
            )
            # add the local data source by default
            if (
                not query.data_sources
                and EXPLORE_ADD_DEFAULT_LOCAL_DATA_SOURCE_TO_QUERY
            ):
                add_local_data_source(self.request, query)

            query = query_api.upsert(query, self.request.user)
            query.templates.set(persistent_query.templates.all())

            # then redirect to the result page core_explore_example_results with /<template_id>/<query_id>
            return self._get_reversed_url(query)
        except AccessControlError:
            # add error message
            messages.add_message(self.request, messages.ERROR, "Access Forbidden.")
            return self._get_reversed_url_if_failed()
        except Exception:
            # add error message
            messages.add_message(
                self.request, messages.ERROR, "The given URL is not valid."
            )
            return self._get_reversed_url_if_failed()

    @staticmethod
    @abstractmethod
    def _get_persistent_query_by_id(persistent_query_id, user):
        raise NotImplementedError("_get_persistent_query method is not implemented.")

    @staticmethod
    @abstractmethod
    def _get_persistent_query_by_name(persistent_query_name, user):
        raise NotImplementedError("_get_persistent_query method is not implemented.")

    @staticmethod
    @abstractmethod
    def get_url_path():
        raise NotImplementedError("get_url_path method is not implemented.")

    @staticmethod
    @abstractmethod
    def _get_reversed_url(query):
        raise NotImplementedError("_get_reversed_url method is not implemented.")

    @staticmethod
    @abstractmethod
    def _get_reversed_url_if_failed():
        raise NotImplementedError(
            "_get_reversed_url_if_failed method is not implemented."
        )
