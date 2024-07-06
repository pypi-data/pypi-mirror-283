from setuptools import setup, find_packages
import os
import re

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
    name='minresourcepy',
    version=get_version(),
    description='Tools for Resource Geologists',
    url='https://github.com/renanlo/MinResourcepy',
    author='Renan Lopes',
    author_email='renanglopes@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy>=1.24.3',
        'pandas>=2.0.3',
        'transforms3d>=0.4.1',
        'plotly>=5.9.0',
        'matplotlib>=3.7.2'
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
    packages=find_packages(),
    package_data={
        '': ['*.txt', '*.md', 'version.py'],
    },
)