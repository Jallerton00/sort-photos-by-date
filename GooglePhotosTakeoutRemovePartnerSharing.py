import os
import glob
import json
from exif import Image
from datetime import datetime

'''
This script was created to untangle my photos and the photos accidentally imported using partner sharing.
'''


photos_dir = "" #Takeout path
partnerUploadKeepFrom = datetime(1970, 1, 1, 00, 00) # keep everything newer than this date

os.chdir(photos_dir)

jsonGlob = '**/*.json'

# use iglob to not load all at once
listOfJsonFilesIterator = glob.iglob(jsonGlob, recursive=True)

listOfPartnerUploads = []

for jsonFile in listOfJsonFilesIterator:
    if "metadata" not in jsonFile:
        #print(jsonFile)
        jsonContents = json.load(open(jsonFile))
        photoTaken = jsonContents.get("photoTakenTime", "Unknown")
        if photoTaken == "Unknown":
            timestamp = partnerUploadKeepFrom #if don't know, keep it
        else:
            timestamp = datetime.strptime(photoTaken["formatted"].replace("Sept","Sep"), "%d %b %Y, %H:%M:%S %Z")
        if (jsonContents.get("googlePhotosOrigin","NA") == {"fromPartnerSharing":{}}) and (partnerUploadKeepFrom > timestamp):
            photoFilename = jsonFile.replace(".json","")
            listOfPartnerUploads.append(photoFilename)
            if os.path.exists(photoFilename):
                os.remove(photoFilename)
                os.remove(jsonFile)
            else:
                print("File could not be found: " + photoFilename)

partnerUploadsOutput = open("partnerUploads","w")

for filename in listOfPartnerUploads:
    partnerUploadsOutput.write(filename + "\n")

partnerUploadsOutput.close()
