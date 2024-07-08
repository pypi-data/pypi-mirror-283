import os
import subprocess
import uuid

from slicertools.printers import Printers
from slicertools.results import SliceResult
from slicertools.utils import cura_engine_path


class CuraEngineSlicer:

    def __init__(self, printer=Printers.ENDER_S1, engine_path: str = None):
        if engine_path is None:
            engine_path = cura_engine_path()
        self.printer = printer
        self._engine_path = engine_path
        self._slice_params = {}
        self.slice_params_last = {}

    def slice(self, file, **kwargs) -> SliceResult:
        self.slice_params_last = {**self._slice_params, **kwargs}
        extra_kwargs = {'gcode_path': f'.{uuid.uuid1()}.gcode', **self.slice_params_last}
        stdout, stderr = self.execute(self.slice_command(file, self.printer, **extra_kwargs))
        return self.result(stdout, **extra_kwargs)

    def result(self, data, **kwargs) -> SliceResult:
        result = SliceResult()
        for line in data.splitlines()[::-1]:
            line = line.strip()
            if "Print time (s)" in line:
                result.print_time = int(line.split(" ")[-1])
            elif "Filament (mm^3)" in line:
                result.volume = float(line.split(" ")[-1])
            if None not in [result.print_time, result.volume]:
                break
        gcode_path = kwargs.get('gcode_path')
        with open(gcode_path, mode="r") as gcode_file:
            result.gcode = gcode_file.read()
        os.remove(gcode_path)
        return result

    def slice_command(self, file, printer, gcode_path=None, **parameters):
        command = " ".join([
                               self._engine_path,
                               "slice",
                               f"-j {printer}",
                               f"-l {file}",
                           ] + [f"-s {key}={value}" for key, value in parameters.items() if value is not None])
        if gcode_path is not None:
            command += f' -o {gcode_path}'
        return command

    def execute(self, command, *args, **kwargs):
        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()
