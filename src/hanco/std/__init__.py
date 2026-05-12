from .file_std import STDLIB as FILE_STDLIB
from .random_std import STDLIB as RANDOM_STDLIB
from .time_std import STDLIB as TIME_STDLIB


STDLIB = {}

for module_stdlib in (RANDOM_STDLIB, TIME_STDLIB, FILE_STDLIB):
    STDLIB.update(module_stdlib)
