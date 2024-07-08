from setuptools import setup, find_packages

setup(
    name='pystudio',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'moviepy',
        'pydub',
        'numpy',
        'scipy',
        'speechrecognition',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            # Example entry point: 'pystudio-cli=pystudio.module:main',
        ],
    },
    author='Contentify AI',
    author_email='hi@contentify.app',
    description='PyStudio is a versatile video and audio processing package designed for creating, editing, and managing multimedia content. It leverages popular libraries such as MoviePy, Pydub, NumPy, and Scipy to provide powerful tools for handling audio and video files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alphatrait/pystudio',  # Update this with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
