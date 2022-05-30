import re
files = ["ax//x", "bd;\\a", "a\/cb:a"]
badChars = [":", ";"]
for file in files:
    subfolders = re.split("[/\\\\]+", file)
    if any(any(char in badChars for char in item) for item in subfolders):
        print(subfolders)