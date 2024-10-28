import re
import random
from dataclasses import dataclass
from fake_http_header import FakeHttpHeader
from ._header_properties import HeaderProperties
from ._navigator_properties import NavigatorProperties
from ._viewport_properties import ViewportProperties
from ._webgl_properties import WebGlProperties


@dataclass
class Properties:

    header: HeaderProperties
    navigator: NavigatorProperties
    viewport: ViewportProperties
    webgl: WebGlProperties
    runOnInsecureOrigins: bool

    def __init__(self):
        spoofed_headers = FakeHttpHeader(domain_code="com", browser="chrome")

        # Generate shared properties
        brands = self._generate_brands(spoofed_headers.user_agent)
        dnt = self._generate_dnt()

        # Generate properties
        self.header = HeaderProperties(
            brands=brands, dnt=dnt, **spoofed_headers.as_header_dict()
        )
        self.navigator = NavigatorProperties(
            brands=brands, dnt=dnt, **spoofed_headers.as_header_dict()
        )
        self.viewport = ViewportProperties()
        self.webgl = WebGlProperties()
        self.runOnInsecureOrigins = None

    def _generate_brands(self, user_agent: str, browser: str = "chrome") -> str:
        """Generates the brands based on the referer."""

        regex_patterns = {
            "chrome": r"Chrome/(\d+)",
            "firefox": r"Firefox/(\d+)",
            "safari": r"Version/(\d+)",
        }

        pattern = regex_patterns[browser]

        browser_with_version = re.search(pattern, user_agent)
        version = browser_with_version.group(1)
        seed = int(version.split(".")[0])

        order = [
            [0, 1, 2],
            [0, 2, 1],
            [1, 0, 2],
            [1, 2, 0],
            [2, 0, 1],
            [2, 1, 0],
        ][seed % 6]

        escaped_chars = [" ", " ", ";"]

        greasey_brand = f"{escaped_chars[order[0]]}Not{escaped_chars[order[1]]}A{escaped_chars[order[2]]}Brand"

        greased_brand_version_list = [{}, {}, {}]

        greased_brand_version_list[order[0]] = {
            "brand": greasey_brand,
            "version": "99",
        }

        greased_brand_version_list[order[1]] = {
            "brand": "Chromium",
            "version": seed,
        }

        greased_brand_version_list[order[2]] = {
            "brand": "Google Chrome",
            "version": seed,
        }

        return greased_brand_version_list

    def _generate_dnt(self) -> str:
        """Randomly generates a 0 or 1."""

        return str(random.randint(0, 1))

    def as_dict(self) -> dict:
        """Returns the properties as a dictionary."""

        return {
            "header": self.header.as_dict(),
            "viewport": self.viewport.as_dict(),
            "navigator": self.navigator.as_dict(),
            "webgl": self.webgl.as_dict(),
        }
