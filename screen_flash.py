import color_flash

import game


class ScreenFlash(color_flash.ColorFlash):
    def __init__(self, color_list, duration_ms, times, start_delay_ms=0):
        super().__init__(color_list, duration_ms, times, start_delay_ms)

    def update(self):
        super().update()
        if self.is_enabled():
            game.Game.instance().set_bg_color(self.get_current_color())
