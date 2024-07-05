from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='pdf-Creator-mr',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'reportlab',
    ],
    description='A simple library for creating PDFs in Python. USE: Django,tkinter....',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mateus Reis',
    author_email='mateussgp12@gmail.com',
    url='https://github.com/mateusdosreisf/pdf_generator',
)
