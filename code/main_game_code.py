from random import randint, random
from ursina import *
from ursina import color
from ursina.lights import DirectionalLight, PointLight
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from models_main import *
from characters import *
from assets import *
from computer import *
from values import *
from start_screen import Start_Screen, End_screen

tutorial = False
tut1_play = False
tut2_play = False
tut3_play = False
tut4_play = False

post1_pos = (152, 0.5, 32)
post2_pos = (155, 0.5, 32)
post3_pos = (175, 0.5, 90)
npc_number = 0
npc_list = []
npc_in_row = 0
solved_npc = 0
Q = False
needed_position = post1_pos
spawn_int = 0
spawn_timer = False
pc_pos = (154.2,0,29.2)

item_spwn_var = 0
item_spwn_bol = False
itm_pos = (152.3,3.5,30)
spwn_pos = 0
item_number = 0
trigger = False 
a, b = -1.5, 0.8
c,d = -0.8,0.8
num_value = 0
answer = 0
move_trigger = False

npc = None
coke = None
spawned_items = []
fanta = None
big_bottle1 = None

wrong_answers = 0
start_bol = False
end_bol = False

game_timer = None
s = PointLight(shadow_map_resolution=(1,1084), color= color.gray, position=(150,20,40))
s.look_at(Vec3(150,10,32))
scene.fog_color = color.gray
scene.fog_density = 0.2
Sky(color= color.gray)

fail_audio = Audio("/sounds/timpani-boing-fail-146292.mp3", loop=False, autoplay=False)
tut_audio1 = Audio("/sounds/tutor_audio1_new.mp3", loop=False, autoplay=False)
tut_audio2 = Audio("/sounds/tut_audio2_new.mp3", loop=False, autoplay=False)
tut_audio3 = Audio("/sounds/tut_audio3_new.mp3", loop=False, autoplay=False)
tut_audio4 = Audio("/sounds/tut_audio4_new.mp3", loop=False, autoplay=False)

def item_spawner():
    global item_spwn_var, spwn_pos, item_number, spawned_items

    itm_spwn_int = min(int(round(2+(solved_npc*0.2),0)),6)
    print(itm_spwn_int)

    if tutorial:
        cart = 1
    else:
        cart = randint(1, itm_spwn_int)

    for _ in range(cart):
        print("Going for round")
        spwn_pos = Vec3(itm_pos) + Vec3(random.uniform(a, b), 0, random.uniform(c, d))
        print(f"Spawning at position: {spwn_pos}")

        list_chooser = randint(0, 2)
        item_number += 1

        if list_chooser == 0:
            print("Coke spawned")
            new_item = Coke(trigger_test, position=spwn_pos)
        elif list_chooser == 1:
            print("Fanta spawned")
            new_item = Fanta(trigger_test, position=spwn_pos)
        elif list_chooser == 2:
            print("Big Bottle spawned")
            new_item = Big_Bottle1(trigger_test, position=spwn_pos)

        print("spawning items")
        spawned_items.append(new_item)


        print(f"After spawned items list: {spawned_items}")
    return spwn_pos, item_spwn_var, item_number

def value_insert(value):
    num_value = value
    return num_value

def item_check():
    global item_spwn_bol
    item_spwn_bol = True
    return item_spwn_bol

def item_bol_reset():
    global item_spwn_bol
    if item_spwn_bol == True:
        print("resetting bol")
        item_spwn_bol = False
    return item_spwn_bol

def calculation():
    global spawned_items, answer
    list_answer = []
    for item in spawned_items:
        print(f"{item} found in list")
        item_name = item.name if hasattr(item, 'name') else str(item)
        if item_name in item_prices:
            print(f"adding {item_name} to list")
            price = item_prices[item_name]
            list_answer.append(price)
            print(list_answer)
    answer = round(sum(list_answer),2)
    return answer


def npc_spawning(var):
    global npc, npc_number

    npc_spawn_int = int(round(-300 - (npc_number * 50), 0))

    if spawn_timer:
        print("Npcs are currently not spawning")
    if not spawn_timer:
        if npc_number < 5:
            if var < 1:
                var += randint(npc_spawn_int, 1)
                if var == 1:
                    var = -300
                    npc_spawner()
                    npc_number += 1
                return var, npc_number

def npc_spawner():
    global npc
    x = randint(30, 60)
    z = randint(30, 60)
    npc = Npc(output, game_timer, test, move_trigger, move_test_getter, lower_number, move_lower_number, higher_number, position_checking, item_check,
              needed_position, npc_number, lower_row_number, raise_solved_num, post1.position, post2.position, post3_pos, spawned_items, position=(x, 0.1, z))
    npc_list.append(npc)
    print("npc spawned")

def position_checking(x):
    global npc_number, needed_position
    if x.position == needed_position:
        return True
    return False


def test():
    if Q:
        print("q reset")
        invoke(return_q, delay=0.031)
        return True
    return False

def return_q():
    global Q
    Q = False
    return Q

def return_state():
    global npc_number
    if npc_number < 0:
        npc_number += 1
    return npc_number

def raise_solved_num():
    global solved_npc
    solved_npc += 1
    return solved_npc

def higher_number():
    global npc_in_row
    npc_in_row += 1
    return npc_in_row

def lower_row_number():
    global npc_in_row
    npc_in_row -= 1
    return npc_in_row

def lower_number():
    global npc_number
    npc_number = npc_number - 1
    return npc_number

def move_lower_number():
    global npc_in_row, npc_number, tutorial
    if npc and not tutorial:
        num = 1/npc_in_row
        print(f"this is num:{num}")
        npc_number = npc_number - num
        return npc_number

def move_bol_change():
    global move_trigger
    print("changing move_trigger")
    move_trigger = True
    print(move_trigger)
    invoke(move_trigger_reset, delay=0.064)
    return move_trigger

def move_trigger_reset():
    global move_trigger
    if move_trigger == True:
        print("changing back move")
        move_trigger = False
    return move_trigger

def move_test_getter():
    global move_trigger
    return move_trigger

def get_needed_answer():
    global answer
    return answer

def spawn_timer_reset():
    global spawn_timer
    spawn_timer = False


def scan_test():
    if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'name'):
        entity_name = mouse.hovered_entity.name.lower()
        print(f"Entity Name: {entity_name}")

        if entity_name == "coke":
            print("COOOOOOOKKKKKKEEE")
            return True
    return False


def return_trigger():
    global trigger
    trigger = False
    return trigger


def trigger_test():
    global trigger
    if trigger:
        invoke(return_trigger, delay=0.016)
        return True
    return False

def wrong_answer():
    global wrong_answers
    wrong_answers += 1
    return wrong_answers

def get_in_row():
    global npc_in_row
    return npc_in_row

def input(key):
    global Q, spawn_timer, trigger

    if not spawn_timer:
        if key == "escape":
            quit()
        elif key == 'right mouse down':
            trigger = True
            return trigger
        elif key == "q up":
            Q = True
            spawn_timer = True
            invoke(spawn_timer_reset, delay=1)
            print("q released")
            return Q, spawn_timer
    if spawn_timer:
        print("inputs not active rn")

def game_restart():
    global npc_number,npc_in_row,spawn_int,item_spwn_var,item_spwn_bol,spwn_pos,item_number,num_value,answer,\
        move_trigger,npc,coke,fanta,big_bottle1,spawned_items,wrong_answers,start_bol, pc_pos, output,calculator,end_bol,\
        npc_list, game_timer, solved_npc

    scene.fog_color = color.gray
    scene.fog_density = 0.2

    game_start()

    npc_number = 0
    for existing_item in npc_list[:]:
        destroy(existing_item)
    npc_in_row = 0
    solved_npc = 0
    spawn_int = 0

    item_spwn_var = 0
    item_spwn_bol = False
    spwn_pos = 0
    item_number = 0
    num_value = 0
    answer = 0
    move_trigger = False

    npc = None
    coke = None
    fanta = None
    big_bottle1 = None
    for existing_item in spawned_items[:]:
        destroy(existing_item)
    spawned_items = []

    wrong_answers = 0
    start_bol = False
    end_bol = False
    player.position = pc_pos

    game_timer.reset_timer()

    output.ignore_input = False
    output.text = ''' '''
    output.text_destroyer()
    output.item_list = spawned_items
    calculator.equation = ''' '''
    calculator.update_display()

def tutorial_start():
    global tutorial
    print("tutorial is activated")
    tutorial = True
    return tutorial

def tutorial_end():
    global tutorial
    print("tutorial is deactivated")
    tutorial = False
    return tutorial

def game_start():
    global start, start_bol, player, pc_pos
    if start and hasattr(start, 'name'):
        start_name = start.name.lower()
        player = None

    if not start and start_bol == False:
        print("Game started")
        player = FirstPersonController(position=pc_pos, scale=3, collider="box")
        start_bol = True

    return start_bol

def tut_spawn():
    Npc(output, game_timer, test, move_trigger, move_test_getter, lower_number, move_lower_number,
        higher_number, position_checking, item_check, needed_position, npc_number, lower_row_number,
        post1.position, post2.position, post3_pos, spawned_items, position=(x, 0.1, z))
    npc_list.append(npc)

def Tutorial():
    global tut1_play, tut2_play, tut3_play, tut4_play, npc_number

    if not tut1_play:
        tut_audio1.play()
        tut1_play = True
        return tut1_play

    elif tut1_play and not tut2_play and calculator.equation == "vale vastus, proovi uuesti":
        tut_audio2.play()
        if not npc:
            invoke(npc_spawner, delay = 12)
            npc_number += 1
        tut2_play = True
        return tut2_play, npc_number

    elif tut1_play and not tut2_play and calculator.equation == "Vale sisend, sisesta number":
        tut_audio2.play()
        if not npc:
            invoke(npc_spawner, delay=12)
            npc_number += 1
        tut2_play = True
        return tut2_play, npc_number

    elif tut2_play and not tut3_play and npc_in_row == 1:
        tut_audio3.play()
        tut3_play = True
        return tut3_play

    elif not npc and tut3_play and not tut4_play:
        tut_audio4.play()
        tut4_play = True
        invoke(tutorial_end, delay=4)
        return tut4_play


def update():
    global start, player, end_bol, game_timer, calculator, itm_pos, npc_number

    game_start()

    if not start and tutorial:
        if not game_timer:
            game_timer = GameTimer(get_in_row, position=(31, 5, 30.5), start_time=120)

        if npc_in_row:
            game_timer.update()

        if item_spwn_bol == True:
            print("calling item spawner")
            item_spawner()
            calculation()

        Tutorial()
        item_bol_reset()
        test()



    if not start and not tutorial:
        if not game_timer:
            game_timer = GameTimer(get_in_row, position=(31, 5, 30.5), start_time=120)

        if npc_in_row and not end_bol:
            game_timer.update()

        if game_timer.remaining_time <= 0 and end_bol == False:
            fail_audio.play()
            player.enabled = False
            game_timer.enabled = False
            End_screen(game_restart, answer)
            end_bol = True
            return end_bol

        if wrong_answers == 3 and end_bol == False:
            fail_audio.play()
            player.enabled = False
            game_timer.enabled = False
            End_screen(game_restart, answer)
            end_bol = True
            return end_bol

        if not npc:
            npc_spawner()
            npc_number += 1
            return npc_number


        if item_spwn_bol == True:
            print("calling item spawner")
            item_spawner()
            calculation()

        npc_number = round(npc_number)
        item_bol_reset()
        test()
        npc_spawning(spawn_int)
        return_state()
        print(npc_number)


wall = Wall
floor = Floor

for x in range(10):
    for z in range(10):
        floor(position=(x * 20, 0, z * 20))
        Ceiling(position=(x * 20, 8, z * 20))


for x in range(11):
    wall(position=(x * 20, 0, -20))
    wall(position=(x * 20, 0, 180))

for z in range(11):
    wall(position=(-20, 0, -20+z * 20)).rotation_y=90
    wall(position=(180, 0, -20+z * 20)).rotation_y=90

for z in range(4):
    Cashregister(position=(155, 0, 50 + z * 10))

for z in range(2):
    Cashregister(position=(155, 0, 20 + z * -10))

shelf = Store_Shelf
for x in range(8):
    for z in range(10):
        shelf(position=(40 + x * 10, 0, z * 20)).rotation_y=180

for x in range(10):
    for z in range(10):
        Lamp(position=(x * 14.75, 7.25, z * 14.5))

Entity(model="cube", scale=(0, 30, 0), position=pc_pos, collider="box")

cash_register = Cashregister(position=(155,0,30))

cover = MyButton(position=(154.32, 4.55, 30.3))
calculator = Input(answer, move_bol_change, get_needed_answer, wrong_answer)
output = Output(spawned_items, num_value, trigger_test, test, position=(154.4, 5.2, 30.2))

post1 = Post(position=post1_pos)
post1.visible = False
post2 = Post(position=post2_pos)
post2.visible = False
post3 = Post(position=post3_pos)

def main():
    app = Ursina()
    window.fps_counter.enabled = False
    window.entity_counter.enabled = False
    window.collider_visuals = False
    window.debug = False 

    global start, tutorial_start
    start = Start_Screen(tutorial_start)
    print(start)

    app.run()

if __name__ == "__main__":
    main()