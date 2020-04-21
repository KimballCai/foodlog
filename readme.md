# SIFT
Scanning by Intelligent Food Tracker  
NUS CS5224 Project  
March 2020  

Requirement:
> absl-py==0.9.0
astor==0.8.1
bleach==1.5.0
certifi==2019.11.28
Django==2.0.6
gast==0.3.3
grpcio==1.27.2
h5py==2.10.0
html5lib==0.9999999
Keras==2.2.5
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
Markdown==3.2.1
mkl-fft==1.0.15
mkl-random==1.1.0
mkl-service==2.3.0
numpy==1.18.1
olefile==0.46
Pillow==7.0.0
protobuf==3.11.3
pytz==2019.3
PyYAML==5.3
scipy==1.4.1
six==1.14.0
tensorboard==1.7.0
tensorflow==1.7.0
termcolor==1.1.0
uWSGI==2.0.18
Werkzeug==1.0.0  

# Quick start
```bash
python manage.py runserver 127.0.0.1:8008 --insecure
```


# model
you need to download the model weight if you want to run the model.
### yolov3
link: https://drive.google.com/open?id=14hdXY8AJugvSHlTagZYjLJ8h8989UTC1
path: models/darknet/backup/food/yolov3-food_final.weights  

### xception
link: https://drive.google.com/open?id=12VfIb4q5CCC_V5PC8V4hFKQNrs7x11o1  
path: models/classification/models/xception-0-15-0.82.h5

### food231
link: https://drive.google.com/open?id=11oVuB4muzv-VlVEeJraBsG7g0-GxHDXQ
path: models/classification/class_index/food231.npy

