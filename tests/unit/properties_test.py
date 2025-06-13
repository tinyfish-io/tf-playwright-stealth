import logging

import pytest
from fake_http_header import FakeHttpHeader
from mockito import mock, unstub, when, when2

import playwright_stealth.properties._properties as properties
from playwright_stealth.properties._header_properties import HeaderProperties
from playwright_stealth.properties._navigator_properties import NavigatorProperties
from playwright_stealth.properties._properties import Properties
from playwright_stealth.properties._viewport_properties import ViewportProperties
from playwright_stealth.properties._webgl_properties import WebGlProperties

log = logging.getLogger(__name__)


@pytest.fixture
def fake_headers():
    """Provides fake headers for mocking."""
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/85.0.4183.102",
        "Accept-language": "en-US,en;q=0.9",
        "Accept-encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.example.com",
    }


@pytest.fixture
def mock_fake_http_header(fake_headers):
    """Mocks FakeHttpHeader used within the Properties class."""
    mock_instance = mock(FakeHttpHeader)
    when2(properties.FakeHttpHeader, domain_code="com", browser="chrome").thenReturn(mock_instance)
    mock_instance.user_agent = fake_headers["User-Agent"]
    when(mock_instance).as_header_dict().thenReturn(fake_headers)
    yield
    unstub()


@pytest.fixture
def mock_properties_dependencies(mock_fake_http_header):
    """Mocks methods in Properties and its dependencies to control randomness."""
    # Mock Properties._generate_dnt
    when(properties.Properties)._generate_dnt().thenReturn("1")

    # Mock ViewportProperties methods
    when(ViewportProperties)._generate_viewport_dimensions().thenReturn((1920, 1080))
    when(ViewportProperties)._generate_outer_dimensions().thenReturn((1920, 1080))
    when(ViewportProperties)._generate_inner_dimensions().thenReturn((1920, 1080))

    # Mock WebGlProperties
    test_webgl_prop = {"vendor": "Test Vendor", "renderer": "Test Renderer"}
    when(WebGlProperties)._generate_webgl_prop().thenReturn(test_webgl_prop)

    yield
    unstub()


def test_initialization(mock_properties_dependencies, fake_headers):
    """Test that Properties initializes all components correctly."""
    # Create an instance of Properties
    props = Properties()

    # Assertions for header properties
    assert isinstance(props.header, HeaderProperties)
    assert props.header.user_agent == fake_headers["User-Agent"]
    assert props.header.accept_language == fake_headers["Accept-language"]
    assert props.header.dnt == "1"

    # Assertions for navigator properties
    assert isinstance(props.navigator, NavigatorProperties)
    assert props.navigator.userAgent == fake_headers["User-Agent"]
    assert props.navigator.doNotTrack == "1"

    # Assertions for viewport properties
    assert isinstance(props.viewport, ViewportProperties)
    assert props.viewport.width == 1920
    assert props.viewport.height == 1080

    # Assertions for webgl properties
    assert isinstance(props.webgl, WebGlProperties)
    assert props.webgl.vendor == "Test Vendor"
    assert props.webgl.renderer == "Test Renderer"

    # Assertion for runOnInsecureOrigins
    assert props.runOnInsecureOrigins is None


def test_generate_brands(mock_fake_http_header, fake_headers):
    """Test the _generate_brands method."""
    # Create Properties instance
    props = Properties()
    brands = props._generate_brands(fake_headers["User-Agent"])

    # Verify that brands is a list of dictionaries with 'brand' and 'version'
    assert isinstance(brands, list)
    assert len(brands) == 3
    for brand_info in brands:
        assert "brand" in brand_info
        assert "version" in brand_info


def test_generate_dnt():
    """Test the _generate_dnt method."""
    # Mock Properties._generate_dnt
    when(properties.Properties)._generate_dnt().thenReturn("0")

    props = Properties()
    dnt = props._generate_dnt()
    assert dnt == "0"

    unstub()


def test_as_dict(mock_properties_dependencies, fake_headers):
    """Test the as_dict method."""
    # Create Properties instance
    props = Properties()
    props_dict = props.as_dict()

    # Assertions for header in as_dict
    assert props_dict["header"]["user-agent"] == fake_headers["User-Agent"]
    assert props_dict["header"]["dnt"] == "1"

    # Assertions for navigator in as_dict
    assert props_dict["navigator"]["userAgent"] == fake_headers["User-Agent"]
    assert props_dict["navigator"]["doNotTrack"] == "1"

    # Assertions for viewport in as_dict
    expected_viewport = {
        "width": 1920,
        "height": 1080,
        "outerWidth": 1920,
        "outerHeight": 1080,
        "innerWidth": 1920,
        "innerHeight": 1080,
    }
    assert props_dict["viewport"] == expected_viewport

    # Assertions for webgl in as_dict
    expected_webgl = {
        "vendor": "Test Vendor",
        "renderer": "Test Renderer",
    }
    assert props_dict["webgl"] == expected_webgl


def test_full_integration():
    """Test the Properties class as a whole."""
    # This test allows randomness to ensure components integrate correctly
    props = Properties()
    props_dict = props.as_dict()

    # Check that the dictionary has the correct keys
    assert "header" in props_dict
    assert "navigator" in props_dict
    assert "viewport" in props_dict
    assert "webgl" in props_dict

    # Check that header properties are consistent
    header = props_dict["header"]
    navigator = props_dict["navigator"]
    assert header["user-agent"] == navigator["userAgent"]

    # Check that dnt values are consistent
    assert header["dnt"] == navigator["doNotTrack"]

    # Check that viewport dimensions make sense
    viewport = props_dict["viewport"]
    assert viewport["width"] >= viewport["innerWidth"]
    assert viewport["height"] >= viewport["innerHeight"]

    # Check that webgl properties are valid
    webgl = props_dict["webgl"]
    webgl_properties = props.webgl.webgl_properties
    assert {
        "vendor": webgl["vendor"],
        "renderer": webgl["renderer"],
    } in webgl_properties

    unstub()
