import os
import time
from ursina import *
from app_settings import *
from objects.prefabs import *

# Kamerayı hızlandırıyoruz (devasa yapıyı gezebilmek için)
cam.move_speed = 300

def update():
    update_universe(cam)

app.run()