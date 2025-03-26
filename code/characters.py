from ursina import *
from random import randint
from models_main import *
from computer import Output
from Timer import GameTimer

class Post(Entity):
    def __init__(self, position=(0,0,0), **kwargs):
        colours = [color.white, color.gray, color.azure, color.black33, color.brown]
        super().__init__(parent=scene,
                         position=position,
                         color=colours[randint(0, 4)],
                         model="human4.obj",
                         texture="",
                         scale=0.5,
                         **kwargs)


class Npc(Post):
    def __init__(self, output, game_timer, test, move_test, move_tester, lower_func, move_lower_funct, higher_funct, check_position,
                 itm_spwn, ned_pos, num_of_ent, num_in_row_lower, num_solved, post1, post2, post3, spawned_items, position=(0,0.01,0.),**kwargs):
        super().__init__(position=position,
                         collider="cube",
                         **kwargs)

        self.count = num_of_ent
        self.in_row_num_lower = num_in_row_lower
        self.npcs_solved = num_solved
        self.post1 = post1
        self.post1_true = post1 - Vec3(self.count, 0, 0)
        self.post2 = post2
        self.post3 = post3
        self.has_moved_to_post1 = False
        self.has_moved_to_post2 = False
        self.has_moved_to_post3 = False
        self.test = test
        self.move_test = move_test
        self.move_test_getter = move_tester
        self.test_var = 0
        self.lower_number = lower_func
        self.move_lower_number = move_lower_funct
        self.make_number_bigger = higher_funct
        self.in_row = False
        self.number_change_var = False
        self.position_check = check_position
        self.needed_position = ned_pos
        self.raycast_var = False
        self.checking_var2 = False
        self.item_check = itm_spwn
        self.spawned_items = spawned_items
        self.output = output
        self.game_timer = game_timer
        self.distance = (self.position - self.post1_true).length()
        self.taken_time = self.distance / 10
        self.adjusted_duration = max(1, self.taken_time * (5 / (self.distance + 1)))

    def movement(self):
        if not self.has_moved_to_post1:
            self.look_at(self.post1_true)
            self.animate_position(self.post1_true, duration=self.adjusted_duration, curve=curve.linear)
            self.has_moved_to_post1 = True

    def move_to_correct_position(self):
        if self.position.z == 32 and self.raycast_var == False:
            search_direction = Vec3(0.3, 0, 0)
            ray_distance = 5

            hit_info = raycast(self.position, search_direction, distance=ray_distance, ignore=[self,Post, Wall, Floor])

            if hit_info.hit and hit_info.distance > 1:
                if hit_info.entity:
                    if hit_info.entity.position < 152:
                        found_npc_position = hit_info.entity.position
                        print(f"this is the position of the npc in front {found_npc_position}")
                        new_position = Vec3(round(found_npc_position.x, 0),found_npc_position.y,found_npc_position.z) + Vec3(-1, 0, 0)
                        print(f"I am at {self.position} {hit_info.entity} found at {round(found_npc_position.x, 0)},"
                              f" moving to next available spot at {new_position}.")
                        self.look_at(self.post1)
                        self.animate_position(new_position, duration=1, curve=curve.linear)
                        self.raycast_var = True
                        return self.raycast_var
                    else:
                        new_position = self.post1
                        self.animate_position(new_position, duration=1, curve=curve.linear)
                        self.raycast_var = True
                        return self.raycast_var
            else:
                print("I am first npc")
                self.raycast_var = True
                return self.raycast_var

    def move_to_post2(self):
        self.has_moved_to_post2 = True
        self.look_at(self.post2)
        self.animate_position(self.post2, duration=2, curve=curve.linear)

    def move_to_post3(self):
        self.has_moved_to_post3 = True
        self.look_at(self.post3)
        self.animate_position(self.post3, duration=10, curve=curve.linear)
        self.remove_spawned_items()
        self.output.text_destroyer()
        self.npcs_solved()
        invoke(destroy, self, delay=10)
        self.game_timer.reset_timer()

    def move_up(self):
        new_position = self.position + Vec3(1,0,0)
        if self.position != self.needed_position:
            self.look_at(self.post1)
            self.animate_position(new_position, duration=1, curve=curve.linear)

    def position_test(self):
        return self.position_check(self)

    def higher_number_test(self):
        if self.position.z == 32 and self.has_moved_to_post2 == False:
            return True
        return False

    def higher_number(self):
        if self.higher_number_test() and self.in_row == False:
            print("making number bigger")
            self.make_number_bigger()
            self.in_row = True

    def lower_row_number(self):
        if not self.higher_number_test() and self.has_moved_to_post2 and self.number_change_var == False:
            print("making number smaller")
            self.in_row_num_lower()
            self.number_change_var = True

    def Test(self):
        if self.test():
            print("Q up")
            return True

    def move_tester(self):
        if self.move_test:
            print("npc is moving to post3")
            return True
        return False

    def checking(self):
        hit_info_forward = raycast(self.position, self.forward, distance=0.5, ignore=[self, Post, Wall, Floor,])
        if hit_info_forward.hit:
            print(f"hit detected at: {hit_info_forward.point}, participants: {hit_info_forward.entities}")
            self.position = round(self.position,0)
            self.position = Vec3(round(hit_info_forward.entity.position.x,0) - 1,0.5,32)
        return hit_info_forward

    def remove_spawned_items(self):
        for item in self.spawned_items[:]:
            destroy(item)
            self.spawned_items.remove(item)

    def update(self):
        print(self.position)
        self.move_test = self.move_test_getter()
        self.higher_number_test()
        if self.in_row == False:
            self.higher_number()
        self.lower_row_number()

        self.movement()
        self.move_to_correct_position()

        if self.position.z == 32 and self.has_moved_to_post2 == False and self.raycast_var:
            self.checking()

        if self.has_moved_to_post2 == True and not self.has_moved_to_post3:
            self.look_at(Vec3(155,0.5,29.2))

        if self.Test():
            hit_info = raycast(self.position, Vec3(0.3, 0, 0), distance=3, ignore=[self, Post, Wall, Floor])
            print("q has been pressed")
            if self.position_test() and not hit_info.hit:
                self.item_check()
                self.move_to_post2()
                self.move_lower_number()
            elif not self.has_moved_to_post2 and not self.position_test() and self.position.z == 32:
                print("going boss")
                self.move_up()
                self.move_lower_number()
                return self.count
            elif not self.has_moved_to_post2 and not self.position_test() and not self.position.z == 32:
                self.movement()
            else:
                self.move_lower_number()

        if self.move_tester() and self.has_moved_to_post2 == True:
            self.move_to_post3()

class Test_Npc(Post):
    def __init__(self, post, num_of_ent, position=(0,0.01,0.),**kwargs):
        super().__init__(position=position,
                         collider="cube",
                         **kwargs)

        self.count = num_of_ent
        self.post1 = post
        self.post1_true = self.post1 + Vec3(self.count,0,0)
        self.has_moved_to_post1 = False

    def movement(self):
        if not self.has_moved_to_post1:
            self.look_at(self.post1_true)
            self.animate_position(self.post1_true, duration=1, curve=curve.linear)
            self.has_moved_to_post1 = True


    def update(self):
        self.movement()