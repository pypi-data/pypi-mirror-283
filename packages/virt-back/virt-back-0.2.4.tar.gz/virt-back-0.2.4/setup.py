from setuptools import setup
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="virt-back",
    version="0.2.4",
    description="virt-back: A backup utility for QEMU, KVM, XEN, and Virtualbox guests",
    keywords="backup virtual hypervisor QEMU KVM XEN Virtualbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Russell Ballestrini",
    author_email="russell@ballestrini.net",
    url="https://git.unturf.com/python/virt-back",
    platforms=["All"],
    license="Public Domain",
    py_modules=["virtback"],
    include_package_data=True,
    scripts=["virt-back"],
    install_requires=[
        "libvirt-python",
    ],
)

"""
setup()
  keyword args: http://peak.telecommunity.com/DevCenter/setuptools

# built and uploaded to pypi with this:

python setup.py sdist
twine upload dist/*

"""

# Installation Instructions:
# To install virt-back, you can use pip:
#  * pip install virt-back
#
# Note: You need to have the libvirt development libraries installed.
# On Fedora/RedHat, you can install it with:
#  * sudo dnf install libvirt-devel
# On Ubuntu, you can install it with:
#  * sudo apt-get install libvirt-dev
