from setuptools import setup, find_packages

setup(
    name="my_pm10_predictor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "tensorflow",
        "keras"
    ],
)
