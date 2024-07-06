from setuptools import setup, find_packages

setup(
    name='jaalvarez2818_airport_docs',
    version='0.8.4',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/jaalvarez2818/airport-docs',
    author='José Angel Alvarez Abraira',
    author_email='jaalvarez2818development@gmail.com',
    description='Generación de documentación y reportes requeridos por aeropuertos y/o aduanas para viajes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
