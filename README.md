# memeloader
Scans for specificly prefixed files and filetypes then uploads them via POST. 
Intended to be used as scheduled task with logging and move operations.

Detects possible duplicate files with (1), (2), ... in the name and moves them to duplicates/.
Uploaded files will be moved to uploaded/, where also the log.txt file will reside by default.
Duplicate files will be moved to duplicate/. 
These directories and the log.txt will be created if not existing already.

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
```
Added an userscript that complements the memeloader.
It enables middleMouseClick to download on img and video tagged elements.