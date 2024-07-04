from setuptools import setup, find_packages

setup(
    name='acuiferoec',
    version='0.1.0',
    description='Calcula el volumen de agua almacenada en un sistema de acuíferos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=('Santiago Quiñones', 'Luis Cuenca'),
    author_email='lsquinones@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
