from setuptools import setup, find_packages
from ocelotz import constants

setup(
    name='ocelotz',
    version=constants.OCELOT_VERSION,
    packages=find_packages(),
    install_requires=[
        'pyfiglet',
        'emoji',
        'SimpleITK',
        'natsort',
        'numpy==1.26.0',
        'pydicom',
        'tqdm',
        'rich',
        'requests',
        'moosez==2.4.0',
        'pandas',
        'dicom2nifti',
        'six'
    ],
    entry_points={
        'console_scripts': [
            'ocelotz = ocelotz.ocelotz:main'
        ],
    },
    author='Sebastian Gutschmayer',
    author_email='sebastian.gutschmayer@meduniwien.ac.at',
    description=' OCELOT: diffeOmorphiC rEgistration for voxel-wise anOmaly Tracking - a tool to generate cohort specific normative PET/CT images.',
    url='https://github.com/Keyn34/OCELOT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10'
    ],
)
