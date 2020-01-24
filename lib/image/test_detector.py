from .detector import Detector

import pytest
import numpy as np
import os


@pytest.mark.skipif(not os.path.exist('tf_hub_cache'), reason="No cached TF models")
def test_detection():
    d = Detector(module_handle="https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1")
    result = d.detect(np.zeros([10, 10, 3]))

    assert 'detection_boxes' in result
    assert 'detection_scores' in result
    assert 'detection_class_entities' in result
