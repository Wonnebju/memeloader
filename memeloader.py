import os
import requests
import datetime
import re
from dotenv import load_dotenv
from tqdm import tqdm


class Log:
    def __init__(self, path="", name="log", timestamp=True, time_format="%d-%m-%Y %H:%M:%S"):
        self.path = path
        self.name = name
        self.timestamp = timestamp
        self.time_format = time_format

    def append(self, line):
        with open(self.path + self.name + ".txt", "a") as log_file:
            if self.timestamp:
                stamp = datetime.datetime.now()
                line = stamp.strftime(self.time_format) + ": " + line
            log_file.write(line + "\n")


def scan_dir(path: str, prefixes: tuple, types: list) -> list:
    """Scans directory for files with valid prefixes & types

    :param path: directory to search in
    :param prefixes: tuple of prefixes
    :param types: list of valid filetypes without the "."
    :return: list of valid filenames
    """
    files = list()
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file() \
                    and entry.name.startswith(prefixes) \
                    and entry.name.lower()[entry.name.rfind(".") + 1:] in types:
                files.append(entry.name)
    return files


def clean_name(name: str) -> str:
    """Clean filename of non word chars and substitute them with "_"
    """
    name_cleaned = re.sub(r'[^\w\-()]', "_", name[:name.rfind(".")]) + name[name.rfind("."):]
    return name_cleaned


def mkdir(path: str):
    """Creates a directory
    """
    try:
        os.mkdir(path)
        log.append(f"Directory {path} created.")
    except FileExistsError:
        pass


def move_file(name: str, target: str):
    """Moves a file (replaces it)
    """
    try:
        os.replace(name, target)
    except OSError:
        log.append(f"Failed to move {name} to {target}.")
        exit(1)
    # log.append(f"Renamed {name} to {new_name}.")


def split_duplicates(files: list) -> tuple:
    """Cleans file names of duplicates

    :param files: list of file names
    :return: tuple of lists of cleaned file names and duplicates
    """
    files_cleaned, duplicates = list(), list()
    for file in files:
        if re.search(r"\(\d+\)", file):
            duplicates.append(file)
        else:
            files_cleaned.append(file)
    return files_cleaned, duplicates


def upload_file(url: str, data: dict, files: dict) -> object:
    """Upload the file via POST

    :param url: target url
    :param data: body data of the request
    :param files: file descriptor and file byte stream
    :return: Response object
    """
    response = requests.post(url, data=data, files=files)
    # log.append(f"{response.json()['status']}")
    return response


def upload_move_files(files: list, url: str, data: dict, file_descriptor: str, target_dir: str):
    """Upload multiple files with a cleaned name then move them

    :param files: list of files
    :param url: api target url
    :param data: api target body data
    :param file_descriptor: field name for files
    :param target_dir: target move directory after upload
    """
    for file in tqdm(files, desc="Uploading"):
        file_clean = clean_name(file)
        move_file(file, file_clean)
        with open(file_clean, "rb") as outfile:
            upload_file(url, data, {file_descriptor: outfile})
        move_file(file_clean, target_dir + file_clean)


def clean_move_files(files: list, target_dir: str):
    """Clean names and move given files to target_dir

    :param files: list of file names
    :param target_dir:
    """
    for file in tqdm(files, desc="Cleaning"):
        file_clean = clean_name(file)
        move_file(file, target_dir + file_clean)


if __name__ == "__main__":

    # defaults
    default_values = {
        "URL": "https://some.website/api_upload.php",
        "ID": "1",
        "TOKEN": "some_auth_token",
        "FILE_DESCRIPTOR": "file",
        "PREFIXES": "xD_,insta_,reddit_",
        "TYPES": "jpeg,jpg,png,gif,webm,mp4,webp",
        "UPLOAD_DIR": "uploaded/",
        "DUPLICATE_DIR": "duplicate/",
    }

    # Write the default values to a .env file if it doesn't exist
    env_file_path = ".env"
    if not os.path.exists(env_file_path):
        with open(env_file_path, "w") as env_file:
            env_file.write(f"# environment variables for memeloader.py\n\n")
            for key, value in default_values.items():
                env_file.write(f"{key}={value}\n")
        print("Created .env with default values. Please configure before rerunning.")
        exit()

    load_dotenv()

    # request data
    url = os.environ.get("URL")  # target api url
    data = {"id": os.environ.get("ID"),  # body data the request will use. Adjust this to fit your need.
            "token": os.environ.get("TOKEN")}
    file_descriptor = os.environ.get("FILE_DESCRIPTOR")  # name of the files field the target api will use

    # file attributes to scan for and move to
    prefixes = tuple(os.environ.get("PREFIXES").split(','))  # file prefixes to scan for
    types = os.environ.get("TYPES").split(',')  # file types to scan for
    uploaded_dir = os.environ.get("UPLOAD_DIR")  # relative directory to move files to after upload
    duplicate_dir = os.environ.get("DUPLICATE_DIR")  # relative directory to move duplicates to

    # log output
    console = bool(os.environ.get("CONSOLE"))  # output logs to console

    scan_path = "."  # only current work directory supported

    # logging
    log = Log(path=uploaded_dir)
    mkdir(uploaded_dir)
    mkdir(duplicate_dir)

    # start the work
    files = scan_dir(scan_path, prefixes, types)
    files, duplicates = split_duplicates(files)
    if len(files):
        msg = f"Found {len(files)} files, uploading..."
        log.append(msg)
        print(msg)
        upload_move_files(files, url, data, file_descriptor, uploaded_dir)
    if len(duplicates):
        msg = f"Found {len(duplicates)} duplicates, cleaning..."
        log.append(msg)
        print(msg)
        clean_move_files(duplicates, duplicate_dir)
