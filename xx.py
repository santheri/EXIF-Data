from exif import Image
img_path = r'E:\Uploading Images\templates\IMG_20230210_172110081.jpg'

def decimal_coords(coords, ref):
 decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
 if ref == "S" or ref == "W":
     decimal_degrees = -decimal_degrees
 return decimal_degrees

def image_coordinates(image_path):
    with open(img_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            print('No Coordinates')
    else:
        print ('The Image has no EXIF information')
    return coords
    

# with open(img_path, 'rb') as src:
#     img = Image(src)
#     print (src.name, img)
#     print(img.gps_longitude)
#     print(img.gps_latitude)

image_coordinates(img_path)

