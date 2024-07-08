[![Downloads](https://img.shields.io/pypi/dm/slicertools)](https://pypi.org/project/slicertools/)
[![PyPI version](https://img.shields.io/pypi/v/slicertools)](https://pypi.org/project/slicertools/)
[![GitHub stars](https://img.shields.io/github/stars/pysashapy/slicertools?style=social)](https://github.com/pysashapy/slicertools)
# SlicerTools

slicertools - это библиотека на Python, разработанная для выполнения задач по нарезке и конвертации 3D-моделей, с акцентом на подготовку моделей для 3D-печати. Она предоставляет утилиты для работы с файлами 3D-моделей, взаимодействия с нарезочными движками, такими как CuraEngine, а также управления различными параметрами нарезки.

## Установка

Вы можете установить slicertools с помощью pip:

```bash
pip install slicertools
```
## Использование
### Конвертация 3D-моделей
Конвертируйте файл 3D-модели в другой формат:

```python
from slicertools.utils import convert_3d

converted_file = convert_3d('путь/к/вашей/3dмодели.stl')
print(f'Конвертированный файл: {converted_file}')
```
### Нарезка модели
Настройте нарезку 3D-модели с использованием предопределённых настроек качества:

```python
from dataclasses import asdict
from slicertools.enums import QualitySlice
from slicertools.materials import PETG
from slicertools.slicers import CuraSlicer

slicer = CuraSlicer(material=PETG())
result = slicer.slice('путь/к/вашей/модели.stl', **asdict(QualitySlice.STANDARD))
print(f'Результат нарезки:\n{result}')
```
## Особенности

- **Конвертация 3D-моделей:** Конвертация между различными форматами файлов 3D-моделей.
- **Нарезка моделей:** Интерфейс с движком CuraEngine для нарезки 3D-моделей для 3D-печати.
- **Предустановленные настройки качества:** Предопределённые настройки качества для эффективной нарезки.

## Зависимости

- trimesh[easy]
- CuraEngine