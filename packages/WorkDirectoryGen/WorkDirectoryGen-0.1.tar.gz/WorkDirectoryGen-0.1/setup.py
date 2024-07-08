# setup.py

from setuptools import setup, find_packages

setup(
    name='WorkDirectoryGen',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytesseract',
        'Pillow',
        'PyPDF2'
    ],
    entry_points={
        'console_scripts': [
            'WorkDirectoryGen=WorkDirectoryGen.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
