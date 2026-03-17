from ursina import *
from ursina.prefabs.trail_renderer import TrailRenderer
import random
import math

# --- MATEMATİKSEL SABİTLER ---
PHI = (1 + 5**0.5) / 2
GOLDEN_ANGLE = math.tau / (PHI**2)

class Asteroid(Entity):
    def __init__(self, galaxy_pivot):
        super().__init__(
            parent=galaxy_pivot,
            model='sphere',
            color=color.light_gray,
            scale=random.uniform(5, 12),
            texture='white_cube'
        )
        # Manuel kuyruk efekti (TrailRenderer hatasından kaçınmak için)
        self.trail_entities = []
        for i in range(3):
            t = Entity(
                parent=galaxy_pivot,
                model='sphere',
                color=color.rgba(255, 200, 255, 150 - (i * 15)),
                scale=self.scale * (1 - i/12)**(math.pi/12),
                collider=None
            )
            self.trail_entities.append(t)
        
        self.reset_asteroid()

    def reset_asteroid(self):
        # Galaksinin kenarlarından bir yerden başla
        angle = random.uniform(0, math.tau)
        dist = random.uniform(4500, 5500)
        self.position = Vec3(math.cos(angle)*dist, random.uniform(-400, 400), math.sin(angle)*dist)
        
        # Karadeliğin çok yakınından geçecek bir hedef
        offset = Vec3(random.uniform(-400, 400), random.uniform(-200, 200), random.uniform(-400, 400))
        direction = (offset - self.position).normalized()
        
        self.velocity = direction * random.uniform(500, 1500) * (math.pi/6)
        
        # Kuyrukları asteroidin üzerine topla
        for t in self.trail_entities:
            t.position = self.position

    def update(self):
        if not self.enabled: return

        # Kuyruk takibi
        for i in range(len(self.trail_entities)-1, 0, -1):
            self.trail_entities[i].position = self.trail_entities[i-1].position
        if len(self.trail_entities) > 0:
            self.trail_entities[0].position = self.position

        # Karadelikten (0,0,0) gelen kütleçekimi
        dist_sq = self.position.length_squared()
        
        if dist_sq < 25000: # Karadeliğe yutulma
            self.reset_asteroid()
            return

        gravity_strength = 250000000 / dist_sq
        accel = -self.position.normalized() * gravity_strength
        
        self.velocity += accel * time.dt
        self.position += self.velocity * time.dt
        
        # Galaksinin dışına çok çıktıysa resetle
        if self.position.length() > 6000:
            self.reset_asteroid()

class StarSystem:
    def __init__(self, parent_galaxy, position):
        self.center = Entity(parent=parent_galaxy, position=position)
        self.enabled = True 
        
        star_color = random.choice([color.yellow, color.white, color.cyan, color.red, color.orange])
        star_scale = random.uniform(30, 60) 
        self.slider_star = Entity(parent=self.center, model = 'sphere', color= color.white, scale=20,collider=None)
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

        # Hatalı olan range(time.dt) döngüsü düzeltildi veya kaldırıldı
        # Bu kısım başlangıçta anlamsız olduğu için temizlendi.
            
    def update_orbits(self):
        if not self.enabled: return
        for o in self.orbiters:
            o['pivot'].rotation_y += o['speed'] * time.dt * 1.5

class Galaxy:
    def __init__(self, position, rotation, num_stars=5000, color_theme=color.cyan):
        self.pivot = Entity(position=position, rotation=rotation)
        self.radius = 5000 
        
        # 1. Olay Ufku
        self.blackhole = Entity(parent=self.pivot, model='sphere', color=color.black, scale=20, collider=None)
        # --- STİLİZE VE EĞİK KARADELİK ---
        all_vertices = []
        all_colors = []
        for i in range(25):
            r = 300 + (i * 12)
            alpha = 0.25 * (0.15 ** (i/3))
            base_col = lerp(color.orange, color.black, i/12) if i < 12 else lerp(color.yellow, color.black, (i-12)/13)
            safe_color = color.rgba(base_col.r*0, base_col.g*0, base_col.b*10, alpha*105)
            segments = 128
            for j in range(segments + 1):
                theta = (j / segments) * math.tau
                all_vertices.append(Vec3(math.cos(theta)*r, 0, math.sin(theta)*r))
                all_colors.append(safe_color)

        self.disk_mesh = Entity(
            parent=self.pivot,
            model=Mesh(vertices=all_vertices, colors=all_colors, mode='line', thickness=10),
            rotation_x=15, # Eğim 25'ten 20'ye düşürüldü
            rotation_z=15   # Yan yatma açısı daha dengeli olması için 5'e çekildi
        )

        # --- DETAYLI SARMAL GALAKSİ (Çekim Etkili) ---
        stars_pos = []
        stars_colors = []
        num_arms = 4
        arm_spread = 0.35 
        
        for i in range(num_stars):
            arm = (i % num_arms) * (math.tau / num_arms)
            if random.random() > 0.8: arm += random.uniform(0, math.tau)
            
            # Üssü artırarak (1.3) yıldızları merkeze doğru yığdık, başlangıcı 350'ye çektik
            r = random.uniform(0, 1)**1.3 * self.radius + 350
            
            # Merkeze yaklaştıkça kollar daha dar ve düzenli hale gelir (akış hissi)
            dist_factor = r / self.radius
            dynamic_spread = arm_spread * (dist_factor + 0.1)
            
            twist = 3.2
            theta = arm + math.log(r / 400) * twist + random.gauss(0, dynamic_spread)
            
            # Galaktik şişkinlik (merkezde dikey yayılım fazla)
            vertical_spread = (1.0 - dist_factor) * 500 + 40
            
            x = r * math.cos(theta)
            y = random.gauss(0, vertical_spread * 0.4) 
            z = r * math.sin(theta)
            
            stars_pos.append(Vec3(x, y, z))
            
            # --- SAMAN YOLU RENK PALETİ ---
            if dist_factor < 0.22:
                col = lerp(color.rgba(255, 230, 180, 255), color.white, random.uniform(0.3, 0.7))
            elif dist_factor < 0.55:
                dusty_brown = color.rgba(150, 120, 100, 255)
                col = lerp(dusty_brown, color.white, random.uniform(0.4, 0.9))
            else:
                cold_white = color.rgba(230, 245, 255, 255)
                col = lerp(cold_white, color.white, random.uniform(0.6, 1))
            stars_colors.append(col)

        self.dust_cloud = Entity(parent=self.pivot, model=Mesh(vertices=stars_pos, colors=stars_colors, mode='point', thickness=2))

        self.systems = []
        for _ in range(20): 
            r = random.uniform(1000, self.radius * 0.9); theta = random.uniform(0, math.tau)
            pos = Vec3(math.cos(theta)*r, random.gauss(0, 50), math.sin(theta)*r)
            self.systems.append(StarSystem(self.pivot, pos))

        # --- ASTEROİDLERİ EKLE ---
        self.asteroids = []
        for _ in range(12):
            self.asteroids.append(Asteroid(self.pivot))

    def update(self, cam_pos):
        # Galaksi ve Disk beraber döner (Senkronize)
        self.pivot.rotation_y += time.dt * 0.3
        
        dist_to_cam = (self.pivot.world_position - cam_pos).length()
        if dist_to_cam < 15000: 
            # Asteroidleri güncelle (Eğer Entity.update kullanıyorsak buraya gerek kalmayabilir
            # ama galaksi yakınında değilse durdurmak isteyebiliriz)
            for ast in self.asteroids:
                ast.enabled = True
                
            for sys in self.systems:
                sys_dist = (sys.center.world_position - cam_pos).length()
                if sys_dist < 4000:
                    sys.enabled = True; sys.update_orbits()
                else: sys.enabled = False
        else:
            for ast in self.asteroids:
                ast.enabled = False

# --- EVREN ---
galaxies = []
def init_universe():
    galaxy_positions = [Vec3(0,0,0), Vec3(20000,5000,10000), Vec3(-18000,-3000,20000), Vec3(10000,15000,-20000)]
    themes = [color.cyan, color.magenta, color.orange, color.white]
    for i, pos in enumerate(galaxy_positions):
        random_rot = Vec3(random.uniform(0, 45), random.uniform(0, 360), random.uniform(0, 45))
        galaxies.append(Galaxy(pos, rotation=random_rot, color_theme=themes[i % len(themes)]))

init_universe()

def update_universe(cam):
    if held_keys['shift']: cam.move_speed = 6000 
    else: cam.move_speed = 600
    for g in galaxies: g.update(cam.world_position)
