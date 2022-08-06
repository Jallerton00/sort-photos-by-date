''' A script to move files based on creation date,
heavily based on https://www.geeksforgeeks.org/python-move-files-to-creation-and-modification-date-named-directories/
This was modified to be more useful for me to sort my photos from Google Takeout - it removes the json metadata files as we go as I've already used
google-photos-takeout-helper to reattach the metadata.'''

# Import the following modules
import os
import time
import shutil
import datetime
import glob
import sys

if len(sys.argv)!=2:
    print("Please provide a path")
    exit()
else:
    path = sys.argv[1]

# Change the directory and jump to the location
# where you want to arrange the files
os.chdir(path)

# Get the current working directory
outputs = os.getcwd()

#rename to include directory (if directory is not just a number) (this needs to be run only in the directories with names you want to keep)
'''
find . -iname '*.jpg' -exec sh -c '
  for img; do
    parentdir=${img%/*}      # leave the parent dir (remove the last `/` and filename)
    dirname=${parentdir##*/} # leave the parent directory name (remove all parent paths `*/`)
    mv -i "$img" "$parentdir/$dirname ${img##*/}"
  done
' sh {} +
'''

#flatten

'''
find . -mindepth 2 -type f -exec mv -t . --backup=t '{}' + //move all files from sub folders, backup with number if already exists

find . -empty -type d -delete //remove empty dirs

rename 's/((?:\..+)?)\.~(\d+)~$/_$2$1/' *.~*~ //remove stupid backup naming
'''
    
#unflatten
# Again run a loop for traversing through all the
# files in the current directory
for file in os.listdir('.'):
    
    file_extension = os.path.splitext(file)[-1].lower()

    if (file_extension != ".json"):
        # Get all the details of the file creation
        # and modification
        time_format = time.gmtime(os.path.getmtime(file))
        
        # Now, extract only the Year, Month, and Day
        datetime_object = datetime.datetime.strptime(str(time_format.tm_mon), "%m")
        
        # Provide the number and find the month
        # full_month_name = datetime_object.strftime(
            # "%b")
        
        # Give the name of the folder
        dir_name = str(time_format.tm_year) + '-' + str(time_format.tm_mon) + '-' + \
            str(time_format.tm_mday)
            

        # Check if the folder exists or not
        if not os.path.isdir(dir_name):
            
            # If not then make the new folder
            os.mkdir(dir_name)
        dest = dir_name
        
        # Move all the files to their respective folders
        shutil.move(file, dest)
    else:
        os.remove(file)
    
print("successfully moved...")
