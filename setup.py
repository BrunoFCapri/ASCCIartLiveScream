from setuptools import setup, find_packages

setup(
    name='ascii-screen-capture-threaded',
    version='0.1.0',
    author='Bruno',
    author_email='bruno.fabian.capri.oficial@gmail.com',
    description='A Python application that captures the screen in real-time and converts it to ASCII art using multithreading for improved performance.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/ascii-screen-capture-threaded',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Pillow',
        'pyautogui',
        'colorama',
        'numpy',  # Add any additional dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)