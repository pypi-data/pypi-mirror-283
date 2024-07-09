[![Downloads](https://img.shields.io/pypi/dm/slicertools)](https://pypi.org/project/slicertools/)
[![PyPI version](https://img.shields.io/pypi/v/slicertools)](https://pypi.org/project/slicertools/)
[![GitHub stars](https://img.shields.io/github/stars/pysashapy/slicertools?style=social)](https://github.com/pysashapy/slicertools)
# SlicerTools

slicertools is a Python library designed for 3D model slicing and conversion tasks, particularly focused on preparing models for 3D printing. It provides utilities for handling 3D model files, interfacing with slicing engines like CuraEngine, and managing various slicing parameters.

## Installation

You can install slicertools using pip:

```bash
pip install slicertools
```

## Usage
### Convert 3D Models
Convert a 3D model file to another format:

```python
from slicertools.utils import convert_3d

converted_file = convert_3d('path/to/your/3dmodel.stl')
print(f'Converted file: {converted_file}')
```
### Slice a Model
Slice a 3D model using pre-defined quality settings:
```python
from dataclasses import asdict
from slicertools.enums import QualitySlice
from slicertools.materials import PETG
from slicertools.slicers import CuraSlicer

slicer = CuraSlicer(material=PETG())
result = slicer.slice('path/to/your/model.stl', **asdict(QualitySlice.STANDARD))
print(f'STANDARD Slice result:\n{result}')
result = slicer.slice(open('models/xyzCalibration_cube.stl', 'rb').read(), **asdict(QualitySlice.ULTRA_QUALITY))
print(f'ULTRA QUALITY Slice result:\n{result}')
```
## Features

- **3D Model Conversion:** Convert between various 3D model file formats.
- **Model Slicing:** Interface with CuraEngine to slice 3D models for 3D printing.
- **Quality Presets:** Pre-defined quality settings for efficient slicing.

## Dependencies

- trimesh[easy]
- CuraEngine