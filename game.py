from typing import NamedTuple, Text, List
from urllib.parse import urljoin, quote
from httpx import Client
from PIL import Image
import os
import io
import base64

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

    def blit(self):
        # print(self.data)
        return self.data
        if not self.image:
            buffer = io.BytesIO()
            pil_img = Image.open(io.BytesIO(self.data))
            pil_img.thumbnail(DISPLAY_SIZE)
            # buf = pil_img.ba
            # size = pil_img.width, pil_img.height
            pil_img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue())
            self.image = 'data:image/png;base64,' + img_str.decode('utf-8')
            # self.image = 'pygame.image.frombuffer(buf, size, "RGB")'
            return self.image

class FrameX:
    """
    Utility class to access the FrameX API
    """

    BASE_URL = API_BASE

    def __init__(self):
        self.client = Client(timeout=30)

    def video(self, video: Text) -> Video:
        """
        Fetches information about a video
        """

        r = self.client.get(urljoin(self.BASE_URL, f"video/{quote(video)}/"))
        r.raise_for_status()
        return Video(**r.json())

    def video_frame(self, video: Text, frame: int) -> bytes:
        """
        Fetches the JPEG data of a single frame
        """

        # print(urljoin(self.BASE_URL, f'video/{quote(video)}/frame/{quote(f"{frame}")}/'))
        return urljoin(self.BASE_URL, f'video/{quote(video)}/frame/{quote(f"{frame}")}/')

        r = self.client.get(
            urljoin(self.BASE_URL, f'video/{quote(video)}/frame/{quote(f"{frame}")}/')
        )
        r.raise_for_status()
        return r.content


class FrameXBisector:
    """
    Helps managing the display of images from the launch
    """

    BASE_URL = API_BASE

    def __init__(self, name):
        self.api = FrameX()
        self.video = self.api.video(name)
        self._index = 0
        self.image = None

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, v):
        """
        When a new index is written, download the new frame
        """

        self._index = v
        self.image = Frame(self.api.video_frame(self.video.name, v))

    @property
    def count(self):
        return self.video.frames

    def blit(self):
        """
        Draws the current picture.
        """

        return self.image.blit()


def confirm(title):
    """
    Asks a yes/no question to the user
    """


    return  f"{title} - did the rocket launch yet?"


def main():
    """
    Runs a bisection algorithm on the frames of the video, the goal is
    to figure at which exact frame the rocket takes off.

    Images are displayed using pygame, but the interactivity happens in
    the terminal as it is much easier to do.
    """

    # pygame.init()

    bisector = FrameXBisector(VIDEO_NAME)
    # disp = pygame.display.set_mode(DISPLAY_SIZE)

    def mapper(n):
        """
        In that case there is no need to map (or rather, the mapping
        is done visually by the user)
        """

        return n

    def tester(n):
        """
        Displays the current candidate to the user and asks them to
        check if they see wildfire damages.
        """

        bisector.index = n
        # disp.fill(BLACK)
        # bisector.blit(disp)
        # pygame.display.update()

        return confirm(bisector.index)

    culprit = bisect(bisector.count, mapper, tester)
    bisector.index = culprit

    print(f"Found! Take-off = {bisector.index}")

    # pygame.quit()
    exit()

