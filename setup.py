from setuptools import (
    find_packages,
    setup,
)


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='pictory',
    version='0.1.0',
    url='https://github.com/ramonsaraiva/pictory',
    author='Ramon Saraiva',
    author_email='ramonsaraiva@gmail.com',
    description='simple tool to organize pictures and videos in lickable directories',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pictory=pictory.pictory:main'],
    }
)
