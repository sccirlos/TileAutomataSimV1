import tkinter as tk

class Tile:
    def __init__(self, type, update_status):
      self.state_type = type
      self.color = "#bdbdbd"
      self.width = 30
      self.height = 30
      self.can_update = update_status
      self.can_update_color = True
      
    def get_state_type(self):
        
        return self.state_type

    def set_can_update_color_false(self):
        self.can_update_color = False
        
    def update_color(self, new_color):
        if (self.can_update_color == True):
            self.color = new_color
            
    def __str__(self):
        s = self.state_type
        return "|"+ s +"|"
    
    def display_tile_cmd(self):
        print("|", self.state_type, "| ")        
        
            
class SeedTile(Tile):
    def __init__(self):
        super().__init__("S", False)
        self.update_color( "#42f5b6")
        self.set_can_update_color_false()
        
    def __str__(self):
        s = self.state_type
        return "|"+ s +"|"    

class ReseedTile(Tile):
    
    def __init__(self, state_num):
        super().__init__("R", False)
        self.update_color( "#ffc75e")
        self.set_can_update_color_false()
        self.state_number = state_num
        
    def __str__(self):
        s = self.state_type + ", " + self.state_number
        return "|"+ s +"|"
    
    def display_tile_cmd(self):
        print("|", self.state_type, ", ", self.state_number, "| ")     

    def get_state_num(self):
        return self.state_number 

        
class NumberedTile(Tile):
      
      def __init__(self):
          super().__init__("B", True)
          self.state_number = 0

      def display_tile_cmd(self):
          print("|", self.state_type, ",", self.state_number, "| ")     

      def __str__(self):
        s = self.state_type + ", " + self.state_number.__str__()
        return "|"+ s +"|"
      
      def get_state_num(self):
        return self.state_number

      def update_state_num(self, num):
        if num is int:  
            self.state_number = num
            print("state num updated")
        else:
            print("state num update failed")
            
      def update_state_type(self):
        if self.state_type == "B":
            self.state_type = "F"
            print("B state updated to F state") 
        elif self.state_type == "F":     
            self.state_type = "B"
            print("F state updated to B state") 
        else:
            print("state type update failed")

class Assembly:
    
    def __init__(self, n):
        self.tiles = []
        self.quit_num = n
        self.add_seed_tile()
        
    def add_seed_tile(self):
        s = SeedTile()
        self.tiles.append(s)    
        
    def display_assembly(self):
        if not len(self.tiles) == 0:
            s = ""
            for tile in self.tiles:
                s += tile.__str__() + "; "
            print(s)
                
    def add_tile(self):
        if(len(self.tiles) < self.quit_num):
            n = NumberedTile()
            self.tiles.append(n)
            self.display_assembly()

    def walk_back(self):
        if(len(self.tiles) > 2):
            for tile in reversed(self.tiles):
                if(tile.get_state_type() == "S"):
                    return
                
                elif(tile.get_state_type() != "B"):
                    tile.update_state_type()
        answer = input("Start Walk Forward?  ")
        
        if(answer == "y"):
            self.walk_forward()            
                    

    def walk_forward(self): #add start index
        print("walking forward")
        
        for i in range(1, len(self.tiles)-1):
            if(self.tiles[i].state_type == "B"):
                self.tiles[i].state_type == "F"
            
         

                        

num = 4
a = Assembly(num)
a.display_assembly()
for i in range(num-1):
    answer = input("Add Another?  ")
    if(answer == "y"):
        a.add_tile()
        a.walk_back()        
            
                 