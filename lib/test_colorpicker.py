from .colorpicker import Colorpicker


def test_colorpicker_is_stable():
    colorpicker = Colorpicker()
    assert colorpicker.for_title('tree') == (255, 228, 196)
