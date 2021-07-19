from time import sleep
import copy

BOARDHEIGHT = 15
BOARDWIDTH = 15
TILE_WIDTH = 5
TILE_HEIGHT = 5
COLOR = ["#bababa", "#d17f79", "#9abfdb"]

class Tile:
    def __init__(self, *args):
        if args == "S":
            self.seed_tile_init(args)
        elif len(args) == 0:
            self.general_tile_init()

    def seed_tile_init(self, s):
        self.symbol = s
        self.id = 0
        self.color = COLOR[0]
        self.x = 0
       
    def general_tile_init(self):    
        self.symbol = "B"
        self.id = 0
        self.color = COLOR[1]
        self.x = 1
        self.state_num = 0
        
    


        
