from . import example1
from . import example2
from . import example3
from . import example4
from . import example5

import sys

example_list = [
    example1,
    example2,
    example3,
    example4,
    example5,
]

def show():
    num = 0 if len(sys.argv) < 2 else int(sys.argv[1]) - 1
    example_list[num].main()