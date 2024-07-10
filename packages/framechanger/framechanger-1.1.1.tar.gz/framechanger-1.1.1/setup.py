from setuptools import setup, find_packages

setup(
    name="framechanger",
    version="1.1.1", 
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "requests",
        "pyqt5",
    ],
    entry_points={
        "console_scripts": [
            "framechanger=framechanger.app:run",
        ],
    },
    package_data={
        "framechanger": ["icon.ico"],
    },
)
