import random
from dataclasses import dataclass


@dataclass
class ViewportProperties:
    width: int
    height: int
    outerWidth: int
    outerHeight: int
    innerWidth: int
    innerHeight: int

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        self.width, self.height = self._generate_viewport_dimensions()
        self.outerWidth, self.outerHeight = self._generate_outer_dimensions()
        self.innerWidth, self.innerHeight = self._generate_inner_dimensions()

    def _generate_viewport_dimensions(self) -> tuple[int, int]:
        return 1920 + random.randint(-100, 100), 1080 + random.randint(-100, 100)

    def _generate_outer_dimensions(self) -> tuple[int, int]:
        return self.width, self.height

    def _generate_inner_dimensions(self) -> tuple[int, int]:
        return (
            self.width - random.randint(0, 20),
            self.height - random.randint(0, 20),
        )

    def as_dict(self) -> dict:
        return self.__dict__
