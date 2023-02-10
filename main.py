from flask import Flask, render_template, request, redirect, url_for
# from PIL import Image
from exif import Image
import exifread
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def decimal_coords(coords, ref):
 decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
 if ref == "S" or ref == "W":
     decimal_degrees = -decimal_degrees
 return decimal_degrees

def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
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
    

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        coords=image_coordinates(r"E:\Uploading Images\static\images\IMG_20230210_172110081.jpg")
        print(coords)
        lat = coords[0]
        lng = coords[1]
        
        # Format the latitude and longitude as decimal degrees
        if lat and lng:
            static_map_url = f'https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=13&size=600x300&maptype=roadmap&markers=color:red%7Clabel:A%7C{lat},{lng}&key=YOUR_API_KEY'
            response = requests.get(static_map_url)
            
            # Save the static map image to a file
            with open('static_map.png', 'wb') as f:
                f.write(response.content)
        
        # Redirect to the home page to display the uploaded image and its location map
        return render_template("xx.html",data=coords)

def convert_to_degrees(value):
    # Convert the EXIF GPS data to decimal degrees
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    
    return d + (m / 60.0) + (s / 3600.0)

if __name__ == '__main__':
    app.run(debug=True)
