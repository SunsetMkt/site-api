import lzma
import zipfile
import os

# Compress china_ip_list.txt to china_ip_list.txt.xz
with open('china_ip_list.txt', 'rb') as f:
    with lzma.open('china_ip_list.txt.xz', 'wb') as f2:
        f2.write(f.read())


# Zip myutils folder recursively to myutils.zip, but ignore .pyc files
# If we need to use zipimport some day, we can use this
# Notice: zipimport only accept ZIP_DEFLATED compression
with zipfile.ZipFile('myutils.zip', 'w', zipfile.ZIP_DEFLATED) as f:
    for root, dirs, files in os.walk('myutils'):
        for file in files:
            if file.endswith('.pyc'):
                continue
            f.write(os.path.join(root, file))
