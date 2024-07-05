from setuptools import setup

setup(
    name="trainlogger",
    version="0.1.2",
    description="A Python package",
    url="https://github.com/jonas-sth/trainlogger",
    author="Jonas Steinhäuser",
    author_email="",
    license="",
    packages=["trainlogger"],
    install_requires=["numpy",                     
                      "torch",
                      "torchmetrics",
                      "tqdm",
                      "pandas",
                      "tensorflow"],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
    ],
)
