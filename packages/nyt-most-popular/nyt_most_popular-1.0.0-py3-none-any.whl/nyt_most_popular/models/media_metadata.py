from .utils.json_map import JsonMap
from .base import BaseModel


@JsonMap({})
class MediaMetadata(BaseModel):
    """MediaMetadata

    :param url: Image's URL., defaults to None
    :type url: str, optional
    :param format: Image's crop name., defaults to None
    :type format: str, optional
    :param height: Image's height (e.g. 293)., defaults to None
    :type height: int, optional
    :param width: Image's width (e.g. 440)., defaults to None
    :type width: int, optional
    """

    def __init__(
        self, url: str = None, format: str = None, height: int = None, width: int = None
    ):
        if url is not None:
            self.url = url
        if format is not None:
            self.format = format
        if height is not None:
            self.height = height
        if width is not None:
            self.width = width
