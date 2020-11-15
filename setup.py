from setuptools import setup

__version__ = '0.0.1'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lcu-driver',
    version=__version__,
    author='André Sousa',
    author_email='andrematosdesousa@gmail.com',
    license='MIT',
    url='https://github.com/sousa-andre/requests-limiter/',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=['limiter'],
    install_requires=[],
    project_urls={
        'Source': 'https://github.com/sousa-andre/requests-limiter/'
    }
)
