# setup.py

from setuptools import setup, find_packages

setup(
    name="syncontrol",  # Replace with your package name
    version="0.2",
    author="Henry Dalgleish",
    author_email="hwpdalgleish@gmail.com",
    description="Python package for synthetic control generation and testing",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=["pandas"
                    ,"numpy"
                    ,"seaborn"
                    ,"matplotlib"
                    ,"rpy2"
                    ,"statsmodels"
                    ,"scipy"
                    ,"python-dateutil"
                    ]
)
