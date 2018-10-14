from setuptools import setup, find_packages

setup(
    name='pictory',
    version='0.1.0',
    url='https://github.com/ramonsaraiva/pictory',
    author='Ramon Saraiva',
    author_email='ramonsaraiva@gmail.com',
    description='simple tool to organize pictures and videos in lickable directories',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pictory=pictory.pictory:main'],
    }
)
