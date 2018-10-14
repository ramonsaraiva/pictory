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
    license='MIT',
    description='simple tool to organize pictures and videos in lickable directories',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': ['pictory=pictory.pictory:main'],
    },
)
