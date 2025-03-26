from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image


app = Ursina()
class Floor(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
                         model="cube",
                         texture="../textures/Bricks_basecolor - Copy.png",
                         shaders=shader,
                         collider="mesh",
                         scale=(20,0,20),
                         position=position,
                         origin_y=0,
                         origin_x=0.5,
                         origin_z=0.5)

class Ceiling(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
                         model="../models_compressed/ceiling_actual12.obj",
                         texture="../textures/floors_Material_BaseColor - Copy.png",
                         collider="box",
                         shaders=shader,
                         position=position,
                         origin_x=10,
                         origin_z=10)


class Wall(Entity):
    def __init__(self, position=(0,0,0), origin_x=10, origin_y=0):
        super().__init__(parent=scene,
                         model="stone_wall_1.obj",
                         texture="../textures/T_Wall_Damaged_2x1_A_BC.png",
                         collider="box",
                         position=position,
                         shaders=shader,
                         origin_x=origin_x,
                         origin_y=origin_y)
class Lamp(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
                         model="../models_compressed/lämp - Copy.obj",
                         texture="../textures/Lamp_DefaultMaterial_BaseColor.png",
                         position=position,
                         origin_y=0.5,
                         origin_x=0.5,
                         origin_z=0.5
                         )


class Store_Shelf(Entity):
    def __init__(self, position=(0,0,0), origin_x=20, origin_y=0):
        super().__init__(parent=scene,
                         model="Self_main - Copy.obj",
                         position=position,
                         shaders=shader,
                         origin_x=origin_x,
                         origin_y=origin_y)





