from ursina import *
from models_main import *
from characters import *
from assets import Test_Fanta

app = Ursina()

PointLight(shadow_map_resolution=(1,1084), color= color.gray, position=(20,-20,20), radius=3)
PointLight(shadow_map_resolution=(1,1084), color= color.gray, position=(20,100,20)).look_at((20,0,20))

camera = EditorCamera(position=(0,4,0))

post1 = Post(position=(15,0,15))


for x in range(4):
    for z in range(4):
        Floor(position=(x * 20, 0, z * 20))
        Ceiling(position=(x * 20, 8, z * 20))


for x in range(5):
    Wall(position=(x * 20, 0, -20))
    Wall(position=(x * 20, 0, 60))

for z in range(5):
    Wall(position=(-20, 0, -20+z * 20)).rotation_y=90
    Wall(position=(60, 0, -20+z * 20)).rotation_y=90



npc_number = 0
spawn_int = 0
def npc_spawning(var):
    global npc, npc_number
    if var < 1:
        var += randint(-200, 1)
        if var == 1:
            var = -300
            npc_spawner()
            npc_number += 1
        return var, npc_number

def npc_spawner():
    global npc
    x = randint(30, 60)
    z = randint(30, 60)
    npc = Test_Npc(post1.position, npc_number, position=(10,0,10))
    print("npc spawned")

def update():
    npc_spawning(spawn_int)

app.run()

