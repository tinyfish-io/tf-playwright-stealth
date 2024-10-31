import pytest
from fake_http_header import FakeHttpHeader
from playwright_stealth.properties._header_properties import HeaderProperties


@pytest.fixture
def fake_headers():
    """Fixture to generate fake headers with an additional 'origin' key if missing."""
    return FakeHttpHeader(domain_code="com", browser="chrome").as_header_dict()


@pytest.fixture
def brands():
    """Fixture for sample brand data."""
    return [{"brand": "BrandA", "version": "1"}, {"brand": "BrandB", "version": "2"}]


@pytest.fixture
def header_properties(fake_headers, brands):
    """Fixture to initialize HeaderProperties with fake headers and brands."""
    return HeaderProperties(brands=brands, dnt="1", **fake_headers)


def test_initialization(header_properties, fake_headers, brands):
    """Test that HeaderProperties initializes with correct attributes and values."""
    assert header_properties.user_agent == fake_headers["User-Agent"]
    assert header_properties.accept_language == fake_headers["Accept-language"]
    assert header_properties.accept_encoding == fake_headers["Accept-encoding"]
    assert header_properties.accept == fake_headers["Accept"]
    assert header_properties.referer == fake_headers["Referer"]
    assert header_properties.dnt == "1"
    assert header_properties.sec_ch_ua == header_properties._generate_sec_ch_ua(brands)
    assert (
        header_properties.sec_ch_ua_mobile
        == header_properties._generate_sec_ch_ua_mobile()
    )
    assert (
        header_properties.sec_ch_ua_platform
        == header_properties._generate_sec_ch_ua_platform()
    )
    assert (
        header_properties.sec_ch_ua_form_factors
        == header_properties._generate_sec_ch_ua_form_factors()
    )


def test_generate_sec_ch_ua_platform(header_properties):
    """Test _generate_sec_ch_ua_platform with various user agents."""
    test_cases = [
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "macOS"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Windows"),
        ("Mozilla/5.0 (X11; Linux x86_64)", "Linux"),
        ("Mozilla/5.0 (Unknown OS)", "Unknown"),
    ]
    for user_agent, expected_platform in test_cases:
        header_properties.user_agent = user_agent
        assert header_properties._generate_sec_ch_ua_platform() == expected_platform


def test_generate_sec_ch_ua(header_properties, brands):
    """Test _generate_sec_ch_ua generates correct string format."""
    ua_string = header_properties._generate_sec_ch_ua(brands)
    expected_string = '"BrandA";v="1","BrandB";v="2",'
    assert ua_string == expected_string


def test_generate_sec_ch_ua_mobile(header_properties):
    """Test _generate_sec_ch_ua_mobile returns expected value."""
    assert header_properties._generate_sec_ch_ua_mobile() == "?0"


def test_generate_sec_ch_ua_form_factors(header_properties):
    """Test _generate_sec_ch_ua_form_factors returns expected value."""
    assert header_properties._generate_sec_ch_ua_form_factors() == "desktop"


def test_as_dict(header_properties):
    """Test as_dict converts headers to kebab-case correctly and includes all keys."""
    headers_dict = header_properties.as_dict()
    expected_keys = {
        "user-agent",
        "accept-language",
        "accept-encoding",
        "accept",
        "referer",
        "dnt",
        "sec-ch-ua",
        "sec-ch-ua-mobile",
        "sec-ch-ua-platform",
        "sec-ch-ua-form-factors",
    }
    assert set(headers_dict.keys()) == expected_keys
    assert headers_dict["user-agent"] == header_properties.user_agent
    assert headers_dict["accept-language"] == header_properties.accept_language
    assert headers_dict["accept-encoding"] == header_properties.accept_encoding
    assert headers_dict["accept"] == header_properties.accept
    assert headers_dict["referer"] == header_properties.referer
    assert headers_dict["dnt"] == header_properties.dnt
    assert headers_dict["sec-ch-ua"] == header_properties.sec_ch_ua
    assert headers_dict["sec-ch-ua-mobile"] == header_properties.sec_ch_ua_mobile
    assert headers_dict["sec-ch-ua-platform"] == header_properties.sec_ch_ua_platform
    assert (
        headers_dict["sec-ch-ua-form-factors"]
        == header_properties.sec_ch_ua_form_factors
    )


@pytest.mark.parametrize(
    "user_agent,expected_platform",
    [
        ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "macOS"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Windows"),
        ("Mozilla/5.0 (X11; Linux x86_64)", "Linux"),
        ("Mozilla/5.0 (Unknown OS)", "Unknown"),
    ],
)
def test_generate_sec_ch_ua_platform_parametrized(user_agent, expected_platform):
    """Parametrized test for _generate_sec_ch_ua_platform."""
    header_properties = HeaderProperties(
        brands=[],
        dnt="1",
        **{
            "User-Agent": user_agent,
            "Accept-language": "",
            "Accept-encoding": "",
            "Accept": "",
            "Referer": "",
        }
    )
    assert header_properties._generate_sec_ch_ua_platform() == expected_platform


def test_missing_headers():
    """Test that HeaderProperties raises an error when required headers are missing."""
    with pytest.raises(KeyError):
        HeaderProperties(brands=[], dnt="1")
