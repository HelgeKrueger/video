import pytest

from .style_transfer import StyleTransfer


@pytest.mark.skip("Long running")
def test_initialization():
    st = StyleTransfer()
