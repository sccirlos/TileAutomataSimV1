import json

from UniversalClasses import Assembly, State, Tile

from PyQt5.QtWidgets import QFileDialog

class Historian:

    class Assemblies:
        def __init__(self, movelist, assembly):
            self.movelist = movelist
            self.assembly = assembly

    def __init__(self):
        pass

    def set_ui_parent(self, ui):
        self.ui = ui

    def set_engine(self, engine):
        self.engine = engine
    
    def dump(self):
        filename = QFileDialog.getSaveFileName(self.ui, "Assembly JSON File", "", "JSON Files (*.json)")

        if filename[0] != '':
            fp = open(filename[0], 'w')
            assemblies = self.Assemblies(self.engine.moveList, self.engine.currentAssembly)
            # Dumping into one line saves a ton of space, but becomes completly unreadable, worse than it already is
            # json.dump(assemblies, fp, sort_keys=False, default=self.encoder)
            # Dumping with some indentation makes it nice-ish, but takes a large amount of space for \n and \t and ' '
            json.dump(assemblies, fp, sort_keys=False, default=self.encoder, indent=2)

    def dumps(self):
        print("Dumping Assemblies")
        assemblies = self.Assemblies(self.engine.moveList, self.engine.currentAssembly)
        print(json.dumps(assemblies, sort_keys=False, default=self.encoder, indent=2))
    
    def load(self):
        filename = QFileDialog.getOpenFileName(self.ui, "Select JSON History", "", "JSON Files (*.json)")

        if filename[0] != "":
            fp = open(filename[0], 'r')

            assemblies = json.load(fp)

            # Break down the history
            history = assemblies["history"]
            movelist = []

            for m in history:
                if m["type"] == "a":
                    # converting json into objects
                    x = int(m["x"])
                    y = int(m["y"])
                    s = self.get_state(m["state1"])

                    # add move to movelist
                    newM = {}
                    newM["type"] = "a"
                    newM["x"] = x
                    newM["y"] = y
                    newM["state1"] = s
                    movelist.append(newM)
                else:
                    # converting json into objects
                    x = int(m["x"])
                    y = int(m["y"])
                    s1 = self.get_state(m["state1"])
                    s2 = self.get_state(m["state2"])
                    s3 = self.get_state(m["state1Final"])
                    s4 = self.get_state(m["state2Final"])

                    # add move to movelist
                    newM = {}
                    newM["type"] = "t"
                    newM["x"] = x
                    newM["y"] = y
                    newM["dir"] = m["dir"]
                    newM["state1"] = s1
                    newM["state2"] = s2
                    newM["state1Final"] = s3
                    newM["state2Final"] = s4

                    movelist.append(newM)
            
            # update moveList in engine
            self.engine.moveList = movelist
            self.engine.lastIndex = len(movelist)
            self.engine.currentIndex = len(movelist)

            # Break down the assembly
            assembly = assemblies["assembly"]

            tiles = []
            for t in assembly["tiles"]:
                tile = self.get_tile(t)

                tiles.append(tile)
            
            coords = {}
            for c in assembly["coords"]:
                tile = self.get_tile(assembly["coords"][c])
                coords[c] = tile
                
            # create the Assembly
            currentAssembly = Assembly()
            currentAssembly.label = assembly["label"]
            currentAssembly.leftMost = int(assembly["leftMost"])
            currentAssembly.rightMost = int(assembly["rightMost"])
            currentAssembly.upMost = int(assembly["upMost"])
            currentAssembly.downMost = int(assembly["downMost"])
            currentAssembly.tiles = tiles
            currentAssembly.coords = coords

            # update assembly in engine
            self.engine.currentAssembly = currentAssembly
            self.engine.validMoves = currentAssembly.getMoves(self.engine.system)

            # draw to screen
            self.ui.draw_assembly(self.engine.getCurrentAssembly())
            self.ui.Update_available_moves()
    
    def get_state(self, stateJSON):
        label = stateJSON["label"]
        color = stateJSON["color"]
        s = State(label, color)

        return s
    
    def get_tile(self, t):
        s = self.get_state(t["state"])
        x = int(t["x"])
        y = int(t["y"])
        tile = Tile(s, x, y)

        return tile

    def loads(self):
        print("Loading Assembiles")
        moveHistoryEncoded = json.dumps(self.engine.moveList, sort_keys=False, default=self.encoder, indent=3)
        moveHistoryDecoded = json.loads(moveHistoryEncoded)

        print("History decoded into...")
        print(*moveHistoryDecoded)

        # Convert moveHistoryDecoded from dictionary to actual object it represents (state dictionary into state object)

        eq = moveHistoryEncoded == json.dumps(moveHistoryDecoded, sort_keys=False, default=self.encoder, indent=3)

        if eq:
            print("Strings are the same! History Decode PASS")
        else:
            print("String are NOT the same! History Decode FAIL")
        
        assemblyEncoded = json.dumps(self.engine.currentAssembly, sort_keys=False, default=self.encoder, indent=3)
        assemblyDecoded = json.loads(assemblyEncoded)

        print("Assembly decoded into...")
        print(*assemblyDecoded)

        # Convert assemblyDecoded into actual objects

        eq = assemblyEncoded == json.dumps(assemblyDecoded, sort_keys=False, default=self.encoder, indent=3)

        if eq:
            print("Strings are the same! Assembly Decode PASS")
        else:
            print("String are NOT the same! Assembly Decode FAIL")

    def encoder(self, obj):
        # what state should look like in json
        if isinstance(obj, State):
            statedict = {}
            statedict["label"] = obj.get_label()
            statedict["color"] = obj.returnColor()
            return statedict
        elif isinstance(obj, self.Assemblies):
            dict = {}
            dict["history"] = obj.movelist
            dict["assembly"] = obj.assembly

            return dict
        elif isinstance(obj, Tile):
            tiledict = {}
            tiledict["state"] = obj.state
            tiledict["x"] = obj.x
            tiledict["y"] = obj.y

            return tiledict
        elif isinstance(obj, Assembly):
            # create dictionary from the instance variables
            assemblydict = {}

            assemblydict["label"] = obj.label
            assemblydict["tiles"] = obj.tiles
            assemblydict["coords"] = obj.coords
            assemblydict["leftMost"] = obj.leftMost
            assemblydict["rightMost"] = obj.rightMost
            assemblydict["upMost"] = obj.upMost
            assemblydict["downMost"] = obj.downMost

            return assemblydict
