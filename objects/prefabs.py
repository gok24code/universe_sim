from ursina import *
import random
import math

# --- MATEMATİKSEL SABİTLER ---
PHI = (1 + 5**0.5) / 2
GOLDEN_ANGLE = math.tau / (PHI**2)

class StarSystem:
    def __init__(self, parent_galaxy, position):
        self.center = Entity(parent=parent_galaxy, position=position)
        self.enabled = True 
        
        star_color = random.choice([color.yellow, color.white, color.cyan, color.red, color.orange])
        star_scale = random.uniform(30, 60) 
        self.star = Entity(parent=self.center, model='sphere', color=star_color, scale=star_scale, collider=None)
        
        self.orbiters = [] 
        num_planets = random.randint(4, 7)
        ecosystems = [color.blue, color.green, color.red, color.cyan, color.rgba(139, 69, 19), color.magenta]
        
        last_dist = star_scale * 3
        for i in range(num_planets):
            dist = last_dist + random.uniform(80, 200) 
            last_dist = dist
            speed = (4 + random.uniform(1, 3)) / (dist ** 0.5) 
            planet_color = random.choice(ecosystems)
            size = random.uniform(5, 12)
            planet_pivot = Entity(parent=self.center)
            planet = Entity(parent=planet_pivot, model='sphere', position=(dist, 0, 0), color=planet_color, scale=size, collider=None)
            self.orbiters.append({'pivot': planet_pivot, 'speed': speed})
            
            if size > 8:
                num_moons = random.randint(0, 1)
                for j in range(num_moons):
                    moon_dist = size * random.uniform(4, 8) 
                    moon_speed = random.uniform(5, 12)
                    moon_pivot = Entity(parent=planet)
                    moon = Entity(parent=moon_pivot, model='sphere', position=(moon_dist, 0, 0), color=color.light_gray, scale=size * 0.25, collider=None)
                    self.orbiters.append({'pivot': moon_pivot, 'speed': moon_speed})

    def update_orbits(self):
        if not self.enabled: return
        for o in self.orbiters:
            o['pivot'].rotation_y += o['speed'] * time.dt * 1.5

class Galaxy:
    def __init__(self, position, rotation, num_stars=5000, color_theme=color.cyan):
        # Galaksinin ana pivotu artık rastgele bir rotasyona (rotation) sahip
        self.pivot = Entity(position=position, rotation=rotation)
        self.radius = 5000 
        
        # 1. Olay Ufku
        self.blackhole = Entity(parent=self.pivot, model='sphere', color=color.black, scale=250, collider=None)
        
        # --- OPTİMİZE EDİLMİŞ AKKRESYON DİSKİ (Aynen korundu) ---
        all_vertices = []
        all_colors = []
        for i in range(25):
            r = 300 + (i * 12)
            alpha = 0.25 * (0.15 ** (i/3))
            base_col = lerp(color.orange, color.black, i/12) if i < 12 else lerp(color.yellow, color.black, (i-12)/13)
            safe_color = color.rgba(base_col.r*100, base_col.g*200, base_col.b*100, alpha*255)
            segments = 64
            for j in range(segments + 1):
                theta = (j / segments) * math.tau
                all_vertices.append(Vec3(math.cos(theta)*r, 0, math.sin(theta)*r))
                all_colors.append(safe_color)

        self.disk_mesh = Entity(
            parent=self.pivot,
            model=Mesh(vertices=all_vertices, colors=all_colors, mode='line', thickness=8),
        )

        # --- 3 BOYUTLU VE HACİMLİ SARMAL GALAKSİ ---
        stars_pos = []
        stars_colors = []
        num_arms = 4
        arm_spread = 0.35 
        
        for i in range(num_stars):
            arm = (i % num_arms) * (math.tau / num_arms)
            if random.random() > 0.8: arm += random.uniform(0, math.tau)
            
            r = random.uniform(0, 1)**0.8 * self.radius + 600
            twist = 3.2
            theta = arm + math.log(r / 500) * twist + random.gauss(0, arm_spread)
            
            # --- 3B BOYUTLANDIRMA ---
            # Galaktik şişkinlik (merkezde dikey yayılım fazla, dışa doğru azalır)
            # Merkezde r=600 civarında y yayılımı ~400 iken, dışarıda r=5000'de ~50 olur.
            dist_factor = r / self.radius
            vertical_spread = (1.0 - dist_factor) * 500 + 50 # Merkezde çok daha kalın
            
            x = r * math.cos(theta)
            y = random.gauss(0, vertical_spread * 0.4) # Hacimli dikey dağılım
            z = r * math.sin(theta)
            
            stars_pos.append(Vec3(x, y, z))
            
            # --- SAMAN YOLU RENK PALETİ ---
            if dist_factor < 0.22:
                col = lerp(color.rgba(255, 150, 90, 255), color.white, random.uniform(0.3, 0.7))
            elif dist_factor < 0.55:
                dusty_brown = color.rgba(210, 180, 140, 255)
                col = lerp(dusty_brown, color.white, random.uniform(0.4, 0.9))
            else:
                cold_white = color.rgba(230, 100, 90, 255)
                col = lerp(cold_white, color.white, random.uniform(0.6, 1))
            stars_colors.append(col)

        self.dust_cloud = Entity(parent=self.pivot, model=Mesh(vertices=stars_pos, colors=stars_colors, mode='point', thickness=2))

        self.systems = []
        for _ in range(20): 
            r = random.uniform(1000, self.radius * 0.9); theta = random.uniform(0, math.tau)
            pos = Vec3(math.cos(theta)*r, random.gauss(0, 50), math.sin(theta)*r)
            self.systems.append(StarSystem(self.pivot, pos))

    def update(self, cam_pos):
        self.pivot.rotation_y += time.dt * 1.0
        dist_to_cam = (self.pivot.world_position - cam_pos).length()
        if dist_to_cam < 15000: 
            for sys in self.systems:
                sys_dist = (sys.center.world_position - cam_pos).length()
                if sys_dist < 4000:
                    sys.enabled = True; sys.update_orbits()
                else: sys.enabled = False

# --- EVREN ---
galaxies = []
def init_universe():
    # Galaksilerin pozisyonları ve rastgele rotasyonları (3 boyutlu yönelimler)
    galaxy_positions = [Vec3(0,0,0), Vec3(20000,5000,10000), Vec3(-18000,-3000,20000), Vec3(10000,15000,-20000)]
    themes = [color.cyan, color.magenta, color.orange, color.white]
    
    for i, pos in enumerate(galaxy_positions):
        # Her galaksi evrende farklı bir açıyla duruyor (X, Y ve Z eksenlerinde rastgele eğim)
        random_rot = Vec3(random.uniform(0, 45), random.uniform(0, 360), random.uniform(0, 45))
        galaxies.append(Galaxy(pos, rotation=random_rot, color_theme=themes[i % len(themes)]))

init_universe()

def update_universe(cam):
    if held_keys['shift']: cam.move_speed = 6000 
    else: cam.move_speed = 600
    for g in galaxies: g.update(cam.world_position)
