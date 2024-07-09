import os

import pytest

from slicertools.utils import convert_3d


def test_conversion():
    converted_file = convert_3d('examples/models/lpwkull_2.3mf')
    assert converted_file is not None
    assert os.path.exists(converted_file)
    os.remove(converted_file)


if __name__ == "__main__":
    pytest.main()
