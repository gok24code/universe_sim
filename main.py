import os
import time
from ursina import *
from app_settings import *
from objects.prefabs import *

# Kamerayı tekrar hızlandırıyoruz (evrende serbestçe gezmek için)
cam.move_speed = 1000

def update():
    update_universe(cam)

app.run()