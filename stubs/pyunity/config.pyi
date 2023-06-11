## Copyright (c) 2020-2023 The PyUnity Team
## This file is licensed under the MIT License.
## See https://docs.pyunity.x10.bz/en/latest/license.html

from typing import Tuple, Type, Union

audio: bool = ...

size: Tuple[int, int] = ...
fps: int = ...
faceCulling: bool = ...
windowProvider: Union[Type, None] = ...
vsync: bool = ...
exitOnError: bool = ...
