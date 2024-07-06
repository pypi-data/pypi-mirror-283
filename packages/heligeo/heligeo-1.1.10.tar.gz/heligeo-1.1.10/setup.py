import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="heligeo",
    version="1.1.10",
    description="Python client for requests to heligeo API services",
    long_description=README,
    long_description_content_type="text/markdown",

    author="Heliware",
    author_email=" rajan@heliware.co.in",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["heligeo"],
    include_package_data=True,
    install_requires=["numpy","Shapely","plotly","requests","dash","pandas","dash-bootstrap-components","kml2geojson","geo2kml","ezdxf","pyshp"],

)