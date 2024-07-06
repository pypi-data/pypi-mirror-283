from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='validproxy',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A package to check the validity of proxies.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://mrfidal.in/cyber-security/validproxy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
