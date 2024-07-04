from setuptools import setup, find_packages

setup(
    name='daiso',
    version='0.0.6',
    description='DAISO: Deep-learning Assistance for Inspection, Supervision, and Optimization',
    author='Taphy',
    author_email='yhpat1@gmail.com',
    url='https://sclab.yonsei.ac.kr/',
    install_requires=['pyyaml', 'numpy', 'torch',],
    packages=find_packages(exclude=[]),
    keywords=['daiso', 'Daiso', 'logger', 'tool', 'deep learning', 'wandb', "grad"],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)