from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({})
class Currency(BaseModel):
    """Currency

:param code: Currency code., defaults to None
:type code: str, optional
:param name: Currency name., defaults to None
:type name: str, optional
:param rate: Exchange rate to USD., defaults to None
:type rate: float, optional
"""
    def __init__(self, code: str = None, name: str = None, rate: float = None):
        if code is not None:
            self.code = code
        if name is not None:
            self.name = name
        if rate is not None:
            self.rate = rate



