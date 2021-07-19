class Tile:
    state_type = None
    tile_num = 0     
        
    def __init__(self, type):
      self.state_type = type
      
      
    def get_state_type(self):
        print("State type is: " + self.state_type)
        return self.state_type
            
class SeedTile(Tile):
    state_type = "S"
    def __init__(self, state_type):
        super().__init__("S")
        self.tile_num = 0
        self.state_type = "S"
        
class NumberedTile(Tile):
      state_number = None
      
      def __init__(self, type, num):
        self.state_type = type
        self.state_number = num

      def get_state_num(self):
        return self.state_number

      def update_state_num(self, num):
        if num is int:  
            self.state_number = num
            print("state num updated")
        else:
            print("state num update failed")
            
      def update_state_type(self, type):
        if type in {"B", "F"}:
            self.state_type = type
            print("state type updated") 
        else:
            print("state type update failed")     

class Assembly:
    
    def __init__(self, q_num):
       self.num_tiles = 0
       self.tiles = []
       self.quit_num = q_num
       self.add_seed_tile()
       
       
    def display_assembly(self):
        print("Display:")
        for i in range(len(self.tiles)):
            if self.tiles[i].state_type == "S":
                print("Index:", i, "Found:", self.tiles[i].state_type)
            else:
                print("Index:", i, "Found:", self.tiles[i].state_type, "Num:", self.tiles[i].state_number)  
       
    def add_seed_tile(self):
        self.seed_tile = SeedTile("S")
        self.tiles.append(self.seed_tile)
        self.num_tiles = 1
        ##print("Seed Added")
        self.add_back_state()
        
    def add_back_state(self):
        if len(self.tiles) == 5:
            exit_display(self)
           
        else:
            back_tile = NumberedTile("B", 0)
            self.tiles.append(back_tile)
            self.num_tiles += 1
            ##print("Back Added")
            self.walk_back()
        
    """ def check_change(self, num_tile_right, num_tile_left):
            if(num_tile_right.state_type == "B"):
                if(num_tile_right.state_number == num_tile_left.state_number):
                    num_tile_left.state_number += 1
                    # print("State num + 1")
                   
                elif(num_tile_right.state_number < num_tile_left.state_number):
                    self.walk_forward() """
                   
                    
    def walk_back(self):
        for index, t in reversed(list(enumerate(self.tiles))):
            
            if t.state_type == "S":
                # print("Found: Seed")
                self.walk_forward(0)
            elif(index == 1):
                ## print("Found: ", index, "Type: ", t.state_type, " Num: ", t.state_number)
                self.walk_forward(1)   
            else:
                ## print("Found: ", index, "Type: ", t.state_type, " Num: ", t.state_number)
                if(t.state_number == self.tiles[index - 1].state_number):
                    self.tiles[index-1].state_number += 1
                    print("Index", index-1, "changed to:", self.tiles[index-1].state_number)
                elif(t.state_number < self.tiles[index - 1].state_number):
                    self.walk_forward(index)    
                

    def walk_forward(self, start_i):
        
        if start_i == 0 or start_i == 1:
            change_to = self.tiles[1].state_number
        else:
            change_to = self.tiles[start_i].state_number 
        for i in range(start_i, len(self.tiles)):
            if i == 0:
                #print("Seed")
                continue 
            else:
                self.tiles[i].state_type = "F"
                self.tiles[i].state_number = change_to
                print("Found: ", self.tiles[i].state_type, " Num: ", self.tiles[i].state_number)   
        self.add_back_state()    
            
def exit_display(assembly):
    assembly.display_assembly()
    print("all done")                    
    quit()

a = Assembly(5)
    
         

