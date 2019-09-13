from .meta_information import MetaInformation


def test_creation():
    mi = MetaInformation(filename='/tmp/test.csv')

    mi.append_entry('blub', 'foo', 'bar')

    assert mi.data is not None
