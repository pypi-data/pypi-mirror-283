from setuptools import setup, find_packages

setup(
    name="arabic_ocr_online",
    version='1.5',
    packages= find_packages(),
    install_requires=[
        'easyocr >=1.7.1',
        'numpy >= 1.26.4',
        'requests >= 2.32.2',
        'opencv-python >= 4.9.0.80'
    ]
)