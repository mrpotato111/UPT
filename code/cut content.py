def checking(self):
    hit_info_forward = raycast(self.position, self.forward, distance=1, ignore=(self, Post))
    hit_info_backward = raycast(self.position, -self.forward, distance=1, ignore=(self, Post))
    if hit_info_forward.hit:
        print(f"hit detected at: {hit_info_forward.point}, participants: {hit_info_forward.entities}")
        self.position = self.position + Vec3(-1, 0, 0)
    if hit_info_backward.hit:
        print(f"hit detected at: {hit_info_backward.point}, participants: {hit_info_backward.entities}")
        self.position = self.position + Vec3(1, 0, 0)
    return hit_info_forward






    def start_timer(self):
        self.timer_started = True
        self.timer = time.time()

    def time_check(self):
        if self.timer_started:
            elapsed_time = time.time() - self.timer
            if elapsed_time >= 10:
                self.timer_started = False
