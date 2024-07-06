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

    # Find the extracted directory
    extracted_dir = None
    for item in os.listdir(temp_extract_path):
        item_path = os.path.join(temp_extract_path, item)
        if os.path.isdir(item_path):
            extracted_dir = item_path
            break

    if extracted_dir is None:
        raise Exception("Failed to find the extracted MongoDB directory")

    # Move files from extracted directory to the final destination
    for item in os.listdir(extracted_dir):
        s = os.path.join(extracted_dir, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            shutil.move(s, d)
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
    mongodb_bin = os.path.join(install_dir, "mongodb")
    os.environ["PATH"] += os.pathsep + mongodb_bin
    print(f"MongoDB bin added to PATH: {mongodb_bin}")


if __name__ == "__main__":
    main()
