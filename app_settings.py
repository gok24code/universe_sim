from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()
window.color = color.black
window.background_color = color.black

cam = EditorCamera(vsync=False,
    borderless=False,
    fullscreen=False,
    development_mode=False
    )

# Görüş mesafesini ve chunk algısını maksimize ediyoruz
cam.clip_plane_far = 2000000 # 2 Milyon birim - En uç galaksiler bile her an görünür
cam.fov = 100               # Daha geniş, sinematik bir görüş açısı
cam.position = (0, 500, -2000)
cam.look_at(Vec3(0,0,0))
cam.move_speed = 600        # Keşif hızı dengelendi

window.exit_button.visible = False
window.fps_counter._visible = False
window.collider_counter.visible =False
window.entity_counter.visible =False
AmbientLight(color=color.white)
DirectionalLight(shadows=False)
