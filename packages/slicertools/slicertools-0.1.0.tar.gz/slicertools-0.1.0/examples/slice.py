from dataclasses import asdict

from slicertools.enums import QualitySlice
from slicertools.materials import PETG
from slicertools.slicers import CuraSlicer


slicer = CuraSlicer(material=PETG())
result = slicer.slice(r'models/xyzCalibration_cube.stl', **asdict(QualitySlice.ULTRA_QUALITY))
print(result)
