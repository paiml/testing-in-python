import pytest
import sys
import cli

def test_help_output_is_generated(capsys):
    sys.argv = ['cli.py', '-h']
    with pytest.raises(SystemExit):
        cli.main()
    out, err = capsys.readouterr()
    assert 'usage: cli [-h] [--foo FOO]' in out
    assert '--foo FOO   the foo option!' in out

