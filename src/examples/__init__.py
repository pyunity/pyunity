from . import (
    example1, example2, example3, example4, example5, example6, example7, example8
)
from ..scene import SceneManager

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
]

def show():
    if len(sys.argv) == 1:
        num = 0
    else:
        num = int(sys.argv[1])
    if not num:
        for index, example in enumerate(example_list):
            print("\nExample", index + 1)
            example.main()
            SceneManager.RemoveScene(SceneManager.GetSceneByName("Scene"))
    else:
        example_list[num - 1].main()
