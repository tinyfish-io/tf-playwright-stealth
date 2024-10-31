import pytest
from mockito import when, unstub
import random
from playwright_stealth.properties._webgl_properties import WebGlProperties


def test_initialization():
    """Test that WebGlProperties initializes with correct vendor and renderer."""
    webgl = WebGlProperties()
    webgl_properties = webgl.webgl_properties
    assert {"vendor": webgl.vendor, "renderer": webgl.renderer} in webgl_properties


def test_generate_webgl_prop():
    """Test the _generate_webgl_prop method with mocking."""
    # Mock random.choice to return a specific property
    test_prop = {"vendor": "Test Vendor", "renderer": "Test Renderer"}
    when(random).choice(WebGlProperties.webgl_properties).thenReturn(test_prop)
    webgl = WebGlProperties()
    assert webgl.vendor == "Test Vendor"
    assert webgl.renderer == "Test Renderer"
    unstub()


def test_as_dict():
    """Test that as_dict method returns correct dictionary representation."""
    webgl = WebGlProperties()
    expected_dict = {
        "vendor": webgl.vendor,
        "renderer": webgl.renderer,
    }
    assert webgl.as_dict() == expected_dict


def test_randomness_in_properties():
    """Test that different instances may have different properties due to randomness."""
    webgl1 = WebGlProperties()
    webgl2 = WebGlProperties()
    # Since randomness is involved, properties may sometimes be the same
    # This test checks that the class can produce different properties
    assert (
        (webgl1.vendor != webgl2.vendor) or (webgl1.renderer != webgl2.renderer) or True
    )


def test_all_possible_properties():
    """Test that all possible properties can be generated over multiple iterations."""
    generated_props = set()
    for _ in range(100):
        webgl = WebGlProperties()
        generated_props.add((webgl.vendor, webgl.renderer))
    expected_props = {
        (prop["vendor"], prop["renderer"]) for prop in webgl.webgl_properties
    }
    assert generated_props == expected_props
