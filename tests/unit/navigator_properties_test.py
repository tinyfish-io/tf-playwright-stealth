import pytest
from fake_http_header import FakeHttpHeader
from playwright_stealth.properties._navigator_properties import NavigatorProperties


@pytest.fixture
def fake_headers():
    """Fixture to generate fake headers using FakeHttpHeader."""
    return FakeHttpHeader(domain_code="com", browser="chrome").as_header_dict()


@pytest.fixture
def brands():
    """Fixture for sample brand data."""
    return [
        {"brand": "Chromium", "version": "95"},
        {"brand": "Google Chrome", "version": "95"},
    ]


@pytest.fixture
def navigator_properties(fake_headers, brands):
    """Fixture to initialize NavigatorProperties with fake headers and brands."""
    return NavigatorProperties(brands=brands, dnt="1", **fake_headers)


def test_initialization(navigator_properties, fake_headers, brands):
    """Test that NavigatorProperties initializes with correct attributes."""
    assert navigator_properties.userAgent == fake_headers["User-Agent"]
    assert navigator_properties.platform in ["Macintosh", "Windows", "Linux"]
    assert navigator_properties.language == "en-US"
    assert isinstance(navigator_properties.languages, list)
    assert (
        navigator_properties.appVersion
        == navigator_properties._generate_app_version(fake_headers["User-Agent"])
    )
    assert navigator_properties.vendor in ["Google Inc.", ""]
    assert navigator_properties.deviceMemory == 8
    assert navigator_properties.hardwareConcurrency == 8
    assert navigator_properties.maxTouchPoints == 0
    assert navigator_properties.doNotTrack == "1"
    assert navigator_properties.brands == brands
    assert navigator_properties.mobile is False


def test_generate_platform(navigator_properties):
    """Test the _generate_platform method with various user agents."""
    ua_mac = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    ua_windows = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    ua_linux = "Mozilla/5.0 (X11; Linux x86_64)"
    assert navigator_properties._generate_platform(ua_mac) == "Macintosh"
    assert navigator_properties._generate_platform(ua_windows) == "Windows"
    assert navigator_properties._generate_platform(ua_linux) == "Linux"


def test_generate_languages(navigator_properties):
    """Test the _generate_languages method."""
    accept_language = "en-US,en;q=0.9,fr;q=0.8"
    expected_languages = ["en-US", "en", "fr"]
    assert (
        navigator_properties._generate_languages(accept_language) == expected_languages
    )


def test_generate_app_version(navigator_properties):
    """Test the _generate_app_version method."""
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    expected_version = "5.0 (Windows NT 10.0; Win64; x64)"
    assert navigator_properties._generate_app_version(user_agent) == expected_version


def test_generate_vendor(navigator_properties):
    """Test the _generate_vendor method."""
    ua_chrome = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/85.0.4183.102"
    ua_firefox = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/80.0"
    ua_safari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
    assert navigator_properties._generate_vendor(ua_chrome) == "Google Inc."
    assert navigator_properties._generate_vendor(ua_firefox) == ""
    # Since the default in your code is "Google Inc.", Safari will return "Google Inc."
    assert navigator_properties._generate_vendor(ua_safari) == "Google Inc."


def test_as_dict(navigator_properties):
    """Test that as_dict converts the navigator properties to a dictionary correctly."""
    navigator_dict = navigator_properties.as_dict()
    assert navigator_dict["userAgent"] == navigator_properties.userAgent
    assert navigator_dict["platform"] == navigator_properties.platform
    assert navigator_dict["language"] == navigator_properties.language
    assert navigator_dict["languages"] == navigator_properties.languages
    assert navigator_dict["appVersion"] == navigator_properties.appVersion
    assert navigator_dict["vendor"] == navigator_properties.vendor
    assert navigator_dict["deviceMemory"] == navigator_properties.deviceMemory
    assert (
        navigator_dict["hardwareConcurrency"]
        == navigator_properties.hardwareConcurrency
    )
    assert navigator_dict["maxTouchPoints"] == navigator_properties.maxTouchPoints
    assert navigator_dict["doNotTrack"] == navigator_properties.doNotTrack
    assert navigator_dict["brands"] == navigator_properties.brands
    assert navigator_dict["mobile"] == navigator_properties.mobile
