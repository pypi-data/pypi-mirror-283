import os
import platform
import shutil
import site
import zipfile
from pathlib import Path

import dotenv
import fire
import tomllib


class Command:
    def zip_file(self, src: str, dst: str) -> None:
        """
        Zip a file to a specified zip file

        Args:
            src (str): Path to the source file.
            dst (str): Path to the destination ZIP file.
        """
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            full_path = os.path.abspath(src)
            archive_path = os.path.relpath(full_path, os.path.dirname(src))
            zip_file.write(full_path, archive_path)

    def zip_dir(self, src: str, dst: str) -> None:
        """
        Zips the contents of a directory to a specified zip file

        Args:
            src (str): Path to the source directory.
            dst (str): Path to the destination ZIP file.
        """
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            for root, _, files in os.walk(src):
                for file in files:
                    full_path = os.path.join(root, file)
                    archive_path = os.path.relpath(full_path, os.path.dirname(src))
                    zip_file.write(full_path, archive_path)

    def get_cpu_arch(self) -> str:
        return platform.machine()

    def get_os(self) -> str:
        system_name = platform.system()
        if system_name == "Windows":
            return "Windows"
        elif system_name == "Linux":
            return "Linux"
        elif system_name == "Darwin":
            return "macOS"
        else:
            return "Unknown system"

    def get_site_packages_dir(self) -> str:
        dirs = site.getsitepackages()
        for d in dirs:
            if "site-packages" in d:
                return d
        raise RuntimeError(f"Faild to find site-packages dir in {dirs}")

    def get_version(self) -> str:
        try:
            # Load the pyproject.toml file
            with Path("pyproject.toml").open("rb") as toml_file:
                toml_data = tomllib.load(toml_file)

            # Get the version from [tool.poetry] section
            version: str = toml_data.get("tool", {}).get("poetry", {}).get("version")
            if version:
                return version

            raise ValueError("Version not found in pyproject.toml [tool.poetry] section.")
        except FileNotFoundError as e:
            raise FileNotFoundError("File pyproject.toml not found.") from e
        except Exception as e:
            raise Exception(f"Error while parsing pyproject.toml: {str(e)}") from e

    def set_env(self) -> None:
        dotenv.set_key(".env", "version", self.get_version())

    def copy_dir(self, src: str, dst: str) -> None:
        shutil.copytree(src, dst, dirs_exist_ok=True)

    def copy_file(self, src: str, dst: str) -> None:
        shutil.copy(src, dst)


def main() -> None:
    fire.Fire(Command)


if __name__ == "__main__":
    main()
