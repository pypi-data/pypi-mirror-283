from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


def install_mongodb():
    subprocess.run(["python", "-m", "db.install_mongodb"], check=True)


class PostInstallCommand(install):
    def run(self):
        install_mongodb()
        install.run(self)


setup(
    name="aimmocore-db",
    version="0.1.0",
    packages=find_packages(),
    cmdclass={
        "install": PostInstallCommand,
    },
)
