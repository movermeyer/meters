#!/usr/bin/env python


import setuptools
import meters.const


##### Main #####
if __name__ == "__main__":
    setuptools.setup(
        name="meters",
        version=meters.const.VERSION,
        url=meters.const.UPSTREAM_URL,
        license="LGPLv3",
        author="Devaev Maxim",
        author_email="mdevaev@gmail.com",
        description="Yet another metrics library",
        platforms="any",

        packages=(
            "meters",
            "meters/handlers",
        ),

        classifiers=( # http://pypi.python.org/pypi?:action=list_classifiers
            "Development Status :: 2 - Pre-Alpha",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Networking :: Monitoring",
        ),
    )

