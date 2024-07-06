# setup.py

from setuptools import setup, find_packages

setup(
    name="am_i_normal",
    version="0.1.0",
    author="mike-rollout",
    description="Are you normal? Time to find out",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mike-rollout/py-am_i_normal",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
