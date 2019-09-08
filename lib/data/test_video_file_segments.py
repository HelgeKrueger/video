from .video_file_segments import VideoFileSegments


def test_unseen_none_for_empty_file():
    vfs = VideoFileSegments(filename='/tmp/test.csv')

    assert vfs.get_first_unseen() is None


def test_append_and_getting_last_entry():
    vfs = VideoFileSegments(filename='/tmp/test.csv')

    vfs.append_entry('one', [0, 1])
    vfs.append_entry('two', [4, 5])

    data = vfs.get_first_unseen()

    assert vfs.count_with_status('unseen') == 2
    assert vfs.count_with_status('processing') == 0

    assert data['filename'] == 'one'
    assert data['index'] == 0

    vfs.set_status(data['index'], 'processing')

    data = vfs.get_first_unseen()
    assert data['filename'] == 'two'
    assert data['index'] == 1

    assert vfs.count_with_status('unseen') == 1
    assert vfs.count_with_status('processing') == 1


def test_set_processing_to_done():
    vfs = VideoFileSegments(filename='/tmp/test.csv')

    vfs.append_entry('one', [0, 1])
    vfs.append_entry('two', [4, 5])

    data = vfs.get_first_unseen()
    vfs.set_status(data['index'], 'processing')

    data = vfs.get_first_unseen()
    vfs.set_status(data['index'], 'processing')

    assert (vfs.data['status'] == 'processing').sum() == 2

    vfs.update_status_from_to('processing', 'done')

    assert (vfs.data['status'] == 'processing').sum() == 0
    assert (vfs.data['status'] == 'done').sum() == 2
