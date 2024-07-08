from setuptools import setup, find_packages

setup(
    name='focused_unittest',
    version='0.1.1',
    description='Decorator to select only one unit test to be run.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Stan',
    author_email='barsv85@gmail.com',
    url='https://github.com/barsv/focused_unittest',
    py_modules=['focused_unittest'],
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
