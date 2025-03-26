from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image

move_audio = Audio("/sounds/scanner beep Sound Effect.mp3", loop=False, autoplay=False)

class Coke(Entity):
    def __init__(self, trigger, position=(0,0,0)):
        super().__init__(parent=scene,
                         position=position,
                         model="Coke.obj",
                         collider="mesh",
                         texture="../textures/1934-coke-can.jpeg",
                         shaders=shader,
                         scale= 1
                         )

        self.target_position = (157, 3.5, 30)
        self.trigger = trigger



    def test(self):
        if self.trigger() == True:
            print("test succsessful")
            return True

    def scan(self):
        if mouse.hovered_entity == self and self.test() == True:
            print("target is self")
            self.on_click_movement()

    def on_click_movement(self):
        move_audio.play()
        print("moving to target location")
        self.pos = Vec3(self.target_position) + Vec3(random.uniform(1, 2), 0, random.uniform(1, 2))
        self.animate_position(self.target_position, duration=1, curve=curve.linear)

    def update(self):
        self.test()
        self.scan()



class Big_Bottle1(Coke):
    def __init__(self, trigger, position=(0,0,0), origin_x=20, origin_y=0):
        super().__init__( position=position,
                          trigger=trigger,
                         )
        self.model = "BigBottle1 - Copy.obj"
        self.texture= "../textures/Support_Cover_baseColor.jpeg"

class Bottle2(Coke):
    def __init__(self, trigger, position=(0,0,0)):
        super().__init__(position=position,
                          trigger=trigger,
                         )
        self.model = "Bottle2.blend"
        self.texture = "../textures/Support_Cover_baseColor.jpeg"


class Big_Bottle3(Coke):
    def __init__(self,trigger, position=(0,0,0)):
        super().__init__(position=position,
                          trigger=trigger
                         )
        self.model = "Bottle3.blend"
        self.texture = "../textures/Support_Cover_baseColor.jpeg"

class Big_Bottle4(Coke):
    def __init__(self, trigger, position=(0,0,0)):
        super().__init__(position=position,
                         trigger=trigger
                         )
        self.model = "Bottle4.blend"
        self.texture = "../textures/Support_Cover_baseColor.jpeg"


class Test_Fanta(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(position=position,
                         model="Coke.obj"
                         )
        self.texture = "../textures/s-l160011.jpg"

class Fanta(Coke):
    def __init__(self, trigger, position=(0,0,0)):
        super().__init__(position=position,
                         trigger=trigger)
        self.texture = "../textures/s-l160011.jpg"


class Cashregister(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(parent=scene,
                         position=position,
                         model="cash_register.obj",
                         texture="../textures/body_color.jpg",
                         scale=4,
                         collider="mesh",
                         rotation_y=90
                         )