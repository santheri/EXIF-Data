from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from exif import Image
import os

app = Flask(__name__)
db = SQLAlchemy()
#configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exif_data.db"
db.init_app(app)


dir=os.getcwd()

class Uploaded_images(db.Model):
    __tablename__="uploaded_images"
    ID=db.Column(db.Integer,primary_key=True)
    file_location=db.Column(db.String,unique=True,nullable=False)
    latitude=db.Column(db.String,unique=False,nullable=False)
    longitude=db.Column(db.String,unique=False,nullable=False)
    
with app.app_context():
    db.create_all()

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
        file_name=file.filename
        print(file.filename)
        file_location=os.path.join(dir,"static","images",file.filename)
        file.save(file_location)  
        
        # coords=image_coordinates(r"E:\EMAIL\EXIF-Data-master\static\images\WIN_20221204_14_17_14_Pro.jpg")
        try:
            coords=image_coordinates(file_location)
        except:
            return render_template("index.html",data="location data not found") 
        try:
            
            img=Uploaded_images(file_location=file_name,latitude=coords[0],longitude=coords[1])
            db.session.add(img)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return render_template("index.html",data="file already exists")
        print(coords)
               
        
        
        
        # Redirect to the home page to display the uploaded image and its location map
        return render_template("index.html",data="file uploaded successfully")
        # return render_template("xx.html",data=coords)

@app.route("/data")
def data():
     data=Uploaded_images.query.all()
     for i in data:
         i.ID="map"+str(i.ID)
     lat_long=[]
     for i in data:
         lat_long.append([float(i.latitude),float(i.longitude)])
     print(lat_long)
     return render_template("data.html",data=lat_long,db_data=data)

if __name__ == '__main__':
    app.run(debug=True)
