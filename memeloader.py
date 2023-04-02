import os
import requests
import datetime


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


if __name__ == "__main__":
    path = "."
    uploaded_dir = "uploaded/"
    url = "https://some.website/api_upload.php"
    url_xd = "https://some.website/api/upload"
    token = "some_token"
    token_xd = "some_token"
    id = "1"
    id_xd = "2"
    body_data = {"id": id, "token": token}
    body_data_xd = {"id": id_xd, "token": token_xd}
    types = ["jpeg", "jpg", "png", "gif", "webm", "mp4"]
    files = []

    log = Log(path=uploaded_dir)

    # scan dir for new files
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file() and not entry.is_dir():
                if entry.name.startswith("xD_") or entry.name.startswith("animu_") or \
                        entry.name.startswith("deviant_") or entry.name.startswith("insta_") or \
                        entry.name.startswith("reddit_"):
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
            if name.startswith("insta_") or name.startswith("deviant_") or name.startswith("reddit_"):
                myfile = {"imageupload": open(name, "rb")}
                x = requests.post(url_xd, data=body_data_xd, files=myfile)
            myfile = {}
            # move files to uploaded_dir
            new_name = uploaded_dir + name
            try:
                os.rename(name, new_name)
            except OSError:
                os.remove(new_name)
                os.rename(name, new_name)
            log.append("Uploaded and moved " + name)

        log.append("Finished work.")
    else:
        log.append("No work to be done.")


