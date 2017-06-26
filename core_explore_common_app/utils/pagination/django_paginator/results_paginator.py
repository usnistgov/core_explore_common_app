"""Results paginator util
"""
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from core_explore_common_app.settings import RESULTS_PER_PAGE


class ResultsPaginator(object):

    @staticmethod
    def get_results(results_list, page):
        # Pagination
        paginator = Paginator(results_list, RESULTS_PER_PAGE)

        try:
            results = paginator.page(int(page))
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return results
