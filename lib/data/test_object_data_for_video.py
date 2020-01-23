import os

from .object_data_for_video import ObjectDataForVideo


def test_init(tmpdir):
    ObjectDataForVideo(os.path.join(tmpdir, 'data.json'))


def test_append(tmpdir):
    od = ObjectDataForVideo(os.path.join(tmpdir, 'data.json'))
    od.append_none()
    od.append_data({'foo': 'bar'})

    assert len(od.data) == 2
