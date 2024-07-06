from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        self._install_mongodb()

    def _install_mongodb(self):
        subprocess.run(["python", "-m", "aimmocore_db.install_mongodb"], check=True)


setup(
    name="aimmocore-db",
    version="0.1.11",
    packages=find_packages(),
    cmdclass={
        "install": PostInstallCommand,
    },
)
