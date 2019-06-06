from colorpicker import Colorpicker


def test_blub():
    colorpicker = Colorpicker()
    assert colorpicker.for_title('tree') == (255, 228, 196)
