from ursina import *
from ursina.prefabs.editor_camera import EditorCamera

app = Ursina()

cam = EditorCamera(vsync=False,          # V-sync kapat → FPS sınırı kalkar
    borderless=False,
    fullscreen=False,
    development_mode=False  # Debug overhead'i kaldırır
    )

window.exit_button.visible = False  # Çıkış butonunu gizle
window.fps_counter._visible = False
window.collider_counter.visible =False
window.entity_counter.visible =False
AmbientLight(color=color.white)
DirectionalLight(shadows=False)
