from . import commands


def test_check_structure_of_commands():
    assert isinstance(commands, dict)

    for key, value in commands.items():
        assert isinstance(value, dict)
        assert 'help' in value
        assert 'func' in value
        assert isinstance(value['help'], str)
        assert callable(value['func'])
