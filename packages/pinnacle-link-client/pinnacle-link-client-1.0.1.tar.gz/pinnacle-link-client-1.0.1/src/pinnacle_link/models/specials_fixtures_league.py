from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .base import BaseModel
from .special_fixture import SpecialFixture



@JsonMap({"id_": "id"})
class SpecialsFixturesLeague(BaseModel):
    """SpecialsFixturesLeague

:param id_: FixturesLeague Id., defaults to None
:type id_: int, optional
:param specials: A collection of Specials, defaults to None
:type specials: List[SpecialFixture], optional
"""
    def __init__(self, id_: int = None, specials: List[SpecialFixture] = None):
        if id_ is not None:
            self.id_ = id_
        if specials is not None:
            self.specials = self._define_list(specials, SpecialFixture)



