from ursina import *
import random


blackhole = Entity(model='sphere', color=color.black,  scale=3)
blackhole_surroundings = [Entity(model='sphere', color=color.rgba(255,100,0,0.01), scale=5) for _ in range(4)]
blackhole_surroundings = [Entity(model='sphere', color=color.rgba(255,100,0,0.01), scale=7) for _ in range(4)]
planet1 = Entity(model='sphere', color=color.blue,  scale=0.5)
planets_satelites = [Entity(model='sphere',color =color.green, scale=0.2) for _ in range(5)]

def draw_ellipse(cx=0, cy=0, cz=0, rx=3, ry=1, segments=64, color=color.white, thickness=2):
    points = []
    for i in range(segments + 1):
        angle = (i / segments) * math.tau
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Vec3(x, y, cz))

    return Entity(model=Mesh(
        vertices=points,
        mode='line',
        thickness=thickness
    ), color=color)

# Işık halkası (parlak kenar)
def create_ring(radius, tilt=0, col=color.white, segments=256, thickness=7):
    points = []
    for i in range(segments + 1):
        angle = (i / segments) * math.tau
        x = radius * math.cos(angle) * math.pi / 3.14
        y = radius * math.sin(angle) * math.sin(math.radians(tilt)) 
        z = radius * math.sin(angle) * math.cos(math.radians(tilt))
        points.append(Vec3(x, y, z))

    return Entity(model=Mesh(
        vertices=points,
        mode='line',
        thickness=thickness
    ), color=col)

# Birden fazla halka — farklı açı ve renk
rings = [
    create_ring(2.5, tilt=0,  col=color.orange,  thickness=4),
    create_ring(3.0, tilt=30,  col=color.yellow,  thickness=3),
    create_ring(3.147, tilt=45,  col=color.red,     thickness=2),
    create_ring(3.5, tilt=60,  col=color.gray,    thickness=1),
]

def rotate_blackhole(cam):

    blackhole.rotation_y += 1
    for i, ring in enumerate(rings):
        ring.rotation_z += time.dt * (10 + i * math.pi)  # Her halka farklı hızda döner
        ring.rotation_y += time.dt * (15 + i * math.pi)  # Her halka farklı hızda döner
        ring.rotation_x += time.dt * (20 + i * math.pi)  # Her halka farklı hızda döner
        for i in range(4):
            blackhole_surroundings[i].rotation_x += time.dt * (20 + i * 5)
    ring.look_at(cam)
    
def move_all_skyspheres():
    planet1.position = (math.sin(time.time()) * math.pi, math.cos(time.time()), math.cos(time.time()) * math.pi)
    planets_satelites[0].position = planet1.position + (math.sin(time.time() * math.pi)*0.7, math.cos(time.time() * math.pi)*0.7, math.cos(time.time() * math.pi)*0.7)
    planets_satelites[1].position = planet1.position + (math.sin(time.time() * math.pi)*0.5, math.cos(time.time() * math.pi)*0.5, math.cos(time.time() * math.pi *0.5))

