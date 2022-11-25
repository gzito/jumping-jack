from pygame.time import Clock


class ColorFlash:
    # the last color in colors_list have to be the orginal color to be restored at the end of color flash
    def __init__(self, colors_list, duration_ms, times, start_delay_ms=0):
        self.__colors = colors_list
        self.__next_color_idx = 0
        self.__duration_ms = duration_ms
        self.__counter = 0
        self.__times = times
        self.__clock = None
        self.__start_ms = 0
        self.__current_ms = 0
        self.__start_delay_ms = start_delay_ms
        self.__is_enabled = False

    def start(self):
        self.__clock = Clock()
        self.__start_ms = 0
        self.__current_ms = 0
        self.__is_enabled = True
        self.__counter = 0
        self.__next_color_idx = 0

    def update(self):
        if self.__is_enabled:
            self.__current_ms += self.__clock.tick()
            if self.__current_ms <= self.__start_delay_ms:
                return
            if self.__current_ms - self.__start_ms >= self.__duration_ms:
                self.__start_ms = self.__current_ms
                self.__next_color_idx += 1
                if self.__next_color_idx >= len(self.__colors):
                    self.__next_color_idx = 0
                    self.__counter += 1
                if self.__counter >= self.__times:
                    self.stop()

    def stop(self):
        self.__is_enabled = False

    def is_enabled(self):
        return self.__is_enabled

    def get_current_color(self):
        retval = None
        if self.__is_enabled:
            retval = self.__colors[self.__next_color_idx]
        return retval
