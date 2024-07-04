""" Setup script for the Pyzo package.

Notes on how to do a release. Mostly for my own convenience:

* Write release notes
* Bump `__version__`
* Commit this to a new branch "bump" and push to GH. The CD freeze jobs will run.
* In online MacOS developer page, agree to license changes. Or certs won't work.
* Update freeze logic if necessary. Merge the pr.
* `git tag vx.y.z` and `git push vx.y.z` (builds the binaries and pushes to a GH release)
* Update links on Pyzo website
* `python setup.py sdist upload`

"""

import os
import sys

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup


def get_version_and_doc(filename):
    NS = dict(__version__="", __doc__="")
    docStatus = 0  # Not started, in progress, done
    with open(filename, "rb") as fd:
        data = fd.read()
    for line in data.decode().splitlines():
        if line.startswith("__version__"):
            exec(line.strip(), NS, NS)
        elif line.startswith('"""'):
            if docStatus == 0:
                docStatus = 1
                line = line.lstrip('"')
            elif docStatus == 1:
                docStatus = 2
        if docStatus == 1:
            NS["__doc__"] += line.rstrip() + "\n"
    if not NS["__version__"]:
        raise RuntimeError("Could not find __version__")
    return NS["__version__"], NS["__doc__"]


version, doc = get_version_and_doc(
    os.path.join(os.path.dirname(__file__), "pyzo", "__init__.py")
)


setup(
    name="pyzo",
    version=version,
    description="the Python IDE for scientific computing",
    long_description=doc,
    author="Almar Klein",
    author_email="almar.klein@gmail.com",
    license="2-Clause BSD",
    url="https://pyzo.org",
    keywords="Python interactive IDE Qt science computing",
    platforms="any",
    provides=["pyzo"],
    python_requires=">=3.6.0",
    install_requires=[],  # and 'PySide2' or 'PyQt5' or 'PySide6' or 'PyQt6'
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_dir={"pyzo": "pyzo"},
    package_data={
        "pyzo": [
            "resources/*.*",
            "resources/icons/*.*",
            "resources/appicons/*.*",
            "resources/images/*.*",
            "resources/fonts/*.*",
            "resources/themes/*.*",
            "resources/translations/*.*",
        ]
    },
    data_files=[
        ("", ["README.md", "LICENSE.md", "pyzo.appdata.xml", "pyzolauncher.py"])
    ],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points={
        "console_scripts": [
            "pyzo = pyzo.__main__:main",
        ],
    },
)


# Post processing:
# Install appdata.xml on Linux if we are installing in the system Python
if sys.platform.startswith("linux") and sys.prefix.startswith("/usr"):
    if len(sys.argv) >= 2 and sys.argv[1] == "install":
        fname = "pyzo.appdata.xml"
        filename1 = os.path.join(os.path.dirname(__file__), fname)
        filename2 = os.path.join("/usr/share/metainfo", fname)
        try:
            with open(filename1, "rb") as fd:
                bb = fd.read()
            with open(filename2, "wb") as fd:
                fd.write(bb)
        except PermissionError:
            pass  # No sudo, no need to warn
        except Exception as err:
            print("Could not install {}: {}".format(fname, err))
        else:
            print("Installed", fname)
