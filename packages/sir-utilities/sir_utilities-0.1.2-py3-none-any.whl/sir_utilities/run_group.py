from enum import Enum


# TODO: Refactor this into sir utilites, and make sir utilites a package as well
class RunGroup(Enum):
    LIVE = "live"
    UNITTEST = "unittest"
