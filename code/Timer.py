from ursina import *
import time

class GameTimer:
    def __init__(self, client_getter, position, start_time=180):
        self.position = position
        self.start_time = start_time
        self.remaining_time = start_time
        self.get_clients = client_getter
        self.timer_display = Text(text=self.format_time(), position=(0.4, 0.45), scale=2, color=color.white)
        self.last_update = time.time()

    def update(self):
        current_time = time.time()
        elapsed = current_time - self.last_update

        if elapsed >= 1:
            self.remaining_time = max(0, self.remaining_time - 1)
            self.timer_display.text = self.format_time()
            self.last_update = current_time

        # Check if timer reaches 0
        if self.remaining_time <= 0:
            self.on_time_up()

    def reset_timer(self):
        clients_in_row = self.get_clients()
        self.remaining_time = max(1, self.start_time - (clients_in_row*2))
        self.timer_display.text = self.format_time()

    def format_time(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        return f"Time: {minutes:02}:{seconds:02}"

    def on_time_up(self):
        print("Time's up!")