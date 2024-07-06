from .utils.json_map import JsonMap
from .base import BaseModel



@JsonMap({"id_": "id","rot_num": "rotNum"})
class SpecialsFixturesContestant(BaseModel):
    """SpecialsFixturesContestant

:param id_: Contestant Id., defaults to None
:type id_: int, optional
:param name: Name of the contestant., defaults to None
:type name: str, optional
:param rot_num: Rotation Number., defaults to None
:type rot_num: int, optional
"""
    def __init__(self, id_: int = None, name: str = None, rot_num: int = None):
        if id_ is not None:
            self.id_ = id_
        if name is not None:
            self.name = name
        if rot_num is not None:
            self.rot_num = rot_num



