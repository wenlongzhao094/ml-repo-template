from setuptools import find_packages, setup

setup(
    name="todo",  # TODO
    version="0.1.0",
    description="",  # TODO
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={"": "src"},
    python_requires=">=3.9.0",
    install_requires=[
        "numpy",
        "torch",
        "tqdm",  # Print looper progress
        "loguru",  # An easy-to-use logger
        "wandb",  # Keep track of experiments, especially hyperparameter sweeps
    ],
)
