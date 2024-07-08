from dataclasses import asdict

from slicertools.engines import CuraEngineSlicer
from slicertools.enums import SliceParameters, QualitySlice
from slicertools.materials import BaseMaterial
from slicertools.printers import Printers


class CuraSlicer(CuraEngineSlicer):
    def __init__(self, printer=Printers.ENDER_S1, material: BaseMaterial = None, engine_path: str = None,  **slice_params):
        super().__init__(printer, engine_path)
        self.material = material or BaseMaterial()
        self.slice_params = slice_params or asdict(QualitySlice.STANDARD)

    def weight(self, volume_mm3):
        return volume_mm3 * self.material.density / 1000

    def slice(self, *args, material: BaseMaterial = None, **kwargs):
        result = super().slice(*args, **kwargs)
        result.material = material or self.material
        result.slice_params = SliceParameters(**self.slice_params_last)
        return result

    @property
    def slice_params(self) -> SliceParameters:
        return SliceParameters(**self._slice_params)

    @slice_params.setter
    def slice_params(self, slice_params):
        self._slice_params.update(slice_params)
