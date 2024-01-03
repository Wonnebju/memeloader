# memeloader
Scans for specificly prefixed files and filetypes then uploads them via POST. 
Intended to be used as scheduled task with logging and move operations.

Detects possible duplicate files with (1), (2), ... in the name and moves them to duplicates/.
Uploaded files will be moved to uploaded/, where also the log.txt file will reside by default.
These directories and the log.txt will be created if not existing already.

Configuration is done in the .env, which will be created on first run in the same directory as memeloader.py.
```dotenv
# environment variables for memeloader.py

URL=https://some.website/api_upload.php # target api url
ID=1 # user id
TOKEN=some_auth_token # auth token
FILE_DESCRIPTOR=file # name of the files field the target api will use
PREFIXES=xD_,insta_,reddit_ # file prefixes to scan for
TYPES=jpeg,jpg,png,gif,webm,mp4,webp # file types to scan for
UPLOAD_DIR=uploaded/ # relative directory to move files to after upload
DUPLICATE_DIR=duplicate/ # relative directory to move duplicates to
```
```python
prefixes = ("", "")  # use this tuple to "disable" prefix condition
types = ["jpeg"] # at least one type is required
```
Required packages:
```
  -os
  -re
  -requests
  -datetime
  -dotenv
  -tqdm
```
Added Userscript (Greasemonkey/Tampermonkey) that complements the memeloader.
It enables middleMouseClick to download on img and video tagged elements.
