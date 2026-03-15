from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()
window.color = color.black
window.background_color = color.black

# Serbest gezen orijinal EditorCamera
cam = EditorCamera(vsync=False,
    borderless=False,
    fullscreen=False,
    development_mode=False
    )

# Görüş mesafesini ve açısını yüksek tutuyoruz
cam.clip_plane_far = 1000000 
cam.fov = 90
cam.position = (0, 500, -2000)
cam.look_at(Vec3(0,0,0))

window.exit_button.visible = False
window.fps_counter._visible = False
window.collider_counter.visible =False
window.entity_counter.visible =False
AmbientLight(color=color.white)
DirectionalLight(shadows=False)
