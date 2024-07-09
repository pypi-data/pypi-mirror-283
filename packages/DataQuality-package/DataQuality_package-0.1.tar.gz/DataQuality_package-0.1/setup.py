from setuptools import setup, find_packages

setup(
    name='DataQuality_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # no dependencies for this example
    ],
    entry_points={
        'console_scripts': [
            'Quality=Quality.DataQuality:main',  # main is a function in calculate.py
        ],
    },
    author='Parveen Kaur',
    author_email='parveen.kaur@gds.ey.com',
    description='Package to perform Data Quality Check ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Pannu2095/DataQuality',
    license='MIT',
)
