import os
import platform
import urllib.request
import tarfile
import zipfile
import shutil


def download_mongodb(destination):
    system = platform.system()
    if system == "Windows":
        url = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-5.0.5.zip"
        filename = "mongodb-windows.zip"
    elif system == "Linux":
        url = "https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-5.0.5.tgz"
        filename = "mongodb-linux.tgz"
    elif system == "Darwin":  # macOS
        url = "https://fastdl.mongodb.org/osx/mongodb-macos-x86_64-5.0.5.tgz"
        filename = "mongodb-macos.tgz"
    else:
        raise Exception("Unsupported operating system")

    filepath = os.path.join(destination, filename)
    if not os.path.exists(filepath):
        print(f"Downloading MongoDB from {url}...")
        urllib.request.urlretrieve(url, filepath)
        print("Download complete.")
    else:
        print("MongoDB archive already downloaded.")

    return filepath


def extract_mongodb(filepath, destination):
    temp_extract_path = os.path.join(destination, "temp_mongodb")

    if not os.path.exists(temp_extract_path):
        os.makedirs(temp_extract_path)

    if filepath.endswith(".zip"):
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(temp_extract_path)
    elif filepath.endswith(".tgz") or filepath.endswith(".tar.gz"):
        with tarfile.open(filepath, "r:gz") as tar_ref:
            tar_ref.extractall(temp_extract_path)
    else:
        raise Exception("Unsupported archive format")

    # Move extracted files to the final destination and clean up temp directory
    for item in os.listdir(temp_extract_path):
        s = os.path.join(temp_extract_path, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            for sub_item in os.listdir(s):
                sub_s = os.path.join(s, sub_item)
                sub_d = os.path.join(destination, "bin", sub_item)
                if not os.path.exists(os.path.join(destination, "bin")):
                    os.makedirs(os.path.join(destination, "bin"))
                shutil.move(sub_s, sub_d)
        else:
            shutil.move(s, d)

    shutil.rmtree(temp_extract_path)

    print("Extraction complete.")


def install_mongodb(destination):
    mongodb_path = os.path.join(destination, "mongodb")
    archive_path = download_mongodb(destination)
    extract_mongodb(archive_path, mongodb_path)
    print(f"MongoDB installed to {mongodb_path}")


def main():
    install_dir = os.path.join(os.path.expanduser("~"), ".aimmocore", "mongodb_installation")
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    install_mongodb(install_dir)

    # Optionally, add MongoDB to the PATH
    mongodb_bin = os.path.join(install_dir, "mongodb", "bin")
    os.environ["PATH"] += os.pathsep + mongodb_bin
    print(f"MongoDB bin added to PATH: {mongodb_bin}")


if __name__ == "__main__":
    main()
