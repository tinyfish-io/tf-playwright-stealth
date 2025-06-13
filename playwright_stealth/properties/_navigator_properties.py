from dataclasses import dataclass


@dataclass
class NavigatorProperties:
    """Class for the navigator properties."""

    userAgent: str
    platform: str
    language: str
    languages: list[str]
    appVersion: str
    vendor: str
    deviceMemory: int
    hardwareConcurrency: int
    maxTouchPoints: int
    doNotTrack: str
    brands: list[dict]
    mobile: bool

    def __init__(self, brands: list[dict], dnt: str, **kwargs):
        self.userAgent = kwargs["User-Agent"]

        # Shared properties
        self.brands = brands
        self.doNotTrack = dnt

        # Generate properties
        self.platform = self._generate_platform(kwargs["User-Agent"])
        self.language = self._generate_language()
        self.languages = self._generate_languages(kwargs["Accept-language"])
        self.appVersion = self._generate_app_version(kwargs["User-Agent"])
        self.vendor = self._generate_vendor(kwargs["User-Agent"])
        self.deviceMemory = self._generate_device_memory(kwargs["User-Agent"])
        self.hardwareConcurrency = self._generate_hardware_concurrency(self.deviceMemory)
        self.maxTouchPoints = self._generate_max_touch_points()
        self.mobile = self._generate_mobile()
        self.productSub = self._generate_product_sub(kwargs["User-Agent"])

    def _generate_platform(self, user_agent: str) -> str:
        """Generates the platform based on the user agent."""

        # Change regarding this article: \
        # https://filipvitas.medium.com/how-to-set-user-agent-header-with-puppeteer-js-and-not-fail-28c7a02165da
        if "Macintosh" in user_agent:
            return "MacIntel"
        elif "Linux" in user_agent:
            return "Linux x86_x64"
        else:
            return "Win64"

    def _generate_language(self) -> str:
        """Generates the language based on the accept language."""

        return "en-US"

    def _generate_languages(self, accept_language: str) -> list[str]:
        """Generates the languages based on the accept language."""

        languages_with_quality = accept_language.split(",")
        languages = [language.split(";")[0] for language in languages_with_quality]
        return languages

    def _generate_app_version(self, user_agent: str) -> str:
        """Generates the app version based on the user agent."""

        version_part = user_agent.split("/", 1)[1]
        return version_part

    def _generate_vendor(self, user_agent: str) -> str:
        """Generates the vendor based on the user agent."""

        if "Chrome" in user_agent:
            return "Google Inc."
        elif "Firefox" in user_agent:
            return ""

        return "Google Inc."

    def _generate_device_memory(self, user_agent: str) -> int:
        """Generates the device memory."""

        return None if "Firefox" in user_agent else 8

    def _generate_hardware_concurrency(self, device_memory: int) -> int:
        """Generates the hardware concurrency."""

        return device_memory

    def _generate_max_touch_points(self) -> int:
        """Generates the max touch points. Default is 0 since this is a desktop browser."""

        return 0

    def _generate_mobile(self) -> bool:
        """Generates the mobile flag."""

        return False

    def _generate_product_sub(self, user_agent: str) -> int:
        """Generate product sub depending on the Browser"""
        return 20100101 if "Firefox" in user_agent else 20030107

    def as_dict(self) -> dict:
        return self.__dict__
