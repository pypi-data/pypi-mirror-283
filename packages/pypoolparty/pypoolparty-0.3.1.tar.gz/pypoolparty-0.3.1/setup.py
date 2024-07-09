import setuptools
import os


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join("pypoolparty", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")

setuptools.setup(
    name="pypoolparty",
    version=version,
    description=(
        "A job pool for distributed compute clusters inspired by "
        "python's multoprocessing.Pool."
    ),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/pypoolparty",
    author="Sebastian Achim Mueller",
    author_email="sebastian-achim.mueller@mpi-hd.mpg.de",
    packages=[
        "pypoolparty",
        "pypoolparty.sun_grid_engine",
        "pypoolparty.slurm",
        "pypoolparty.slurm.array",
    ],
    package_data={
        "pypoolparty": [
            os.path.join("slurm", "tests", "resources", "*"),
            os.path.join("sun_grid_engine", "tests", "resources", "*"),
        ]
    },
    install_requires=[
        "qstat>=0.0.5",
        "json_lines>=0.5.0",
        "json_line_logger>=0.0.9",
        "rename_after_writing>=0.0.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
