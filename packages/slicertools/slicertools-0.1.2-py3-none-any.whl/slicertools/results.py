import textwrap
from dataclasses import dataclass

from slicertools.enums import SliceParameters
from slicertools.materials import BaseMaterial


@dataclass
class SliceResult:
    print_time: int = None
    volume: float = None
    material: BaseMaterial = None
    gcode: str = ""
    slice_params: SliceParameters = None

    def __str__(self):
        gcode_display = textwrap.shorten(self.gcode, 50)
        return (f"SliceResult(print_time={self.print_time}, volume={self.volume}, "
                f"weight={self.weight}, gcode='{gcode_display}'), slice_params={self.slice_params}")

    @property
    def weight(self):
        return self.volume / self.material.density / 1000
