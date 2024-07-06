from setuptools import setup, find_packages

setup(
    name='validproxy',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Fidal',
    author_email='mrfidal@proton.me',
    description='A package to check the validity of proxies.',
    url='https://mrfidal.in/cyber-security/validproxy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
