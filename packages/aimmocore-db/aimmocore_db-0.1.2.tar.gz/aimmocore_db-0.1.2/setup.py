from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import subprocess


class bdist_wheel(_bdist_wheel):
    """Custom bdist_wheel command to run post-installation tasks."""

    def run(self):
        _bdist_wheel.run(self)
        self._install_mongodb()

    def _install_mongodb(self):
        subprocess.run(["python", "-m", "aimmocore_db.install_mongodb"], check=True)


setup(
    name="aimmocore-db",
    version="0.1.0",
    packages=find_packages(),
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
)
