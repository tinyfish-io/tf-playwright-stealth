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
        webgl_prop = self._generate_webgl_prop()
        self.vendor = webgl_prop["vendor"]
        self.renderer = webgl_prop["renderer"]

    def _generate_webgl_prop(self):
        """Generates a WebGL property containing both vendor and renderer."""
        return random.choice(self.webgl_properties)

    def as_dict(self):
        return self.__dict__
