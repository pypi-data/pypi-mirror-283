from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .media import Media


@JsonMap({"id_": "id", "type_": "type"})
class SharedArticle(BaseModel):
    """SharedArticle

    :param url: Article's URL., defaults to None
    :type url: str, optional
    :param adx_keywords: Semicolon separated list of keywords., defaults to None
    :type adx_keywords: str, optional
    :param subsection: Article's subsection (e.g. Politics). Can be empty string., defaults to None
    :type subsection: str, optional
    :param column: Deprecated. Set to null., defaults to None
    :type column: str, optional
    :param eta_id: Deprecated. Set to 0., defaults to None
    :type eta_id: int, optional
    :param section: Article's section (e.g. Sports)., defaults to None
    :type section: str, optional
    :param id_: Asset ID number (e.g. 100000007772696)., defaults to None
    :type id_: int, optional
    :param asset_id: Asset ID number (e.g. 100000007772696)., defaults to None
    :type asset_id: int, optional
    :param nytdsection: Article's section (e.g. sports)., defaults to None
    :type nytdsection: str, optional
    :param byline: Article's byline (e.g. By Thomas L. Friedman)., defaults to None
    :type byline: str, optional
    :param type_: Asset type (e.g. Article, Interactive, ...)., defaults to None
    :type type_: str, optional
    :param title: Article's headline (e.g. When the Cellos Play, the Cows Come Home)., defaults to None
    :type title: str, optional
    :param abstract: Brief summary of the article., defaults to None
    :type abstract: str, optional
    :param published_date: When the article was published on the web (e.g. 2021-04-19)., defaults to None
    :type published_date: str, optional
    :param source: Publisher (e.g. New York Times)., defaults to None
    :type source: str, optional
    :param updated: When the article was last updated (e.g. 2021-05-12 06:32:03)., defaults to None
    :type updated: str, optional
    :param des_facet: Array of description facets (e.g. Quarantine (Life and Culture))., defaults to None
    :type des_facet: List[str], optional
    :param org_facet: Array of organization facets (e.g. Sullivan Street Bakery)., defaults to None
    :type org_facet: List[str], optional
    :param per_facet: Array of person facets (e.g. Bittman, Mark)., defaults to None
    :type per_facet: List[str], optional
    :param geo_facet: Array of geographic facets (e.g. Canada)., defaults to None
    :type geo_facet: List[str], optional
    :param media: Array of images., defaults to None
    :type media: List[Media], optional
    :param uri: An article's globally unique identifier., defaults to None
    :type uri: str, optional
    """

    def __init__(
        self,
        url: str = None,
        adx_keywords: str = None,
        subsection: str = None,
        column: str = None,
        eta_id: int = None,
        section: str = None,
        id_: int = None,
        asset_id: int = None,
        nytdsection: str = None,
        byline: str = None,
        type_: str = None,
        title: str = None,
        abstract: str = None,
        published_date: str = None,
        source: str = None,
        updated: str = None,
        des_facet: List[str] = None,
        org_facet: List[str] = None,
        per_facet: List[str] = None,
        geo_facet: List[str] = None,
        media: List[Media] = None,
        uri: str = None,
    ):
        if url is not None:
            self.url = url
        if adx_keywords is not None:
            self.adx_keywords = adx_keywords
        if subsection is not None:
            self.subsection = subsection
        if column is not None:
            self.column = column
        if eta_id is not None:
            self.eta_id = eta_id
        if section is not None:
            self.section = section
        if id_ is not None:
            self.id_ = id_
        if asset_id is not None:
            self.asset_id = asset_id
        if nytdsection is not None:
            self.nytdsection = nytdsection
        if byline is not None:
            self.byline = byline
        if type_ is not None:
            self.type_ = type_
        if title is not None:
            self.title = title
        if abstract is not None:
            self.abstract = abstract
        if published_date is not None:
            self.published_date = published_date
        if source is not None:
            self.source = source
        if updated is not None:
            self.updated = updated
        if des_facet is not None:
            self.des_facet = des_facet
        if org_facet is not None:
            self.org_facet = org_facet
        if per_facet is not None:
            self.per_facet = per_facet
        if geo_facet is not None:
            self.geo_facet = geo_facet
        if media is not None:
            self.media = self._define_list(media, Media)
        if uri is not None:
            self.uri = uri
