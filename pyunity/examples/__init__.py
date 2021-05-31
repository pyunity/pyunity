from . import (
    example1, example2, example3, example4, example5, example6, example7, example8, example9
)
from ..scenes import SceneManager
from .. import Logger

import sys

example_list = [
    example1,
    example2,
    example3,
    example4,
    example5,
    example6,
    example7,
    example8,
    example9,
]

def show():
    if len(sys.argv) == 1:
        num = 0
    else:
        num = int(sys.argv[1])
    if not num:
        for index, example in enumerate(example_list):
            Logger.Log("\nExample", str(index + 1))
            example.main()
            SceneManager.RemoveScene(SceneManager.GetSceneByName("Scene"))
    else:
        example_list[num - 1].main()
