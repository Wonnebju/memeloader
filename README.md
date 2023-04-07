# memeloader
Scans for specificly prefixed files and filetypes then uploads them via POST. 
Intended to be used as scheduled task with logging and move operations.

Detects possible duplicate files with (1), (2), ... in the name and moves them to duplicates/.
Uploaded files will be moved out of the root_dir to uploaded/, where also the log.txt file will reside.
These directories and the log.txt will be created if not existing already.

Requires packages:
```
  -os
  -re
  -requests
  -datetime
```
