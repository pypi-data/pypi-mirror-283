# coding: utf8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-09 16:38:27 UTC+8
"""

import os
import subprocess
import sys
import setuptools
import requests

from datetime import datetime
from typing import Literal
from importlib.resources import read_text


_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
_RELEASE_LEVEL = ["release", "test", "alpha", "beta"]
_major = 1
_minor = 1
_micro = 0
releaselevel: Literal["release", "test", "alpha", "beta"] = "release"

if sys.version_info < (3, 8):
    sys.exit("Python 3.8 or higher is required.")


class InstallDependenciesCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = "python -m pip install --force git+https://github.com/imba-tjd/pip-autoremove@ups"
        subprocess.call(command, shell=True)


class PackageInfo(object):
    """
    Public package

    :param major: major num
    :type major: int
    :param minor: minor num
    :type minor: int
    :param micro: stage num
    :type micro: int
    :param revise: revise num
    :type revise: int
    :param releaselevel: version mark
    :type releaselevel: str
    """

    def __init__(self, major: int, minor: int, micro: int, releaselevel: str):
        self.major = self.vaildate_param(major, int)
        self.minor = self.vaildate_param(minor, int)
        self.micro = self.vaildate_param(micro, int)
        self.serial = self.get_github_serial()

        if releaselevel.lower() not in ("release", "test", "alpha", "beta"):
            raise TypeError('Param: releaselevel type error, releaselevel must in ["release", "test", "alpha", "beta"].')

        self.releaselevel = releaselevel

    @property
    def name(self):
        return "PyFairylandFuture"

    @property
    def author(self):
        return "Lionel Johnson"

    @property
    def email(self):
        return "fairylandfuture@outlook.com"

    @property
    def url(self):
        return "https://github.com/PrettiestFairy/pypi-fairylandfuture"

    @property
    def version(self):
        self.serial = self.serial.__str__()

        date_str = datetime.now().date().__str__().replace("-", "")
        revise_after = "-".join((self.serial.__str__(), date_str))
        release_version = ".".join((self.major.__str__(), self.minor.__str__(), self.micro.__str__()))

        if self.releaselevel == "release":
            version = release_version
        elif self.releaselevel == "test":
            version = ".".join((release_version, "".join(("rc.", revise_after))))
        elif self.releaselevel == "alpha":
            version = ".".join((release_version, "".join(("alpha.", revise_after))))
        elif self.releaselevel == "beta":
            version = ".".join((release_version, "".join(("beta.", revise_after))))
        else:
            version = ".".join((release_version, "".join(("rc.", revise_after))))

        return version

    @property
    def description(self):
        return "Efficient developed Python library."

    @property
    def long_description(self):
        with open(os.path.join(_ROOT_PATH, "README.md"), "r", encoding="UTF-8") as stream:
            long_description = stream.read()

        return long_description

    @property
    def long_description_content_type(self):
        return "text/markdown"

    @property
    def packages_include(self):
        include = ("fairylandfuture", "fairylandfuture.*")

        return include

    @property
    def packages_exclude(self):
        exclude = (
            "bin",
            "conf",
            "deploy",
            "docs",
            "scripts",
            "temp",
            "test",
            # "fairylandfuture/test",
        )

        return exclude

    @property
    def packages_data(self):
        data = {"": ["*.txt", "*.rst", "*.md"], "fairylandfuture": ["conf/**"]}

        return data

    @property
    def fullname(self):
        return self.name + self.version

    @property
    def python_requires(self):
        return ">=3.8"

    @property
    def keywords(self):
        return [
            "fairyland",
            "Fairyland",
            "pyfairyland",
            "PyFairyland",
            "fairy",
            "Fairy",
            "fairylandfuture",
            "PyFairylandFuture",
            "FairylandFuture",
        ]

    @property
    def include_package_data(self):
        return True

    @property
    def classifiers(self):
        results = [
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Programming Language :: SQL",
            "Framework :: Django :: 4",
            "Framework :: Flask",
            "Framework :: FastAPI",
            "Framework :: Flake8",
            "Framework :: IPython",
            "Framework :: Jupyter",
            "Framework :: Scrapy",
            "Natural Language :: English",
            "Natural Language :: Chinese (Simplified)",
            "Operating System :: Microsoft :: Windows :: Windows 10",
            "Operating System :: Microsoft :: Windows :: Windows 11",
            "Operating System :: POSIX :: Linux",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Version Control :: Git",
            "Topic :: System :: Operating System Kernels :: Linux",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        ]

        return results

    @property
    def install_requires(self):
        with open(os.path.join(_ROOT_PATH, "fairylandfuture", "conf", "requirements.in"), "r", encoding="UTF-8") as stream:
            requirements_text = stream.read()
        return requirements_text.split()

    @property
    def cmdclass(self):
        results = {
            "install_dependencies": InstallDependenciesCommand,
        }
        return results

    @staticmethod
    def vaildate_param(param, _type):
        if not isinstance(param, _type):
            raise TypeError(f"{param} type error.")

        return param

    @staticmethod
    def get_local_serial():
        try:
            with open(os.path.join(_ROOT_PATH, "fairylandfuture", "conf", "release", "commit-version"), "r", encoding="UTF-8") as stream:
                commit_count = stream.read()
            return int(commit_count)
        except Exception as err:
            print(f"Error: Getting build version {err}")
            return 0

    @classmethod
    def get_github_serial(cls):
        try:
            url = "https://raw.githubusercontent.com/PrettiestFairy/pypi-fairylandfuture/ReleaseMaster/fairylandfuture/conf/release/commit-version"
            response = requests.get(url)
            if response.status_code == 200:
                commit_count = int(response.text)
                return commit_count
            else:
                return cls.get_local_serial()
        except Exception as err:
            print(err)
            return cls.get_local_serial()


package = PackageInfo(_major, _minor, _micro, releaselevel)

setuptools.setup(
    name=package.name,
    fullname=package.fullname,
    keywords=package.keywords,
    version=package.version,
    author=package.author,
    author_email=package.email,
    description=package.description,
    long_description=package.long_description,
    long_description_content_type=package.long_description_content_type,
    url=package.url,
    # license="AGPLv3+",
    # packages=setuptools.find_packages(include=package.packages_include, exclude=package.packages_exclude),
    packages=setuptools.find_packages(exclude=package.packages_exclude),
    package_data=package.packages_data,
    include_package_data=package.include_package_data,
    classifiers=package.classifiers,
    python_requires=package.python_requires,
    install_requires=package.install_requires,
    cmdclass=package.cmdclass,
)
