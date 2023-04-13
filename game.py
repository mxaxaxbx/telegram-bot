from typing import NamedTuple, Text, List
from PIL import Image
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

class Color(NamedTuple):
    """
    8-bit components of a color
    """

    r: int
    g: int
    b: int

class Video(NamedTuple):
    """
    That's a video from the API
    """

    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text

DISPLAY_SIZE = Size(int(480 * 1.5), int(270 * 1.5))
BLACK = Color(0, 0, 0)

def bisect(n, mapper, tester):
    """
    Runs a bisection.

    - `n` is the number of elements to be bisected
    - `mapper` is a callable that will transform an integer from "0" to "n"
      into a value that can be tested
    - `tester` returns true if the value is within the "right" range
    """

    if n < 1:
        raise ValueError("Cannot bissect an empty array")

    left = 0
    right = n - 1

    while left + 1 < right:
        mid = int((left + right) / 2)

        val = mapper(mid)

        if tester(val):
            right = mid
        else:
            left = mid

    return mapper(right)

class Frame:
    """
    Wrapper around frame data to help drawing it on the screen
    """

    def __init__(self, data):
        self.data = data
        self.image = None

    def blit(self, disp):
        if not self.image:
            pil_img = Image.open(io.BytesIO(self.data))
            pil_img.thumbnail(DISPLAY_SIZE)
            buf = pil_img.tobytes()
            size = pil_img.width, pil_img.height
            self.image = 'pygame.image.frombuffer(buf, size, "RGB")'

        disp.blit(self.image, (0, 0))
