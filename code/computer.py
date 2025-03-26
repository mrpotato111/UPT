from ursina import *
from values import *
from assets import *


class MyButton(Entity):
    def __init__(self,position=(0,0,0)):
        super().__init__(parent=scene,
                         position=position,
                         color=color.blue,
                         scale=(1.25,.96,0),
                         model="cube",
                         collider="box",
                         rotation_x=43
                         )

class NumberButton(Button):
    def __init__(self, text, text_size, position=(0,0,0)):
        super().__init__(parent=scene,
                         position=position,
                         color=color.black33,
                         highlight_color=color.gray,
                         scale=(0.20,0.1,0),
                         text=text,
                         text_color=color.gray,
                         text_size=text_size,
                         collider="box",
                         rotation_x=43
                         )


print_audio = Audio("/sounds/cash-drawer-and-receipt-105386.mp3", loop=False, autoplay=False)
wrong_audio = Audio("/sounds/wrong1.mp3", loop=False, autoplay=False)

class Input(Entity):
    def __init__(self, number, bol_changer, number_getter, wrong_anw_funct):
        super().__init__(parent=scene)

        self.equation = ""
        self.display_lines = []
        self.max_visible_lines = 3
        self.scroll_offset = 0
        self.needed_number = number
        self.bol_change = bol_changer
        self.get_needed_number = number_getter
        self.wrong_answer_funct = wrong_anw_funct

        self.display = Text(parent=scene,
                            text=self.equation,
                            position=(155,5,30),
                            scale=2,
                            origin=(0, 0),
                            background=True,
                            rotation_x=43
        )

        self.create_buttons()

    def create_buttons(self):
        positions = [
            [(153.9, 4.8, 30.5), "1"], [(154.1, 4.8, 30.5), "2"], [(154.3, 4.8, 30.5), "3"],
            [(153.9, 4.7, 30.4), "4"], [(154.1, 4.7, 30.4), "5"], [(154.3, 4.7, 30.4), "6"],
            [(153.9, 4.6, 30.3), "7"], [(154.1, 4.6, 30.3), "8"], [(154.3, 4.6, 30.3), "9"],
            [(153.9, 4.5, 30.2), "0"], [(154.1, 4.5, 30.2), "."]
        ]

        operators = ["C", "="]
        operator_positions = [
            (153.9, 4.4, 30.1), (154.3, 4.5, 30.2)
        ]

        for pos, num in positions:
            button = NumberButton(text=num, text_size=0.2, position=pos)
            button.on_click = lambda n=num: self.add_to_equation(n)

        for pos, op in zip(operator_positions, operators):
            button = NumberButton(text=op, text_size=0.2, position=pos)
            button.on_click = lambda o=op: self.handle_operator(o)


    def add_to_equation(self, value):
        if self.equation == "vale vastus, proovi uuesti":
            self.equation = ""
            self.equation += value
            self.update_display()

        elif self.equation == "Vale sisend, sisesta number":
            self.equation = ""
            self.equation += value
            self.update_display()
        else:
            self.equation += value
            self.update_display()

    def handle_operator(self, operator):
        if operator == "C":
            self.equation = ""
        elif operator == "=":
            try:
                self.equation = str(eval(self.equation))
            except Exception:
                self.equation = "Error"
            print("starting calculation")
            self.checking()
        else:
            self.equation += operator

        self.update_display()

    def checking(self):
        needed_number = self.get_needed_number()
        print(f"Current Needed Number: {needed_number}")
        print(f"User Input: {self.equation}")

        try:
            user_input = float(self.equation)

            if user_input == needed_number:
                print_audio.play()
                print("Õige Vastus!")
                self.equation = ""
                self.update_display()
                self.bol_change()
            else:
                wrong_audio.play()
                self.equation = "vale vastus, proovi uuesti"
                self.wrong_answer_funct()

        except:
            self.equation = "Vale sisend, sisesta number"
            self.update_display()

    def update_display(self):
        self.display.text = self.equation




class Output(TextField):
    def __init__(self, item_list, value, trigger, test, position):
        super().__init__(
            parent=scene,
            scale=(1,2),
            editable=False,
            text="",
            position=position,
            max_lines=10,
        )

        self.bg.color = color.clear
        self.highlight_color = color.white
        self.ignore_input = True
        self.trigger = trigger
        self.test = test
        self.value_text = value
        self.item_list = item_list

    def text_destroyer(self):
            print("destroying text")
            self.ignore_input = False
            self.cursor.y = 0
            self.text = ''''''
            self.simulate_keypress()
            self.cursor.x = 0

    def reset(self):
        if self.ignore_input == False:
            self.ignore_input = True
        return self.ignore_input

    def tester(self):
        if self.test() == True:
            print("test is true")
            return True
        return False

    def check(self):
        if self.trigger() == True:
            print("Trigger is true")
            print(self.item_list)
            for item in self.item_list:
                print("going for round item prices")
                if mouse.hovered_entity == item:
                    print("item is an item")
                    item_name = item.name if hasattr(item, 'name') else str(item)
                    print(item_name)
                    if item_name in item_prices:
                        print("item in item prices")
                        price = item_prices[item_name]
                        print(f"Text added for {item}")
                        if self.text == '''''':
                            print("nothing before")
                            self.add_text(f'''\n{price}''')

                        elif self.text == '''Hästi Tehtud!''':
                            self.cursor.y = 0
                            self.text = ''' '''
                            self.add_text(f'''\n{price}''')
                            self.cursor.x = 0
                        else:
                            print("didnt work")
                            self.add_text(f'''\n{price}''')
                        return
                else:
                    print("item not")

    def text_add(self):
        if self.value_text:
            print("adding text")
            self.add_text(self.value_text)

    def input(self, key):
        if key == "m":
            self.add_text("Hästi Tehtud!")


    def simulate_keypress(self):
        self.input("m")

    def update(self):
        print(self.text)
        self.check()
        self.reset()