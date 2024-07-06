from typing import Dict, Optional
from pybi.utils.data_gen import Jsonable


class ActionInfo(Jsonable):
    def __init__(self, id: str, name: str, kwargs: Optional[Dict] = None) -> None:
        self.id = id
        self.name = name
        self.kwargs = kwargs or {}
