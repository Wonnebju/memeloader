import os
import requests
import datetime
import re


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
            print(line)


if __name__ == "__main__":
    # set these
    url = "https://some.website/api_upload.php"
    url_xd = "https://some.website/api/upload"
    token = "some_token"
    token_xd = "some_token"
    id_ = "1"
    id_xd = "2"

    path = "."
    uploaded_dir = "uploaded/"
    body_data = {"id": id_, "token": token}
    body_data_xd = {"id": id_xd, "token": token_xd}
    prefixes = ("xD_", "animu_", "deviant_", "insta_", "reddit_")
    prefixes_xd = ("animu_", "deviant_", "insta_", "reddit_")
    types = ["jpeg", "jpg", "png", "gif", "webm", "mp4", "webp"]
    files = []

    log = Log(path=uploaded_dir)

    # scan dir for new files
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file() and not entry.is_dir():
                if entry.name.startswith(prefixes):
                    if entry.name.lower()[entry.name.rfind(".") + 1:] in types:
                        files.append(entry.name)

    if files:
        # create dir to move files into
        try:
            os.mkdir(uploaded_dir)
            log.append("Path " + uploaded_dir + " created.")
        except FileExistsError:
            pass
        finally:
            log.append("Found new files. Proceeding to upload.")

        # upload files
        for name in files:
            myfile = {"file": open(name, "rb")}

            x = requests.post(url, data=body_data, files=myfile)
            if name.startswith(prefixes_xd):
                myfile = {"imageupload": open(name, "rb")}
                y = requests.post(url_xd, data=body_data_xd, files=myfile)

            myfile = {}
            # clean up the name
            response = x.json()
            new_name = uploaded_dir + re.sub('[^\w-]', "_", name[:name.rfind(".")]) + name[name.rfind("."):]
            # move file
            try:
                os.rename(name, new_name)
            except OSError:
                os.remove(new_name)
                log.append("Failed to move " + name)
            log.append(f"{response['status']} Renamed {name} and moved to {new_name}.")

        log.append("Finished work.")
    else:
        log.append("No work to be done.")
