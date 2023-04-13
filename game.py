from typing import NamedTuple
import os

API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/")
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)

class Size(NamedTuple):
    """
    Represents a size
    """

    width: int
    height: int
