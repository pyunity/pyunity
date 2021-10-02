from typing import Dict, Generator, Optional, Any
from collections.abc import KeysView, ValuesView, ItemsView

class LiveDict:
    d: Dict
    parent: Optional[LiveDict]
    def __init__(self, d: Dict, parent: Optional[LiveDict] = ...) -> None: ...
    def __getitem__(self, item: Any) -> Any: ...
    def __setitem__(self, item: Any, value: Any) -> None: ...
    def __delitem__(self, item: Any) -> None: ...
    def __contains__(self, item: Any) -> bool: ...
    def __iter__(self) -> Generator: ...
    def update(self) -> None: ...
    def todict(self) -> Dict: ...
    def keys(self) -> KeysView: ...
    def values(self) -> ValuesView: ...
    def items(self) -> ItemsView: ...
    def pop(self, item: Any) -> Any: ...

class Database(LiveDict):
    path: str
    def __init__(self, path: str) -> None: ...
    def update(self) -> None: ...
    def refresh(self) -> None: ...

file: str = ...
db: Database = ...
