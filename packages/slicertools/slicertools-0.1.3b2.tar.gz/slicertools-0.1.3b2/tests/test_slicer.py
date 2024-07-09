from dataclasses import asdict

import pytest

from slicertools.enums import QualitySlice
from slicertools.materials import PETG, ABS
from slicertools.slicers import CuraSlicer


def test_slicing_result():
    slicer = CuraSlicer(material=PETG())
    result = slicer.slice(r'examples/models/xyzCalibration_cube.stl', **asdict(QualitySlice.ULTRA_QUALITY))

    assert result is not None
    assert result.print_time is not None and result.print_time > 0
    assert result.volume is not None and result.volume > 0
    assert result.gcode is not None and len(result.gcode)


def test_slicing_standard_quality():
    slicer = CuraSlicer(material=ABS())
    result = slicer.slice(r'examples/models/xyzCalibration_cube.stl', **asdict(QualitySlice.STANDARD))

    assert result is not None
    assert result.print_time is not None and result.print_time > 0
    assert result.volume is not None and result.volume > 0
    assert result.gcode is not None and len(result.gcode)


if __name__ == "__main__":
    pytest.main()
