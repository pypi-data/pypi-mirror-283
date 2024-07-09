from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Spiking Continues Time Neuron'
LONG_DESCRIPTION = 'A Spiking Neural Network implementation using '

with open("requirements.txt", "r", encoding="utf-8") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="sctn",
    version=VERSION,
    author="Yakir Hadad",
    author_email="yakir4123@email.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    keywords=['python', 'snn', 'ai'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)