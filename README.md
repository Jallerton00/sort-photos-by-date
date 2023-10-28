# sort-photos-by-date

A script to move files based on creation date, heavily based on https://www.geeksforgeeks.org/python-move-files-to-creation-and-modification-date-named-directories/

This was modified to be more useful for me to sort my photos from Google Takeout - it removes the json metadata files as we go as I've already used [google-photos-takeout-helper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper/) to reattach the metadata.

I found the flattening function to be a bit annoying in Python, so I settled on a couple of shell commands:
```
find . -mindepth 2 -type f -exec mv -t . --backup=t '{}' + #move all files from sub folders, backup with number if already exists
find . -empty -type d -delete #remove empty dirs
rename 's/((?:\..+)?)\.~(\d+)~$/_$2$1/' *.~*~ #remove stupid backup naming
```

I also had some folders which had useful names which I wanted to keep with the photos, so I renamed the photo to include the folder name before flattening:
```
find . -iname '*.jpg' -exec sh -c '
  for img; do
    parentdir=${img%/*}      # leave the parent dir (remove the last `/` and filename)
    dirname=${parentdir##*/} # leave the parent directory name (remove all parent paths `*/`)
    mv -i "$img" "$parentdir/$dirname ${img##*/}"
  done
' sh {} +
```
