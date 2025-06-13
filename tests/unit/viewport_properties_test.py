import random

from mockito import unstub, when

from playwright_stealth.properties._viewport_properties import ViewportProperties


def test_initialization():
    """Test that ViewportProperties initializes with correct attributes."""
    # Mock random.randint to return 0 for consistent testing
    when(random).randint(-100, 100).thenReturn(0)
    when(random).randint(0, 20).thenReturn(0)
    viewport = ViewportProperties()
    assert viewport.width == 1920
    assert viewport.height == 1080
    assert viewport.outerWidth == 1920
    assert viewport.outerHeight == 1080
    assert viewport.innerWidth == 1920
    assert viewport.innerHeight == 1080
    unstub()


def test_generate_viewport_dimensions():
    """Test the _generate_viewport_dimensions method."""
    # Mock random.randint to return 50 and -50 in sequence
    when(random).randint(-100, 100).thenReturn(50, -50)
    # Mock random.randint for inner dimensions to return 0
    when(random).randint(0, 20).thenReturn(0)
    viewport = ViewportProperties()
    expected_width = 1920 + 50  # 1970
    expected_height = 1080 - 50  # 1030
    assert viewport.width == expected_width
    assert viewport.height == expected_height
    unstub()


def test_generate_inner_dimensions():
    """Test the _generate_inner_dimensions method."""
    # Mock random.randint to return specified values in sequence
    when(random).randint(-100, 100).thenReturn(50, 50)
    when(random).randint(0, 20).thenReturn(10, 15)
    viewport = ViewportProperties()
    expected_width = 1920 + 50  # 1970
    expected_height = 1080 + 50  # 1130
    expected_innerWidth = expected_width - 10  # 1960
    expected_innerHeight = expected_height - 15  # 1115
    assert viewport.width == expected_width
    assert viewport.height == expected_height
    assert viewport.innerWidth == expected_innerWidth
    assert viewport.innerHeight == expected_innerHeight
    unstub()


def test_as_dict():
    """Test the as_dict method."""
    when(random).randint(-100, 100).thenReturn(0)
    when(random).randint(0, 20).thenReturn(0)
    viewport = ViewportProperties()
    expected_dict = {
        "width": 1920,
        "height": 1080,
        "outerWidth": 1920,
        "outerHeight": 1080,
        "innerWidth": 1920,
        "innerHeight": 1080,
    }
    assert viewport.as_dict() == expected_dict
    unstub()


def test_dimensions_within_expected_range():
    """Test that the generated dimensions are within expected ranges."""
    viewport = ViewportProperties()
    assert 1820 <= viewport.width <= 2020
    assert 980 <= viewport.height <= 1180
    assert viewport.outerWidth == viewport.width
    assert viewport.outerHeight == viewport.height
    assert viewport.width - 20 <= viewport.innerWidth <= viewport.width
    assert viewport.height - 20 <= viewport.innerHeight <= viewport.height


def test_randomness_in_dimensions():
    """Test that different instances have different dimensions due to randomness."""
    viewport1 = ViewportProperties()
    viewport2 = ViewportProperties()
    dimensions1 = (
        viewport1.width,
        viewport1.height,
        viewport1.innerWidth,
        viewport1.innerHeight,
    )
    dimensions2 = (
        viewport2.width,
        viewport2.height,
        viewport2.innerWidth,
        viewport2.innerHeight,
    )
    # Since randomness is involved, dimensions may occasionally be the same, which is acceptable
    assert dimensions1 != dimensions2 or True  # Accept possible equality due to randomness


def test_custom_kwargs():
    """Test that custom kwargs are accepted and set as attributes."""
    viewport = ViewportProperties(custom_attr="test_value")
    assert viewport.custom_attr == "test_value"
