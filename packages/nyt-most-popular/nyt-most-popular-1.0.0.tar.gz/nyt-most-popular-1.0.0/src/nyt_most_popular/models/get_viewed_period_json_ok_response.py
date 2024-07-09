from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .viewed_article import ViewedArticle


@JsonMap({})
class GetViewedPeriodJsonOkResponse(BaseModel):
    """GetViewedPeriodJsonOkResponse

    :param status: API response status (e.g. OK)., defaults to None
    :type status: str, optional
    :param copyright: Copyright message., defaults to None
    :type copyright: str, optional
    :param num_results: Number of articles in the results (e.g. 20)., defaults to None
    :type num_results: int, optional
    :param results: Array of articles., defaults to None
    :type results: List[ViewedArticle], optional
    """

    def __init__(
        self,
        status: str = None,
        copyright: str = None,
        num_results: int = None,
        results: List[ViewedArticle] = None,
    ):
        if status is not None:
            self.status = status
        if copyright is not None:
            self.copyright = copyright
        if num_results is not None:
            self.num_results = num_results
        if results is not None:
            self.results = self._define_list(results, ViewedArticle)
