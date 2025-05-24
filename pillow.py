from PIL import Image
from PIL.ExifTags import TAGS

# Apne image ka path do
image_path = "transaction.jpg"

# Image open karo
image = Image.open(image_path)

# EXIF metadata extract karo
exif_data = image._getexif()

if exif_data:
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        print(f"{tag_name}: {value}")
else:
    print("❌ No EXIF metadata found!")
