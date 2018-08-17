from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='advice',
    version='0.1.0',
    description='Aspect-oriented programming',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/orsinium/advice',
    author='@orsinium',
    author_email='master_fess@mail.ru',
    keywords=(
        'aspect oriented programming advice joinpoint '
        'patching import decorators logging testing extension'
    ),

    packages=['advice'],
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },

    # project_urls={
    #     'Documentation': '',
    # },

    # https://pypi.org/classifiers/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Software Development',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Mocking',
        'Topic :: System :: Logging',
    ],
)
