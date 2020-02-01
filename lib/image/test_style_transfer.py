import pytest
import numpy as np

from .style_transfer import StyleTransfer


@pytest.mark.skip("Long running")
def test_running():
    st = StyleTransfer()
    st.transform_frame(np.zeros([300, 300, 3]))
