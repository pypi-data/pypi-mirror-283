from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='inpass',
    version='2.0.0',
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='Automated login attempts for Instagram.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://mrfidal.in',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'inpass = inpass.cli:main',
        ],
    },
)
