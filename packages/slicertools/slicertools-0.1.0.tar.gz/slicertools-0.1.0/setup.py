from setuptools import setup, find_packages

setup(
    name='slicertools',
    version='0.1.0',
    description='A library for slicing 3D models for 3D printing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexander Ibragimov',
    author_email='sasha.2000ibr@example.com',
    url='https://github.com/pysashapy/slicertools',
    packages=find_packages(),
    install_requires=[
        'trimesh[easy]'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.9',
    include_package_data=True,
)
