from setuptools import setup, find_packages

setup(
    name='cpstools',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'biopython==1.78',
        'numpy==1.26.4',
    ],
    entry_points={
        'console_scripts': [
            'cpstools=cpstools.cmdline:main',
        ],
    },
    author='Xu Wenbo',
    author_email='xwb7533@163.com',
    description='CPStools is a package for analyzing chloroplast genome sequences.',
    url='https://github.com/Xwb7533/CPStools',
)