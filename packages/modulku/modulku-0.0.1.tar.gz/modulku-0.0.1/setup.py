from setuptools import setup, find_packages

VERSION = '0.0.1'

def readme() -> str:
	with open(r'README.md') as f:
		README = f.read()
	return README

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python'
]

setup(
    name='modulku',
    version=VERSION,
    description='Modul pribadi',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/iewilmaestro/modulku_python',
    author='iewil',
    author_email='purna.iera@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['python php'],
    packages=find_packages(),
    install_requires=['']
)