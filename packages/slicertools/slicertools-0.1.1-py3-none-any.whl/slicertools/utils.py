import os
import sys

import trimesh

from slicertools.path import BASE_DIR


def cura_engine_path():
    if sys.platform == 'linux' or sys.platform == 'linux2':
        return os.path.join(BASE_DIR, 'engines', 'cura', 'linux', 'CuraEngine')
    elif sys.platform == 'win32':
        return os.path.join(BASE_DIR, 'engines', 'cura', 'windows', 'CuraEngine.exe')
    # elif sys.platform == 'darwin':
    #     return os.path.join(base_dir, 'engines', 'macos', 'CuraEngine')
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def convert_3d(file_path, directory='.', format='stl'):
    mesh = trimesh.load(file_path)
    output_name = f"{directory}/{file_path.split('/')[-1].rsplit('.', 1)[0]}.{format}"
    mesh.export(output_name)
    return output_name
