import random
from dataclasses import dataclass


@dataclass
class WebGlProperties:
    vendor: str
    renderer: str

    webgl_properties = [
        {"vendor": "Intel Inc.", "renderer": "Intel Iris OpenGL Engine"},
        {"vendor": "AMD", "renderer": "AMD Radeon Pro 5600M OpenGL Engine"},
        {
            "vendor": "NVIDIA",
            "renderer": "NVIDIA GeForce GTX 1660 Ti OpenGL Engine",
        },
        {"vendor": "Apple Inc.", "renderer": "Apple M1 OpenGL Engine"},
        {"vendor": "Qualcomm Inc.", "renderer": "Qualcomm Adreno OpenGL Engine"},
    ]

    def __init__(self):
        self.vendor = self._generate_vendor()
        self.renderer = self._generate_renderer()

    def as_dict(self):
        return self.__dict__

    def _generate_vendor(self) -> str:
        """Generates the vendor based on the user agent."""

        return random.choice(self.webgl_properties)["vendor"]

    def _generate_renderer(self) -> str:
        """Generates the renderer based on the user agent."""

        return random.choice(self.webgl_properties)["renderer"]
