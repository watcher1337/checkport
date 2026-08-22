from setuptools import setup

setup(
    name="checkport",
    version="2.0.0",
    py_modules=["checkport"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "checkport=checkport:main",
        ],
    },
    author="watcher1337",
    description="Port management tool for checking and killing processes on specific ports",
    url="https://github.com/watcher1337/checkport",
    python_requires=">=3.8",
)
