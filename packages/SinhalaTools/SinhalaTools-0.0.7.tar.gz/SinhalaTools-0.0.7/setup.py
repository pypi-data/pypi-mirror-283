from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='SinhalaTools',
    version='0.0.7',
    packages=find_packages(),
    install_requires=[
        'requests'
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    description='Sinhala Tools for converting Sinhala text to Roman and vice versa.',
    author='Tharindu Madhusanka Wimalasena',
    author_email='tharindu.20@cse.mrt.ac.lk',
    url='https://github.com/TharinduMadhusanka',
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
