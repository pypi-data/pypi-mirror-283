from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='houlang',
    version='0.0.5',
    author='Colin Brisson',
    author_email='colibrisson@gmail.com',
    description='Houlang is a package for Chinese historical documents automatic transcription.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['houlang']),
    install_requires=[
        'kraken>=5.0',
        'ultralytics>=8.0',
        'scikit-learn',
    ],
    python_requires='>=3.8, <3.12',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='historical documents, classical chinese, automatic transcription, OCR',

)