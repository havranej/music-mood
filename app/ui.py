import curses
import random

EAR = [
"    ████████████████        ",
"  ████            ██████    ",
"████                  ████  ",
"██                      ██  ",
"        ██████████      ████",
"      ████      ██        ██",
"    ████      ████        ██",
"    ██          ████      ██",
"    ██    ██    ██        ██",
"    ██  ████    ██        ██",
"        ██      ██      ████",
"      ████    ████      ██  ",
"            ████      ████  ",
"        ██████        ██    ",
"    ██████          ██      ",
"██              ████        ",
"██          ██████          ",
"████    ██████              ",
"  ████████                  ",
]


HEIGHT, WIDTH = 26, 98
BAR_WIDTH = 51


class Bar():
    def __init__(self, y, x, fcp = 1, ecp = 2):
        self.width = BAR_WIDTH
        self.window = curses.newwin(1, BAR_WIDTH, y, x)
        self.full_color_pair = fcp
        self.empty_color_pair = ecp
        self.show_value(0, "Initializing...")
    
    def show_value(self, value, text = ""):
        if value < 0:
            value = 0
        if value >= self.width:
            value = self.width - 1
        
        text = " " + text + (" " * (self.width - 2 - len(text)))
        full_part = text[:value]
        empty_part = text[value:]

        self.window.addstr(0,0, full_part, curses.color_pair(self.full_color_pair) | curses.A_DIM)
        
        self.window.addstr(0,value, empty_part, curses.color_pair(self.empty_color_pair) | curses.A_DIM)

        self.window.refresh()


class MainFrame():
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.height = HEIGHT
        self.width = WIDTH

        self.BAR_X_OFFSET = 40
        self.BAR_Y_OFFSET = 5
        self.Y_GAP = 3
        
        self.window = curses.newwin(HEIGHT, WIDTH, y, x)
        self.window.border()

        self.draw_ear()
        self.window.addstr(self.BAR_Y_OFFSET - 1,  self.BAR_X_OFFSET, "Current values", curses.A_BOLD)
        self.window.addstr(self.BAR_Y_OFFSET + self.Y_GAP, self.BAR_X_OFFSET, "Running values", curses.A_BOLD)
        self.window.addstr(self.BAR_Y_OFFSET + 4*self.Y_GAP + 4, self.BAR_X_OFFSET, "Ctrl+C to exit")

        
        self.window.refresh()


        self.bars = {
            "a_current": Bar(self.y + self.BAR_Y_OFFSET, self.x + self.BAR_X_OFFSET),
            "v_current": Bar(self.y + self.BAR_Y_OFFSET + 1, self.x + self.BAR_X_OFFSET ),
            "a_rolling": Bar(self.y + self.BAR_Y_OFFSET + self.Y_GAP + 1, self.x + self.BAR_X_OFFSET ),
            "v_rolling": Bar(self.y + self.BAR_Y_OFFSET + self.Y_GAP + 2, self.x + self.BAR_X_OFFSET ),
        }
        
    def draw_ear(self):
        for i, line in enumerate(EAR):
            self.window.addstr(i + 3, 5, line)

    def draw_random_bars(self):
        for bar in self.bars.values():
            value = random.randint(0, 50)
            text = f"Random value: {value}" 
            bar.show_value(value, text)

    def set_bar_value(self, bar_id, value, text = ""):
        self.bars[bar_id].show_value(value, text)

    def print_rgb(self, rgb, colorname = ""):
        # rgb = [str(x) for x in rgb]
        self.window.addstr(self.BAR_Y_OFFSET + 2*self.Y_GAP + 3, self.BAR_X_OFFSET, "RGB", curses.A_BOLD)
        self.window.addstr(self.BAR_Y_OFFSET + 2*self.Y_GAP + 4, self.BAR_X_OFFSET, f"{rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d} {colorname:>38}")
        self.window.refresh()

    def print_port(self, port):
        if not port:
            port = "None"
            
        self.window.addstr(self.BAR_Y_OFFSET + 3*self.Y_GAP + 3, self.BAR_X_OFFSET, "Port", curses.A_BOLD)
        self.window.addstr(self.BAR_Y_OFFSET + 3*self.Y_GAP + 4, self.BAR_X_OFFSET, port)
        self.window.refresh()