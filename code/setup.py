from setuptools import setup, find_packages

setup(
    name='testvalidator',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # List your project dependencies here,
        # e.g., 'requests', 'argparse', etc.
    ],
    entry_points={
        'console_scripts': [
            'testvalidator=main:main',
        ],
    },
)
