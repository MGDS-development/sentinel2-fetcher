import sentinelsat as ss
import zipfile
import time
import tempfile
import glob
import shutil
import os


tile = "30TVK"

api = ss.SentinelAPI(os.environ["COPERNICUS_USER"], os.environ["COPERNICUS_PASS"], 'https://scihub.copernicus.eu/dhus')

data = api.query(date=('NOW-5DAYS', 'NOW-0DAYS'),raw="filename:*MSIL2A*T30TVK*", limit=1) #L2A on tile 30TVK

v = dict(data)

if len(v) > 0:

    uuid = list(v.keys())[0]
    filename = v[uuid]['filename']

    with tempfile.TemporaryDirectory() as download_path:

        print("Downloading on", download_path + '/')

        f = api.download(uuid, directory_path=download_path, checksum=True)

        print(f)

        zip_path = f['path']

        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(download_path)

        b04 = glob.glob(download_path+'/*.SAFE/GRANULE/*/IMG_DATA/*B04*')[0]

        b08 = glob.glob(download_path+'/*.SAFE/GRANULE/*/IMG_DATA/*B08*')[0]

        shutil.move(b04, "/opt/ids/sentinel/")
        shutil.move(b08, "/opt/ids/sentinel/")

        print("Finished!")


        
