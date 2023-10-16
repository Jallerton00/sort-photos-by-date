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
        jsonContents = json.load(open(jsonFile))
        if jsonContents != {}:
            photoFilename = jsonContents["title"]
            photoTaken = jsonContents.get("photoTakenTime", "Unknown")
            if photoTaken == "Unknown":
                timestamp = partnerUploadKeepFrom #if don't know, keep it
            else:
                timestamp = datetime.strptime(photoTaken["formatted"].replace("Sept","Sep"), "%d %b %Y, %H:%M:%S %Z")
            if (jsonContents.get("googlePhotosOrigin","NA") == {"fromPartnerSharing":{}}) and (partnerUploadKeepFrom > timestamp):
                photoPath = re.sub(r'/.*', '/', jsonFile)
                fullPhotoPath = photoPath + photoFilename
                #fullPhotoPath=fullPhotoPath.replace("'","_")
                if (fullPhotoPath + ".json" == jsonFile):
                    print(fullPhotoPath)
                    listOfPartnerUploads.append(fullPhotoPath)
                    os.remove(fullPhotoPath)
                    os.remove(jsonFile)
                else:
                    print("json and photo don't match... " + fullPhotoPath + " " + jsonFile)

partnerUploadsOutput = open("partnerUploads","w")

for filename in listOfPartnerUploads:
    partnerUploadsOutput.write(re.sub('Photos from [0-9]*/', '', filename) + "\n")

partnerUploadsOutput.close()
