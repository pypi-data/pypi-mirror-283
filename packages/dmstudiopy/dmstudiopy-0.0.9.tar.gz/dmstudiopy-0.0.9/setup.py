import os
import re
from setuptools import setup, find_packages

def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'version.py')
    try:
        with open(version_file) as f:
            version_line = f.read().strip()
        version_match = re.match(r"^__version__ = ['\"]([^'\"]*)['\"]", version_line)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")
    except Exception as e:
        raise RuntimeError(f"Error reading version file: {e}")

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='dmstudiopy',
    version=get_version(),
    author='Sean Horan, Renan Lopes',
    author_email='renanglopes@gmail.com',
    description='Python package for Datamine Studio scripting.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seanhoran/dmstudio',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pywin32',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries'
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', 'version.py'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/seanhoran/dmstudio/issues'
    },
)
