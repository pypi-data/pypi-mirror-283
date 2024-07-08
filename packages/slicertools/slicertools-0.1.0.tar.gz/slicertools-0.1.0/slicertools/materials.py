class BaseMaterial:
    material = None
    printing_temperature = None
    density = 1


class PLA(BaseMaterial):
    material = "PLA"
    printing_temperature = "190-220°C"
    density = 1.24


class ABS(BaseMaterial):
    material = "ABS"
    printing_temperature = "220-250°C"
    density = 1.04


class PETG(BaseMaterial):
    material = "PETG"
    printing_temperature = "230-250°C"
    density = 1.27


class Nylon(BaseMaterial):
    material = "Nylon"
    printing_temperature = "230-260°C"
    density = 1.15


class TPU(BaseMaterial):
    material = "TPU"
    printing_temperature = "220-250°C"
    density = 1.2
