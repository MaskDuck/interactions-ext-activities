from setuptools import setup

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
packages = [
    "interactions.ext.autosharder",
]
setup(
    name='interactions-ext-autosharder',
    version='0.0.1a1',
    description='An interactions.py extension to help you shard your bot',  # noqa: E501
    long_description=open('README.md').read(),
    url='',
    author='MaskDuck',
    license='MIT',
    classifiers=classifiers,
    keywords='autoshard',
    packages=packages,
    long_description_content_type='text/markdown',
    install_requires=['discord-py-interactions']
)