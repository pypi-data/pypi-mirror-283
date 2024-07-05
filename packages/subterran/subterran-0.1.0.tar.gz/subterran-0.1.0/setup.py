from setuptools import setup, find_packages

setup(
    name='subterran',
    version='0.1.0',
    description='Calcula el volumen de agua almacenada en un sistema de acuíferos.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Santiago Quiñones',
    author_email='lsquinones@gmail.com',
    url='https://github.com/yourusername/acuiferoec',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.24.1',
    ],
)


