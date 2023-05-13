from setuptools import setup

__VERSION__ = "1.0.0"

def get_requirements(file_path):
    with open(file_path, 'r') as f:
        requirements = f.read().splitlines()
    return requirements

setup(
    name = "nrtui",
    packages=['nrtui', 'nrtui.lib'],
    version = __VERSION__,
    description = "simple no recoil for linux written in python",
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    author = "V2BlockBuster2K",
    url = "https://github.com/V2BlockBuster2K/nrtui",
    license = "GPLv3",

    entry_points={
        'console_scripts': ['nrtui=nrtui.nrtui:main']
    },
    classifiers = [
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux'
    ],
    install_requires=get_requirements('requirements.txt'),
)
