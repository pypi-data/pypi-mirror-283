import re

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

from aider import __version__
from aider.help_pats import exclude_website_pats

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    long_description = re.sub(r"\n!\[.*\]\(.*\)", "", long_description)
    # long_description = re.sub(r"\n- \[.*\]\(.*\)", "", long_description)

# Debug: Print discovered packages
packages = find_packages(exclude=["benchmark"]) + ["aider.website"]
print("Discovered packages:", packages)

setup(
    name="test444888",
#     version=__version__,
    version="1.0",
    packages=packages,
    include_package_data=True,
    package_data={
        "aider": ["queries/*.scm"],
        "aider.website": ["**/*.md"],
    },
    exclude_package_data={"aider.website": exclude_website_pats},
    install_requires=requirements,
    python_requires=">=3.9,<3.13",
    entry_points={
        "console_scripts": [
            "test444888 = aider.main:main",
        ],
    },
#     description="Aider is AI pair programming in your terminal",
    description="test",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
    url="https://github.com",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
)
