from dataclasses import dataclass


class PrintPattern:
    LINEAR = 'linear'
    GRID = 'grid'
    CYCLONE_SPIRAL = 'cyclone_spiral'
    CONTOUR = 'contour'
    HILBERT_CURVE = 'hilbert_curve'
    ZIG_ZAG = 'zig_zag'
    CROSS = 'cross'
    CROSS_3D = 'cross_3d'
    STRIPED = 'striped'
    ARCHIMEDEAN_CHORD = 'archimedean_chord'


@dataclass
class SliceParameters:
    pattern: str = PrintPattern.LINEAR
    speed_print: int = 60
    layer_height: float = None
    wall_thickness: float = None
    infill_density: int = 20
    roofing_layer_count: int = 3
    center_object: bool = True
    auto_position: bool = True
    bed_size: str = '9999,9999'


class QualitySlice:
    DRAFT = SliceParameters(
        speed_print=80,
        infill_density=10,
        layer_height=0.3,
        wall_thickness=1.2
    )

    STANDARD = SliceParameters(
        speed_print=60,
        infill_density=20,
        layer_height=0.2,
        wall_thickness=1.0
    )

    SUPER = SliceParameters(
        speed_print=40,
        infill_density=30,
        layer_height=0.1,
        wall_thickness=0.8
    )

    HIGH_QUALITY = SliceParameters(
        speed_print=30,
        infill_density=40,
        layer_height=0.05,
        wall_thickness=0.6
    )

    ULTRA_QUALITY = SliceParameters(
        speed_print=20,
        infill_density=50,
        layer_height=0.02,
        wall_thickness=0.4
    )