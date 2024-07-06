from setuptools import setup,find_packages

setup(
    name='Abhay-STT',
    version='0.1',
    author='Abhay Agnihotri',
    author_email='abhayagnihotri976@gmail.com',
    description='A package to convert speech to text using selenium created by Abhay'
)

packages=find_packages(),
install_requirements = [
    'selenium',
    'webdriver-manager'
]
