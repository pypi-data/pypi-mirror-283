from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .media_metadata import MediaMetadata


@JsonMap({"type_": "type", "media_metadata": "media-metadata"})
class Media(BaseModel):
    """Media

    :param type_: Asset type (e.g. image)., defaults to None
    :type type_: str, optional
    :param subtype: Asset subtype (e.g. photo)., defaults to None
    :type subtype: str, optional
    :param caption: Media caption., defaults to None
    :type caption: str, optional
    :param copyright: Media credit., defaults to None
    :type copyright: str, optional
    :param approved_for_syndication: Whether media is approved for syndication., defaults to None
    :type approved_for_syndication: int, optional
    :param media_metadata: Media metadata (url, width, height, ...)., defaults to None
    :type media_metadata: List[MediaMetadata], optional
    """

    def __init__(
        self,
        type_: str = None,
        subtype: str = None,
        caption: str = None,
        copyright: str = None,
        approved_for_syndication: int = None,
        media_metadata: List[MediaMetadata] = None,
    ):
        if type_ is not None:
            self.type_ = type_
        if subtype is not None:
            self.subtype = subtype
        if caption is not None:
            self.caption = caption
        if copyright is not None:
            self.copyright = copyright
        if approved_for_syndication is not None:
            self.approved_for_syndication = approved_for_syndication
        if media_metadata is not None:
            self.media_metadata = self._define_list(media_metadata, MediaMetadata)
