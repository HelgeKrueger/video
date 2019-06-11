from .video_file_segments import VideoFileSegments

def test_append_and_getting_last_entry():
    vfs = VideoFileSegments(filename='/tmp/test.csv')

    vfs.append_entry('one', [0, 1])
    vfs.append_entry('two', [4, 5])

    data = vfs.get_first_unseen()

    assert data['filename'] == 'one'
    assert data['index'] == 0

    vfs.set_status(data['index'], 'processing')

    data = vfs.get_first_unseen()
    assert data['filename'] == 'two'
    assert data['index'] == 1
