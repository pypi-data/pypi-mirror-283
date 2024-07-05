from setuptools import setup, find_packages

setup(
    name="PanelOLSPipeline",
    version="0.1.0",
    author="Gaurav M",
    author_email="gaurav.mohindroo9@gmail.com",
    description="A package to preprocess data, fit models, and calculate VIF for Panel Data Regression",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GrimmXoXo/OLS_package",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "statsmodels",
        "scikit-learn",
        "linearmodels",
        "joblib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
