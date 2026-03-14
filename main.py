import os
import time
from ursina import *
from app_settings import *
from objects.prefabs import *

def update():
    rotate_blackhole(cam)
    move_all_skyspheres()
app.run()