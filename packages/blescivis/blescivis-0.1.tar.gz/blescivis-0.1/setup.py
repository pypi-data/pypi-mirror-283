from setuptools import setup, find_packages

setup(
    name='blescivis',
    version='0.1',
    packages=find_packages(),
    install_requires=['numpy==1.24.3'],
    author='Pere Rosselló',
    author_email='per.rossello@gmail.com',
    description='A package with tailored functions for scientific visualization in Blender via scripting through Blender\'s Python API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pererossello/blescivis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)