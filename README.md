# iTS_server

### Installation Instructions

The server file permissions need to be set properly before both the user and the
server can manipulate files properly.

Here are (hopefully) complete instructions.

1. From the html folder (not from the parent folder), set the appropriate permissions
for current files. Always try all commands without `sudo` first, and only use `sudo` if needed.
```
find . -type d -exec chmod 775 {} \;
find . -type f -exec chmod 664 {} \;
```
2. Now, `cd ..` to move to the parent folder.
3. Type `setfacl -d -m u::rwX,g::rwX,o::- html`. Note the capitalization. Replace `html` with
the actual name of the html folder. This will ensure that any subfolders, subfiles created will
automatically have the required permissions.
4. Finally, make the `its`, and `test_all` file executable.
```
chmod 774 html/iTS/its
chmod 774 html/iTS/test_suite/test_all
```
5. Try to run the program online to see if it works.
