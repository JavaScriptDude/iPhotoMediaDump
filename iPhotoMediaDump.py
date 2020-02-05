#########################################
# .: iPhotoMediaDump.py :.
# Reads an iPhoto AlbumData.xml, parses out the images,movies and dumps data to a tab separated file
# in the same folder called z_media_list.tsv
# .: Usage :.
# python3 iPhotoMediaDump.py <path_to_AlbumData.xml>
# .: Other :.
# Author: Timothy C. Quinn
# Home: https://github.com/JavaScriptDude/iPhotoMediaDump
# Licence: https://opensource.org/licenses/MIT
# References:
# - Borrowed some logic from a ruby script here: https://gist.github.com/yuanying/9968855
#########################################

import plistlib, csv, os, sys
from datetime import datetime, timezone
from io import StringIO

UNIX_EPOCH = datetime(1970,1,1)
IPHOTO_EPOCH = datetime(2001, 1, 1)
IPHOTO_EPOCH_DELTA = (IPHOTO_EPOCH - UNIX_EPOCH).total_seconds()


def main(argv):    
    in_path = argv[0]

    f_album_data = open(in_path+"/AlbumData.xml", "rb")
    albumData = plistlib.load(f_album_data)


    f_out = open(in_path+"/z_media_list.tsv", "w")
    wri = csv.writer(f_out, delimiter='\t')
    wri.writerow(['type', 'file', 'path', 'roll', 'date'])

    masterImageList = albumData["Master Image List"]
    for key, value in masterImageList.items():

        fname,fpath = splitPath(value['ImagePath'])

        photo_date = getIPhotoDate(value['DateAsTimerInterval'])

        wri.writerow([value['MediaType'], fname, fpath, value['Roll'], photo_date])


    f_out.close()

    print("Done. Data written to {}".format(f_out.name))



def getIPhotoDate(iphoto_date):
    return datetime.utcfromtimestamp(IPHOTO_EPOCH_DELTA + iphoto_date)

def splitPath(s):
    f = os.path.basename(s)
    p = s[:-(len(f))-1]
    return f, p

    

if __name__ == '__main__':
    main(sys.argv[1:])
