from setuptools import setup, find_packages

setup(
    name='SpeechToTextByAwais',
    version='0.1',
    author='Awais',
    author_email='tahirawais341@gmail.com',
    description='A Python library for converting speech to text with high accuracy.',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
    ],
)
