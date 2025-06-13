from dataclasses import dataclass


@dataclass
class HeaderProperties:
    """Class for the header properties. We will take the Sec_Fetch_Site, Sec_Fetch_Mode and Sec_Fetch_Dest from the original headers."""

    # Headers passed by library
    user_agent: str
    accept_language: str
    accept_encoding: str
    accept: str
    referer: str

    # Self generated headers
    origin: str
    sec_ch_ua: str
    sec_ch_ua_mobile: str
    sec_ch_ua_platform: str
    sec_ch_ua_form_factors: str
    dnt: str

    def __init__(
        self,
        brands: list[dict],
        dnt: str,
        client_hint_headers_enabled: bool = True,
        **kwargs,
    ):
        # Passed by library
        self.user_agent = kwargs["User-Agent"]
        self.accept_language = kwargs["Accept-language"]
        self.accept_encoding = kwargs["Accept-encoding"]
        self.accept = kwargs["Accept"]
        self.referer = kwargs["Referer"]

        # # Shared properties
        self.dnt = dnt

        # # Self generated headers
        if client_hint_headers_enabled:
            self.sec_ch_ua = self._generate_sec_ch_ua(brands)
            self.sec_ch_ua_mobile = self._generate_sec_ch_ua_mobile()
            self.sec_ch_ua_platform = self._generate_sec_ch_ua_platform()
            self.sec_ch_ua_form_factors = self._generate_sec_ch_ua_form_factors()

    def _generate_sec_ch_ua_platform(self) -> str:
        """Generates the Sec_Ch_Ua_Platform based on the user agent platform."""

        is_mac = "Macintosh" in self.user_agent
        is_windows = "Windows" in self.user_agent
        is_linux = "Linux" in self.user_agent

        if is_mac:
            return "macOS"
        elif is_windows:
            return "Windows"
        elif is_linux:
            return "Linux"
        else:
            return "Unknown"

    def _generate_sec_ch_ua(self, brands: list[dict]) -> str:
        """Generates the Sec_Ch_Ua based brands generated"""
        merged_brands = "".join([f'"{brand["brand"]}";v="{brand["version"]}",' for brand in brands])
        return merged_brands

    def _generate_sec_ch_ua_form_factors(self) -> str:
        """Generates the Sec_Ch_Ua_Form_Factors based on the user agent."""

        return "desktop"

    def _generate_sec_ch_ua_mobile(self) -> str:
        """Generates the Sec_Ch_Ua_Mobile based on the user agent."""

        return "?0"

    def as_dict(self) -> dict:
        # Convert all keys to kebab case and return a new dictionary
        return {key.replace("_", "-").lower(): value for key, value in self.__dict__.items()}
