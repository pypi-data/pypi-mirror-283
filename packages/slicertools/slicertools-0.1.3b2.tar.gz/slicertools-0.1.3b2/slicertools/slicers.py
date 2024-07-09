import os
import uuid
from dataclasses import asdict
from io import BufferedWriter, BufferedReader

from slicertools.engines import CuraEngineSlicer
from slicertools.enums import SliceParameters, QualitySlice
from slicertools.materials import BaseMaterial
from slicertools.path import BASE_DIR
from slicertools.printers import Printers
from slicertools.results import SliceResult


class CuraSlicer(CuraEngineSlicer):
    def __init__(self, printer=Printers.ENDER_S1, material: BaseMaterial = None,
                 engine_path: str = None,  **slice_params):
        super().__init__(printer, engine_path)
        self.material = material or BaseMaterial()
        self.slice_params = slice_params or asdict(QualitySlice.STANDARD)

    def weight(self, volume_mm3):
        return volume_mm3 * self.material.density / 1000

    def slice(self, file: str | bytes, material: BaseMaterial = None, **kwargs) -> SliceResult:
        """
        Slice a 3D model using the specified material and slicing parameters.

        Args:
            file (Union[str, bytes]): The path to the STL file or the content of the STL file in bytes.
            material (BaseMaterial, optional): The material to use for slicing. Defaults to None.
            **kwargs: Additional slicing parameters.

        Returns:
            SliceResult: The result of the slicing process, including the material and slicing parameters.

        Raises:
            ValueError: If the file format is not STL.

        Example:
            slicer = CuraSlicer(material=PETG())
            result = slicer.slice('path/to/your/model.stl', quality=QualitySlice.STANDARD)
            print(result)
        """

        temp_file = None
        if isinstance(file, bytes):
            with open(BASE_DIR/'tmp'/(uuid.uuid1().hex+'.stl'), 'wb') as temp_file:
                temp_file.write(file)
                file = temp_file.name

        result = super().slice(file, **kwargs)
        result.material = material or self.material
        result.slice_params = SliceParameters(**self.slice_params_last)

        if isinstance(temp_file, BufferedWriter):
            os.remove(temp_file.name)
        return result

    @property
    def slice_params(self) -> SliceParameters:
        return SliceParameters(**self._slice_params)

    @slice_params.setter
    def slice_params(self, slice_params):
        self._slice_params.update(slice_params)
