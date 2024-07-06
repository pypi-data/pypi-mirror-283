from setuptools import setup, find_packages

setup(
    name='pypawn_annotations',
    version='1.0.0.2',
    packages=find_packages(),
    author='bonkibon',
    author_email='bonkibon75@gmail.com',
    description='pypawn-annotations',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    url='https://github.com/bonkibon-education/pypawn-annotation',
    download_url='https://github.com/bonkibon-education/pypawn-annotations/archive/refs/tags/1.0.0.zip',
    license='GPL-3.0 license, see LICENSE file',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
)
